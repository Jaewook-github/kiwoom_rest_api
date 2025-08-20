# main.py
import os
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

import time
import datetime as dt
from multiprocessing import Process, Queue
from queue import Empty
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Set

import pandas as pd
from loguru import logger

# 기존 모듈과 동일한 엔드포인트를 사용
from tr_process_functions import tr_general_req_func, tr_order_req_func
from websocket_functions import run_websocket

# ========= 유틸 =========

def now_monotonic():
    return time.monotonic()

def try_get(q: Queue):
    try:
        return q.get_nowait()
    except Empty:
        return None

def load_pickle(path: str, default):
    try:
        return pd.read_pickle(path) if path.endswith(".pkl") and isinstance(default, pd.DataFrame) else default
    except Exception:
        return default

def save_pickle_df(path: str, df: pd.DataFrame):
    try:
        df.to_pickle(path)
        return True
    except Exception as e:
        logger.exception(e)
        return False

def load_ui_state(path: str) -> Dict[str, Any]:
    import pickle, os
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            logger.exception(e)
    # 기본값(예전 QSettings 기본과 동일)
    return dict(
        buyAmountLineEdit="200,000",
        marketBuyRadioButton=True,
        limitBuyRadioButton=False,
        marketSellRadioButton=True,
        limitSellRadioButton=False,
        stopLossCheckBox=True,
        trailingStopCheckBox=True,
        limitBuySpinBox=0,
        amendOrderSpinBox=60,
        maxAutoTradeCountSpinBox=10,
        limitSellSpinBox=0,
        stopLossDoubleSpinBox=-2.0,
        trailingStopDoubleSpinBox1=2.0,
        trailingStopDoubleSpinBox2=-1.0,
        buyConditionComboBox=0,
        sellConditionComboBox=0,
        marketStartTimeEdit="090000",
        marketEndTimeEdit="153000",
    )

def save_ui_state(path: str, state: Dict[str, Any]):
    import pickle
    with open(path, "wb") as f:
        pickle.dump(state, f)

def hhmmss_to_time(s: str) -> dt.time:
    return dt.datetime.strptime(s, "%H%M%S").time()

def get_order_price(now_price: int) -> int:
    # 원본 로직 이식
    now_price = int(now_price)
    if now_price < 2000:
        return now_price
    elif 2000 <= now_price < 5000:
        return now_price - now_price % 5
    elif 5000 <= now_price < 20000:
        return now_price - now_price % 10
    elif 20000 <= now_price < 50000:
        return now_price - now_price % 50
    elif 50000 <= now_price < 200000:
        return now_price - now_price % 100
    elif 200000 <= now_price < 500000:
        return now_price - now_price % 500
    else:
        return now_price - now_price % 1000
# 원본 근거: 호가/틱 계산 규칙. :contentReference[oaicite:4]{index=4}

def get_tick_size(now_price: int) -> int:
    now_price = int(now_price)
    if now_price < 2000:
        return 1
    elif 2000 <= now_price < 5000:
        return 5
    elif 5000 <= now_price < 20000:
        return 10
    elif 20000 <= now_price < 50000:
        return 50
    elif 50000 <= now_price < 200000:
        return 100
    elif 200000 <= now_price < 500000:
        return 500
    else:
        return 1000
# 원본 근거: :contentReference[oaicite:5]{index=5}

def parse_int_from_comma_text(s: str) -> int:
    return int(str(s).replace(",", "").strip()) if str(s).strip() else 0

# ========= 상태 컨테이너 =========

@dataclass
class AutoTradeState:
    # 외부 큐(프런트와 연결)
    in_queue: Queue
    out_queue: Queue

    # 내부 프로세스/큐
    tr_req_queue: Queue = field(default_factory=Queue)
    tr_result_queue: Queue = field(default_factory=Queue)
    order_tr_req_queue: Queue = field(default_factory=Queue)
    websocket_req_queue: Queue = field(default_factory=Queue)
    websocket_result_queue: Queue = field(default_factory=Queue)

    # 데이터프레임/딕셔너리 상태
    condition_df: pd.DataFrame = field(default_factory=lambda: pd.DataFrame(columns=["조건index", "조건명"]))
    condition_name_to_index: Dict[str, int] = field(default_factory=dict)
    condition_index_to_name: Dict[int, str] = field(default_factory=dict)
    account_info_df: pd.DataFrame = field(
        default_factory=lambda: pd.DataFrame(columns=["종목명", "현재가", "매입가", "보유수량", "매매가능수량", "수익률(%)"])
    )
    realtime_tracking_df: pd.DataFrame = field(default_factory=lambda: pd.DataFrame(
        columns=["종목명", "현재가", "매입가", "수익률(%)", "트레일링 발동 여부", "트레일링 발동 후 고가", "매수주문여부", "매도주문여부"]
    ))
    last_saved_realtime_tracking_df: pd.DataFrame = field(default_factory=pd.DataFrame)
    stock_code_to_basic_info: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    order_info_df: pd.DataFrame = field(default_factory=lambda: pd.DataFrame(
        columns=["주문접수시간", "종목코드", "주문수량", "매수매도구분"])
    )
    realtime_registered_codes: Set[str] = field(default_factory=set)
    amend_ordered_num_set: Set[str] = field(default_factory=set)

    # 기타 상태
    transaction_cost: float = 0.18  # %
    current_realtime_count: int = 0
    max_realtime_count: int = 95
    is_no_transaction: bool = True
    has_init: bool = False

    # 시간/설정
    ui_state_path: str = "ui_state.pkl"
    ui_state: Dict[str, Any] = field(default_factory=dict)
    market_start_dt: Optional[dt.datetime] = None
    market_end_dt: Optional[dt.datetime] = None

    def init_time_from_ui(self):
        start_t = hhmmss_to_time(self.ui_state["marketStartTimeEdit"])
        end_t = hhmmss_to_time(self.ui_state["marketEndTimeEdit"])
        now = dt.datetime.now()
        self.market_start_dt = now.replace(hour=start_t.hour, minute=start_t.minute, second=start_t.second, microsecond=0)
        self.market_end_dt = now.replace(hour=end_t.hour, minute=end_t.minute, second=end_t.second, microsecond=0)

# ========= 핵심 루틴 =========

def auto_trade(in_queue: Queue, out_queue: Queue):
    """
    FastAPI/HTMX 백엔드에서 호출될 메인 루틴.
    - in_queue: 프런트/컨트롤러 → 루틴으로 들어오는 명령(버튼, 설정변경 등)
    - out_queue: 루틴 → 프런트로 나가는 이벤트(모델 업데이트, 조건식 리스트 등)
    """
    state = AutoTradeState(in_queue=in_queue, out_queue=out_queue)

    # 1) 내부 하위 프로세스/큐 시작
    tr_gen_process = Process(target=tr_general_req_func, args=(state.tr_req_queue, state.tr_result_queue), daemon=True)
    tr_order_process = Process(target=tr_order_req_func, args=(state.order_tr_req_queue,), daemon=True)
    tr_websocket_process = Process(target=run_websocket, args=(state.websocket_req_queue, state.websocket_result_queue), daemon=True)
    tr_gen_process.start(); tr_order_process.start(); tr_websocket_process.start()

    # 6,7,8) UI 내부 변수 딕셔너리 로드(+전달) 및 DF 로드
    state.ui_state = load_ui_state(state.ui_state_path)
    logger.debug(state.ui_state)
    out_queue.put(dict(action_id="settings_loaded", settings=state.ui_state))
    try:
        state.realtime_tracking_df = pd.read_pickle("realtime_tracking_df.pkl")
        state.last_saved_realtime_tracking_df = state.realtime_tracking_df.copy(deep=True)
    except FileNotFoundError:
        pass

    # 초기 질의: 조건검색식리스트, 계좌조회
    state.websocket_req_queue.put(dict(action_id="조건검색식리스트"))
    state.tr_req_queue.put(dict(action_id="계좌조회"))

    # 타이머에 해당하는 next_run 스케줄 (초)
    interval = dict(
        websocket_result=0.01,  # 10ms
        tr_result=0.1,          # 100ms
        update_models=1.0,      # 1s
        save_pickle=5.0,        # 5s
        check_amend=1.0,        # 1s
        check_valid=1.0,        # 1s (ON일 때만)
    )
    next_run = {k: now_monotonic() for k in interval}

    def check_valid_time():
        if not (state.market_start_dt <= dt.datetime.now() <= state.market_end_dt):
            state.is_no_transaction = True
        else:
            state.is_no_transaction = False
    # 근거: 원본 check_valid_time. :contentReference[oaicite:6]{index=6}

    def register_realtime_info(stock_code: str):
        if stock_code not in state.realtime_registered_codes:
            state.realtime_registered_codes.add(stock_code)
            state.websocket_req_queue.put(dict(action_id="실시간등록", 종목코드=stock_code))
            state.current_realtime_count += 1
    # 근거: 원본 register_realtime_info. :contentReference[oaicite:7]{index=7}

    def update_pandas_models():
        # 프런트로 DF 전달
        account_info_df = state.account_info_df.copy(deep=True).reset_index()
        if "index" in account_info_df.columns:
            account_info_df.rename({"index": "종목코드"}, inplace=True)
        state.out_queue.put(dict(
            action_id="update_pandas_models",
            account_info_df=account_info_df,
            realtime_tracking_df=state.realtime_tracking_df,
        ))
    # 근거: 화면 모델 갱신 역할을 out_queue로 대체. :contentReference[oaicite:8]{index=8}

    def save_pickle():
        if not state.realtime_tracking_df.equals(state.last_saved_realtime_tracking_df):
            if save_pickle_df("realtime_tracking_df.pkl", state.realtime_tracking_df):
                state.last_saved_realtime_tracking_df = state.realtime_tracking_df.copy(deep=True)
                logger.info("Saved df!")
    # 근거: 원본 save_pickle. :contentReference[oaicite:9]{index=9}

    def sell_order(종목코드: str):
        if 종목코드 not in state.account_info_df.index:
            logger.info(f"종목코드: {종목코드} is not in account info!")
            return
        state.realtime_tracking_df.at[종목코드, "매도주문여부"] = True
        시장가여부 = state.ui_state["marketSellRadioButton"]
        주문가격 = ''
        주문수량 = state.account_info_df.at[종목코드, "매매가능수량"]
        현재가 = state.account_info_df.at[종목코드, "현재가"]
        if not 시장가여부:
            틱 = get_tick_size(현재가)
            주문가격 = get_order_price(현재가 + state.ui_state["limitSellSpinBox"] * 틱)
        state.order_tr_req_queue.put(dict(
            action_id="매도주문", 종목코드=종목코드, 주문수량=주문수량, 주문가격=주문가격, 시장가여부=시장가여부
        ))
    # 근거: 원본 sell_order. :contentReference[oaicite:10]{index=10}

    def on_realtime_tracking_df_update(종목코드, 현재가, 수익률):
        df = state.realtime_tracking_df
        df.at[종목코드, "현재가"] = 현재가
        df.at[종목코드, "수익률(%)"] = 수익률
        if state.is_no_transaction:
            return
        매도여부 = df.at[종목코드, "매도주문여부"]
        트발 = df.at[종목코드, "트레일링 발동 여부"]
        트고 = df.at[종목코드, "트레일링 발동 후 고가"]

        if 트발 and pd.notnull(트고):
            df.at[종목코드, "트레일링 발동 후 고가"] = max(트고, 현재가)

        if (매도여부 == False) and state.ui_state["stopLossCheckBox"] and (수익률 < state.ui_state["stopLossDoubleSpinBox"]):
            sell_order(종목코드)

        if all([
            (트발 == False),
            (매도여부 == False),
            state.ui_state["trailingStopCheckBox"],
            수익률 >= state.ui_state["trailingStopDoubleSpinBox1"],
        ]):
            df.at[종목코드, "트레일링 발동 후 고가"] = 현재가
            df.at[종목코드, "트레일링 발동 여부"] = True

        트고 = df.at[종목코드, "트레일링 발동 후 고가"]
        if all([
            (df.at[종목코드, "트레일링 발동 여부"] == True),
            (df.at[종목코드, "매도주문여부"] == False),
            pd.notnull(트고) and ((현재가 - 트고) / 트고 * 100 < state.ui_state["trailingStopDoubleSpinBox2"]),
        ]):
            sell_order(종목코드)
    # 근거: 원본 on_realtime_tracking_df_update. :contentReference[oaicite:11]{index=11}

    def on_receive_realtime_tick(data: Dict[str, Any]):
        종목코드 = data['종목코드']; 현재가 = data['현재가']
        if 종목코드 in state.account_info_df.index:
            state.account_info_df.at[종목코드, "현재가"] = 현재가
            매입가 = state.account_info_df.at[종목코드, "매입가"]
            수익률 = round((현재가 - 매입가) / 매입가 * 100 - state.transaction_cost, 2)
            state.account_info_df.at[종목코드, "수익률(%)"] = 수익률
            if 종목코드 in state.realtime_tracking_df.index:
                on_realtime_tracking_df_update(종목코드, 현재가, 수익률)
    # 근거: 원본 on_receive_realtime_tick. :contentReference[oaicite:12]{index=12}

    def on_receive_order_result(data: Dict[str, Any]):
        # 원본 주문 처리 로직 이식(정정 큐 관리 포함)
        종목코드 = data['종목코드']; 주문상태 = data['주문상태']
        단위체결가 = data['단위체결가']; 단위체결량 = data['단위체결량']
        주문수량 = data['주문수량']; 미체결수량 = data['미체결수량']
        종목명 = data['종목명']; 주문및체결시간 = data['주문및체결시간']
        주문번호 = data['주문번호']; 주문구분 = data['주문구분']

        if 주문상태 == "접수" and 종목코드 in state.realtime_tracking_df.index:
            state.order_info_df.loc[주문번호] = {
                "주문접수시간": 주문및체결시간, "종목코드": 종목코드, "주문수량": 주문수량, "매수매도구분": 주문구분,
            }

        if 주문상태 == "체결" and 미체결수량 == 0 and 주문번호 in state.order_info_df.index:
            state.order_info_df.drop(주문번호, inplace=True)

        if 주문상태 == "체결" and data['주문구분'] in ("매수", "매수정정"):
            if 종목코드 in state.account_info_df.index:
                보유수량 = state.account_info_df.at[종목코드, "보유수량"]
                매입가 = state.account_info_df.at[종목코드, "매입가"]
                new_매입가 = round((매입가 * 보유수량 + 단위체결가 * 단위체결량) / (보유수량 + 단위체결량), 1)
                state.account_info_df.at[종목코드, "보유수량"] = 보유수량 + 단위체결량
                state.account_info_df.at[종목코드, "매매가능수량"] += 단위체결량
                state.account_info_df.at[종목코드, "매입가"] = new_매입가
                if 종목코드 in state.realtime_tracking_df.index:
                    state.realtime_tracking_df.at[종목코드, "매입가"] = new_매입가
            else:
                state.account_info_df.loc[종목코드] = {
                    "종목명": 종목명,
                    "현재가": 단위체결가,
                    "매입가": 단위체결가,
                    "보유수량": 단위체결량,
                    "매매가능수량": 단위체결량,
                    "수익률(%)": -state.transaction_cost,
                }
                if 종목코드 in state.realtime_tracking_df.index:
                    state.realtime_tracking_df.at[종목코드, "매입가"] = 단위체결가
                    state.realtime_tracking_df.at[종목코드, "수익률(%)"] = -state.transaction_cost
        elif 주문상태 == "체결" and data['주문구분'] in ("매도", "매도정정"):
            if 종목코드 in state.account_info_df.index:
                state.account_info_df.at[종목코드, "보유수량"] -= 단위체결량
                state.account_info_df.at[종목코드, "매매가능수량"] -= 단위체결량
                보유수량 = state.account_info_df.at[종목코드, "보유수량"]
                if 보유수량 <= 0:
                    state.account_info_df.drop(종목코드, inplace=True)
                    if 종목코드 in state.realtime_tracking_df.index:
                        state.realtime_tracking_df.drop(종목코드, inplace=True)
                        state.websocket_req_queue.put(dict(action_id="실시간해제", 종목코드=종목코드))
                        if 종목코드 in state.realtime_registered_codes:
                            state.realtime_registered_codes.remove(종목코드)
                        state.current_realtime_count -= 1
    # 근거: 원본 on_receive_order_result. :contentReference[oaicite:13]{index=13}

    def check_amend_orders():
        now = dt.datetime.now()
        for order_num, row in state.order_info_df.copy(deep=True).iterrows():
            try:
                if order_num in state.amend_ordered_num_set:
                    state.order_info_df.drop(order_num, inplace=True)
                    continue
                주문접수시간 = row['주문접수시간']  # HHMMSS
                종목코드 = row['종목코드']; 주문수량 = row['주문수량']; 매수매도구분 = row['매수매도구분']
                if 종목코드 not in state.realtime_tracking_df.index:
                    continue
                basic = state.stock_code_to_basic_info.get(종목코드)
                if basic is None:
                    logger.info(f"종목코드: {종목코드} 기본정보 부재!")
                    continue
                order_time = now.replace(
                    hour=int(주문접수시간[:-4]), minute=int(주문접수시간[-4:-2]), second=int(주문접수시간[-2:])
                )
                if now > order_time and (now - order_time).seconds > state.ui_state["amendOrderSpinBox"]:
                    if 매수매도구분 == "매수":
                        주문가격 = basic["상한가"]
                    elif 매수매도구분 == "매도":
                        주문가격 = basic["하한가"]
                    else:
                        continue
                    state.order_info_df.drop(order_num, inplace=True)
                    state.order_tr_req_queue.put(dict(
                        action_id="정정주문", 종목코드=종목코드, 주문번호=order_num, 주문수량=주문수량, 주문가격=주문가격
                    ))
                    state.amend_ordered_num_set.add(order_num)
            except Exception as e:
                logger.exception(e)
    # 근거: 원본 check_amend_orders. :contentReference[oaicite:14]{index=14}

    def on_receive_account_info(data: Dict[str, Any]):
        df = data['df']
        if len(df) > 0:
            state.account_info_df = df[["종목코드", "종목명", "현재가", "매입가", "보유수량", "매매가능수량", "수익률(%)"]]
            state.account_info_df.set_index("종목코드", inplace=True)
            for stock_code, row in state.account_info_df.iterrows():
                register_realtime_info(stock_code)
                if state.stock_code_to_basic_info.get(stock_code) is None:
                    state.tr_req_queue.put(dict(action_id="주식기본정보", 종목코드=stock_code))
                if stock_code in state.realtime_tracking_df.index:
                    state.realtime_tracking_df.at[stock_code, "매입가"] = row["매입가"]
                    state.realtime_tracking_df.at[stock_code, "현재가"] = row["현재가"]
                    state.realtime_tracking_df.at[stock_code, "수익률(%)"] = row["수익률(%)"]
            if not state.has_init:
                for stock_code, _ in state.realtime_tracking_df.copy(deep=True).iterrows():
                    if stock_code not in state.account_info_df.index:
                        state.realtime_tracking_df.drop(stock_code, inplace=True)
        update_pandas_models()
        state.has_init = True
    # 근거: 원본 on_receive_account_info. :contentReference[oaicite:15]{index=15}

    def on_receive_condition_list(data: Dict[str, Any]):
        state.condition_df = data['df']
        state.condition_name_to_index = dict(zip(state.condition_df["조건명"], state.condition_df["조건index"]))
        state.condition_index_to_name = dict(zip(state.condition_df["조건index"], state.condition_df["조건명"]))
        # UI에 콤보 추가 대신 설정 로드와 브로드캐스트
        out_queue.put({
            "action_id": "on_receive_condition_list",
            "조건명리스트": state.condition_df["조건명"].tolist(),
            "buy_index": state.ui_state.get("buyConditionComboBox", 0),
            "sell_index": state.ui_state.get("sellConditionComboBox", 0),
        })
        out_queue.put(dict(action_id="settings_loaded", settings=state.ui_state))
        # 기존 load_settings(is_init=False) 역할: 인덱스 매핑 유지
        # 프런트에서 콤보 박스 선택을 반영하면 '설정변경'으로 전달

    # ====== 루프 ======
    # 자동매매 ON/OFF 상태에 따라 check_valid 스케줄 동작
    auto_on = False

    while True:
        now = now_monotonic()

        # ---- 2) 각 큐 폴링 (타이머 주기 모사) ----
        if now >= next_run["websocket_result"]:
            next_run["websocket_result"] = now + interval["websocket_result"]
            data = try_get(state.websocket_result_queue)
            if data:
                aid = data.get("action_id")
                if aid == "실시간체결":
                    on_receive_realtime_tick(data)
                elif aid == "조건검색식리스트":
                    on_receive_condition_list(data)
                elif aid == "조건식실시간편입편출":
                    조건식idx = data['조건식idx']; 종목코드 = data['종목코드']; 편입편출 = data['편입편출']
                    # 매수
                    조건명리스트 = state.condition_df["조건명"].tolist()
                    if all([
                        state.current_realtime_count < state.max_realtime_count,
                        state.condition_name_to_index.get(조건명리스트[state.ui_state["buyConditionComboBox"]], -1) == 조건식idx,
                        편입편출 == "I",
                        not state.is_no_transaction,
                        len(state.realtime_tracking_df) < state.ui_state["maxAutoTradeCountSpinBox"],
                        종목코드 not in state.account_info_df.index,
                        종목코드 not in state.realtime_tracking_df.index,
                    ]):
                        register_realtime_info(종목코드)
                        state.tr_req_queue.put(dict(action_id="주식기본정보", 종목코드=종목코드))
                        state.realtime_tracking_df.loc[종목코드] = {
                            "종목명": None, "현재가": None, "매입가": None, "수익률(%)": None,
                            "트레일링 발동 여부": False, "트레일링 발동 후 고가": None,
                            "매수주문여부": False, "매도주문여부": False,
                        }
                    # 매도
                    if all([
                        종목코드 in state.realtime_tracking_df.index and state.realtime_tracking_df.at[종목코드, "매수주문여부"] == True,
                        종목코드 in state.realtime_tracking_df.index and state.realtime_tracking_df.at[종목코드, "매도주문여부"] == False,
                        state.condition_name_to_index.get(조건명리스트[state.ui_state["sellConditionComboBox"]], -1) == 조건식idx,
                        편입편출 == "I",
                        not state.is_no_transaction,
                    ]):
                        sell_order(종목코드)
                elif aid == "주문접수및체결":
                    on_receive_order_result(data)

        if now >= next_run["tr_result"]:
            next_run["tr_result"] = now + interval["tr_result"]
            data = try_get(state.tr_result_queue)
            if data:
                aid = data.get("action_id")
                if aid == "계좌조회":
                    on_receive_account_info(data)
                elif aid == "주식기본정보":
                    basic = data['basic_info_dict']; code = data['종목코드']
                    state.stock_code_to_basic_info[code] = basic
                    if code in state.realtime_tracking_df.index and state.realtime_tracking_df.at[code, "매수주문여부"] == False:
                        logger.info(f"종목코드: {code} 매수주문 진행!")
                        현재가 = basic["현재가"]
                        state.realtime_tracking_df.at[code, "종목명"] = basic["종목명"]
                        state.realtime_tracking_df.at[code, "현재가"] = 현재가
                        state.realtime_tracking_df.at[code, "매수주문여부"] = True
                        시장가여부 = state.ui_state["marketBuyRadioButton"]
                        주문가격 = ''
                        if not 시장가여부:
                            틱 = get_tick_size(현재가)
                            주문가격 = get_order_price(현재가 + state.ui_state["limitBuySpinBox"] * 틱)
                        주문금액 = parse_int_from_comma_text(state.ui_state["buyAmountLineEdit"])
                        주문수량 = int(주문금액 // 주문가격) if 주문가격 != '' else int(주문금액 // 현재가)
                        if 주문수량 <= 0:
                            continue
                        state.order_tr_req_queue.put(dict(
                            action_id="매수주문",
                            종목코드=code, 주문수량=주문수량, 주문가격=주문가격, 시장가여부=시장가여부
                        ))

        if now >= next_run["update_models"]:
            next_run["update_models"] = now + interval["update_models"]
            update_pandas_models()

        if now >= next_run["save_pickle"]:
            next_run["save_pickle"] = now + interval["save_pickle"]
            save_pickle()

        if now >= next_run["check_amend"]:
            next_run["check_amend"] = now + interval["check_amend"]
            check_amend_orders()

        if auto_on and now >= next_run["check_valid"]:
            next_run["check_valid"] = now + interval["check_valid"]
            check_valid_time()

        # ---- 3) 버튼/액션(in_queue) 처리 ----
        cmd = try_get(state.in_queue)
        if cmd:
            aid = cmd.get("action_id")
            if aid == "자동매매ON":
                logger.debug("자동매매ON")
                auto_on = True
                state.is_no_transaction = False
                state.init_time_from_ui()
                # 조건식 실시간 등록
                if state.condition_df is not None and len(state.condition_df) > 0:
                    buy_idx = state.ui_state["buyConditionComboBox"]
                    sell_idx = state.ui_state["sellConditionComboBox"]
                    # 인덱스 → 조건index 값으로 매핑
                    try:
                        buy_cond_name = state.condition_df.iloc[buy_idx]["조건명"]
                        sell_cond_name = state.condition_df.iloc[sell_idx]["조건명"]
                        state.websocket_req_queue.put(dict(action_id="조건검색실시간등록", 조건index=state.condition_name_to_index[buy_cond_name]))
                        state.websocket_req_queue.put(dict(action_id="조건검색실시간등록", 조건index=state.condition_name_to_index[sell_cond_name]))
                    except Exception as e:
                        logger.exception(e)
            elif aid == "자동매매OFF":
                logger.debug("자동매매OFF")
                auto_on = False
                state.is_no_transaction = True
                if state.condition_df is not None and len(state.condition_df) > 0:
                    buy_idx = state.ui_state["buyConditionComboBox"]
                    sell_idx = state.ui_state["sellConditionComboBox"]
                    try:
                        buy_cond_name = state.condition_df.iloc[buy_idx]["조건명"]
                        sell_cond_name = state.condition_df.iloc[sell_idx]["조건명"]
                        state.websocket_req_queue.put(dict(action_id="조건검색실시간해제", 조건index=state.condition_name_to_index[buy_cond_name]))
                        state.websocket_req_queue.put(dict(action_id="조건검색실시간해제", 조건index=state.condition_name_to_index[sell_cond_name]))
                    except Exception as e:
                        logger.exception(e)
            elif aid == "POP":
                target_code = str(cmd.get("종목코드", "")).replace(" ", "")
                logger.debug(f"{target_code} 자동매매에서 제거")
                if target_code in state.realtime_tracking_df.index:
                    state.realtime_tracking_df.drop(target_code, inplace=True)
                    update_pandas_models()
            elif aid == "설정변경":
                # 9) 전체 재매핑 및 저장/방출
                payload = cmd.get("settings", {})
                logger.debug(payload)
                state.ui_state.update(payload)
                save_ui_state(state.ui_state_path, state.ui_state)
                out_queue.put(dict(action_id="settings_loaded", settings=state.ui_state))
                # 시간범위도 갱신
                state.init_time_from_ui()
            elif aid == "계좌조회요청":
                state.tr_req_queue.put(dict(action_id="계좌조회"))
            elif aid == "실시간해제_종목":
                code = cmd.get("종목코드")
                if code:
                    state.websocket_req_queue.put(dict(action_id="실시간해제", 종목코드=code))
                    if code in state.realtime_registered_codes:
                        state.realtime_registered_codes.remove(code)
                        state.current_realtime_count -= 1

        # 너무 바쁘지 않게 살짝 휴식
        time.sleep(0.001)
