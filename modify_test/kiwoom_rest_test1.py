import os
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
import sys
import datetime
from multiprocessing import Process, Queue

from loguru import logger
import pandas as pd
from PyQt5.QtCore import Qt, QSettings, QTimer, QAbstractTableModel, QTime
from PyQt5 import QtGui, uic
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow

from tr_process_functions import tr_general_req_func, tr_order_req_func
from websocket_functions import run_websocket
from utils import log_exceptions


form_class = uic.loadUiType("main.ui")[0]


class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
            elif role == Qt.TextAlignmentRole:
                return Qt.AlignCenter
            if role == Qt.ForegroundRole:
                if self._data.columns[index.column()] in ("수익률(%)", "전일대비(%)"):
                    try:
                        value = self._data.iloc[index.row(), index.column()]
                        if isinstance(value, str) and "," in value:
                            value = int(value.replace(",", ""))
                        if float(value) < 0:
                            return QColor(Qt.blue)
                        elif float(value) > 0:
                            return QColor(Qt.red)
                    except:
                        return str(value)
        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[section]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._data.index[section]
        return None

    def setData(self, index, value, role):
        return False

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable


def format_number(text_edit):
    # 숫자만 추출 (콤마 제거)
    plain_number = text_edit.text().replace(',', '')

    try:
        # 정수로 변환하고 천 단위로 콤마를 추가
        formatted_number = f"{int(plain_number):,}"
    except ValueError:
        # 입력값이 없거나 숫자가 아닐 때
        formatted_number = ''

    # 커서 위치 저장
    cursor_pos = text_edit.cursorPosition()

    # 포맷된 텍스트 설정
    text_edit.setText(formatted_number)

    # 커서 위치 복원
    text_edit.setCursorPosition(cursor_pos)


class KiwoomAPI(QMainWindow, form_class):
    def __init__(
        self,
         tr_req_queue=None,
         tr_result_queue=None,
         order_tr_req_queue=None,
         websocket_req_queue=None,
         websocket_result_queue=None,
    ):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.autoOnPushButton.clicked.connect(self.auto_trade_on)
        self.autoOffPushButton.clicked.connect(self.auto_trade_off)
        self.savePushButton.clicked.connect(self.save_settings)
        self.popPushButton.clicked.connect(self.pop_btn_clicked)
        self.buyAmountLineEdit.textChanged.connect(lambda: format_number(self.buyAmountLineEdit))
        self.settings = QSettings('MyAPP20250501', 'myApp20250501')
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.load_settings()

        self.tr_req_queue = tr_req_queue
        self.tr_result_queue = tr_result_queue
        self.order_tr_req_queue = order_tr_req_queue
        self.websocket_req_queue = websocket_req_queue
        self.websocket_result_queue = websocket_result_queue

        self.condition_df = pd.DataFrame(columns=["조건index", "조건명"])
        self.condition_name_to_index_dict = dict()
        self.condition_index_to_name_dict = dict()
        self.account_info_df = pd.DataFrame(columns=["종목명", "현재가", "매입가", "보유수량", "매매가능수량", "수익률(%)"])
        try:
            self.realtime_tracking_df = pd.read_pickle("realtime_tracking_df.pkl")
        except FileNotFoundError:
            self.realtime_tracking_df = pd.DataFrame(
                columns=["종목명", "현재가", "매입가", "수익률(%)", "트레일링 발동 여부", "트레일링 발동 후 고가", "매수주문여부", "매도주문여부"]
            )
        self.last_saved_realtime_tracking_df = self.realtime_tracking_df.copy(deep=True)
        self.stock_code_to_basic_info_dict = dict()
        self.order_info_df = pd.DataFrame(columns=["주문접수시간", "종목코드", "주문수량", "매수매도구분"])
        self.realtime_registered_codes_set = set()
        self.amend_ordered_num_set = set()

        self.transaction_cost = 0.18  # % 단위, 세금: 0.15% + 수수료 0.015% x 2
        self.current_realtime_count = 0
        self.max_realtime_count = 95
        self.is_no_transaction = True
        self.has_init = False
        self.init_time()

        self.websocket_req_queue.put(
            dict(action_id="조건검색식리스트")
        )
        self.tr_req_queue.put(
            dict(action_id="계좌조회")
        )

        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.receive_websocket_result)
        self.timer1.start(10) # 0.01초마다

        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.receive_tr_result)
        self.timer2.start(100) # 0.1초마다

        self.timer3 = QTimer()
        self.timer3.timeout.connect(self.update_pandas_models)
        self.timer3.start(1000) # 1초마다

        self.timer4 = QTimer()
        self.timer4.timeout.connect(self.save_pickle)
        self.timer4.start(5000) # 5초마다

        self.timer5 = QTimer()
        self.timer5.timeout.connect(self.check_amend_orders)
        self.timer5.start(1000) # 1초마다

        self.timer6 = QTimer()
        self.timer6.timeout.connect(self.check_valid_time)

    @log_exceptions
    def check_valid_time(self):
        if not (self.market_start_time <= datetime.datetime.now() <= self.market_end_time):
            self.is_no_transaction = True
        else:
            self.is_no_transaction = False

    def check_amend_orders(self):
        self.timer5.stop()
        now_time = datetime.datetime.now()
        for order_num, row in self.order_info_df.copy(deep=True).iterrows():
            try:
                if order_num in self.amend_ordered_num_set:
                    self.order_info_df.drop(order_num, inplace=True)
                    continue
                주문접수시간 = row['주문접수시간']  # HHMMSS
                종목코드 = row['종목코드']
                주문수량 = row['주문수량']
                매수매도구분 = row['매수매도구분']
                if 종목코드 not in self.realtime_tracking_df.index:
                    continue
                basic_info_dict = self.stock_code_to_basic_info_dict.get(종목코드, None)
                if basic_info_dict is None:
                    logger.info(f"종목코드: {종목코드} 기본정보 부재!")
                    continue
                order_time = datetime.datetime.now().replace(
                    hour=int(주문접수시간[:-4]),
                    minute=int(주문접수시간[-4:-2]),
                    second=int(주문접수시간[-2:]),
                )
                if now_time > order_time and (now_time - order_time).seconds > self.amendOrderSpinBox.value():
                    logger.debug(f"종목코드: {종목코드}, 주문번호: {order_num} 정정 주문 진행!")
                    if 매수매도구분 == "매수":
                        주문가격 = basic_info_dict["상한가"]
                    elif 매수매도구분 == "매도":
                        주문가격 = basic_info_dict["하한가"]
                    else:
                        logger.info(f"매수매도구분: {매수매도구분} continue!")
                        continue
                    self.order_info_df.drop(order_num, inplace=True)
                    self.order_tr_req_queue.put(
                        dict(
                            action_id="정정주문",
                            종목코드=종목코드,
                            주문번호=order_num,
                            주문수량=주문수량,
                            주문가격=주문가격,
                        )
                    )
                    self.amend_ordered_num_set.add(order_num)
            except Exception as e:
                logger.exception(e)
        self.timer5.start(1000)  # 1초마다

    def save_pickle(self):
        self.timer4.stop()
        try:
            are_equal = self.realtime_tracking_df.equals(self.last_saved_realtime_tracking_df)
            if not are_equal:
                self.realtime_tracking_df.to_pickle("realtime_tracking_df.pkl")
                self.last_saved_realtime_tracking_df = self.realtime_tracking_df.copy(deep=True)
                logger.info("Saved df!")
        except Exception as e:
            logger.exception(e)
        self.timer4.start(5000)  # 5초마다

    @log_exceptions
    def pop_btn_clicked(self):
        target_code = self.popStockCodeLineEdit.text().replace(" ", "")
        self.realtime_tracking_df.drop(target_code, inplace=True)
        logger.info(f"종목코드: {target_code} drop")
        self.update_pandas_models()

    def update_pandas_models(self):
        self.timer3.stop()
        try:
            model = PandasModel(self.account_info_df)
            self.accountInfoTableView.setModel(model)
            self.accountInfoTableView.resizeColumnsToContents()
            model2 = PandasModel(self.realtime_tracking_df)
            self.autoTradeInfoTableView.setModel(model2)
            self.autoTradeInfoTableView.resizeColumnsToContents()
        except Exception as e:
            logger.exception(e)
        self.timer3.start(1000)  # 1초마다

    @log_exceptions
    def auto_trade_on(self):
        self.autoOnPushButton.setEnabled(False)
        self.autoOffPushButton.setEnabled(True)
        self.websocket_req_queue.put(
            dict(
                action_id="조건검색실시간등록",
                조건index=self.condition_name_to_index_dict[self.buyConditionComboBox.currentText()],
            )
        )
        logger.info(f"조건명: {self.buyConditionComboBox.currentText()} 실시간 등록")
        self.websocket_req_queue.put(
            dict(
                action_id="조건검색실시간등록",
                조건index=self.condition_name_to_index_dict[self.sellConditionComboBox.currentText()],
            )
        )
        logger.info(f"조건명: {self.sellConditionComboBox.currentText()} 실시간 등록")
        self.is_no_transaction = False
        self.init_time()
        self.marketStartTimeEdit.setEnabled(False)
        self.marketEndTimeEdit.setEnabled(False)
        self.timer6.start(1000)  # 1초마다

    def init_time(self):
        market_start_time = self.marketStartTimeEdit.dateTime()
        self.market_start_time = datetime.datetime.now().replace(
            hour=market_start_time.time().hour(),
            minute=market_start_time.time().minute(),
            second=market_start_time.time().second(),
        )
        market_end_time = self.marketEndTimeEdit.dateTime()
        self.market_end_time = datetime.datetime.now().replace(
            hour=market_end_time.time().hour(),
            minute=market_end_time.time().minute(),
            second=market_end_time.time().second(),
        )

    @log_exceptions
    def auto_trade_off(self):
        self.autoOnPushButton.setEnabled(True)
        self.autoOffPushButton.setEnabled(False)
        self.websocket_req_queue.put(
            dict(
                action_id="조건검색실시간해제",
                조건index=self.condition_name_to_index_dict[self.buyConditionComboBox.currentText()],
            )
        )
        logger.info(f"조건명: {self.buyConditionComboBox.currentText()} 실시간 등록 해제")
        self.websocket_req_queue.put(
            dict(
                action_id="조건검색실시간해제",
                조건index=self.condition_name_to_index_dict[self.sellConditionComboBox.currentText()],
            )
        )
        logger.info(f"조건명: {self.sellConditionComboBox.currentText()} 실시간 등록 해제")
        self.is_no_transaction = True
        self.marketStartTimeEdit.setEnabled(True)
        self.marketEndTimeEdit.setEnabled(True)
        self.timer6.stop()

    def register_realtime_info(self, stock_code):
        if stock_code not in self.realtime_registered_codes_set:
            self.realtime_registered_codes_set.add(stock_code)
            self.websocket_req_queue.put(
                dict(
                    action_id="실시간등록",
                    종목코드=stock_code,
                )
            )
            self.current_realtime_count += 1

    @log_exceptions
    def on_receive_account_info(self, data):
        df = data['df']
        if len(df) > 0:
            self.account_info_df = df[["종목코드", "종목명", "현재가", "매입가", "보유수량", "매매가능수량", "수익률(%)"]]
            self.account_info_df.set_index("종목코드", inplace=True)
            for stock_code, row in self.account_info_df.iterrows():
                self.register_realtime_info(stock_code)
                if self.stock_code_to_basic_info_dict.get(stock_code) is None:
                    self.tr_req_queue.put(
                        dict(
                            action_id="주식기본정보",
                            종목코드=stock_code,
                        )
                    )
                if stock_code in self.realtime_tracking_df.index:
                    self.realtime_tracking_df.at[stock_code, "매입가"] = row["매입가"]
                    self.realtime_tracking_df.at[stock_code, "현재가"] = row["현재가"]
                    self.realtime_tracking_df.at[stock_code, "수익률(%)"] = row["수익률(%)"]
        if not self.has_init:
            for stock_code, row in self.realtime_tracking_df.copy(deep=True).iterrows():
                if stock_code not in self.account_info_df.index:
                    self.realtime_tracking_df.drop(stock_code, inplace=True)
                    logger.debug(f"종목코드: {stock_code}, 실시간 트래킹 리스트에서 drop!")
        self.update_pandas_models()
        self.has_init = True

    def receive_tr_result(self):
        self.timer2.stop()
        try:
            if not self.tr_result_queue.empty():
                data = self.tr_result_queue.get()
                if data['action_id'] == "계좌조회":
                    self.on_receive_account_info(data)
                elif data['action_id'] == "주식기본정보":
                    basic_info_dict = data['basic_info_dict']
                    종목코드 = data['종목코드']
                    self.stock_code_to_basic_info_dict[종목코드] = basic_info_dict
                    if 종목코드 in self.realtime_tracking_df.index and self.realtime_tracking_df.at[종목코드, "매수주문여부"] == False:
                        logger.info(f"종목코드: {종목코드} 매수주문 진행!")
                        현재가 = basic_info_dict["현재가"]
                        self.realtime_tracking_df.at[종목코드, "종목명"] = basic_info_dict["종목명"]
                        self.realtime_tracking_df.at[종목코드, "현재가"] = 현재가
                        self.realtime_tracking_df.at[종목코드, "매수주문여부"] = True
                        시장가여부 = self.marketBuyRadioButton.isChecked()
                        주문가격 = ''
                        if not 시장가여부:
                            틱단위 = self.get_tick_size(현재가)
                            주문가격 = self.get_order_price(현재가 + self.limitBuySpinBox.value() * 틱단위)
                        주문금액 = int(self.buyAmountLineEdit.text().replace(",", ""))
                        주문수량 = int(주문금액 // 주문가격) if 주문가격 != '' else int(주문금액 // 현재가)
                        if 주문수량 <= 0:
                            logger.debug(f"종목코드: {종목코드}, 주문수량: {주문수량}")
                            self.timer2.start(100)
                            return
                        logger.debug(f"종목코드: {종목코드}, 현재가: {현재가}, 주문가격: {주문가격}")
                        self.order_tr_req_queue.put(
                            dict(
                                action_id="매수주문",
                                종목코드=종목코드,
                                주문수량=주문수량,
                                주문가격=주문가격,
                                시장가여부=시장가여부,
                            )
                        )
                elif data['action_id'] == "":
                    pass
        except Exception as e:
            logger.exception(e)
        self.timer2.start(100)

    @staticmethod
    def get_order_price(now_price):
        now_price = int(now_price)
        if now_price < 2000:
            return now_price
        elif 5000 > now_price >= 2000:
            return now_price - now_price % 5
        elif now_price >= 5000 and now_price < 20000:
            return now_price - now_price % 10
        elif now_price >= 20000 and now_price < 50000:
            return now_price - now_price % 50
        elif now_price >= 50000 and now_price < 200000:
            return now_price - now_price % 100
        elif now_price >= 200000 and now_price < 500000:
            return now_price - now_price % 500
        else:
            return now_price - now_price % 1000

    @staticmethod
    def get_tick_size(now_price):
        now_price = int(now_price)
        if now_price < 2000:
            return 1
        elif 5000 > now_price >= 2000:
            return 5
        elif now_price >= 5000 and now_price < 20000:
            return 10
        elif now_price >= 20000 and now_price < 50000:
            return 50
        elif now_price >= 50000 and now_price < 200000:
            return 100
        elif now_price >= 200000 and now_price < 500000:
            return 500
        else:
            return 1000

    def on_receive_order_result(self, data):
        종목코드 = data['종목코드']
        주문상태 = data['주문상태']
        단위체결가 = data['단위체결가']
        단위체결량 = data['단위체결량']
        주문수량 = data['주문수량']
        미체결수량 = data['미체결수량']
        종목명 = data['종목명']
        주문및체결시간 = data['주문및체결시간']
        주문번호 = data['주문번호']
        주문구분 = data['주문구분']
        if 주문상태 == "접수" and 종목코드 in self.realtime_tracking_df.index:
            self.order_info_df.loc[주문번호] = {
                "주문접수시간": 주문및체결시간, "종목코드": 종목코드, "주문수량": 주문수량, "매수매도구분": 주문구분,
            }

        if 주문상태 == "체결" and 미체결수량 == 0 and 주문번호 in self.order_info_df.index:
            logger.debug(f"주문번호: {주문번호} 체결완료!")
            self.order_info_df.drop(주문번호, inplace=True)

        if 주문상태 == "체결" and data['주문구분'] in ("매수", "매수정정"):
            if 종목코드 in self.account_info_df.index:
                보유수량 = self.account_info_df.at[종목코드, "보유수량"]
                매입가 = self.account_info_df.at[종목코드, "매입가"]
                new_매입가 = round((매입가 * 보유수량 + 단위체결가 * 단위체결량) / (보유수량 + 단위체결량), 1)
                self.account_info_df.at[종목코드, "보유수량"] = 보유수량 + 단위체결량
                self.account_info_df.at[종목코드, "매매가능수량"] += 단위체결량
                self.account_info_df.at[종목코드, "매입가"] = new_매입가
                if 종목코드 in self.realtime_tracking_df.index:
                    self.realtime_tracking_df.at[종목코드, "매입가"] = new_매입가
            else:  # 신규편입
                self.account_info_df.loc[종목코드] = {
                    "종목명": 종목명,
                    "현재가": 단위체결가,
                    "매입가": 단위체결가,
                    "보유수량": 단위체결량,
                    "매매가능수량": 단위체결량,
                    "수익률(%)": -self.transaction_cost,
                }
                if 종목코드 in self.realtime_tracking_df.index:
                    self.realtime_tracking_df.at[종목코드, "매입가"] = 단위체결가
                    self.realtime_tracking_df.at[종목코드, "수익률(%)"] = -self.transaction_cost
        elif 주문상태 == "체결" and data['주문구분'] in ("매도", "매도정정"):
            if 종목코드 in self.account_info_df.index:
                self.account_info_df.at[종목코드, "보유수량"] -= 단위체결량
                self.account_info_df.at[종목코드, "매매가능수량"] -= 단위체결량
                보유수량 = self.account_info_df.at[종목코드, "보유수량"]
                if 보유수량 <= 0:
                    self.account_info_df.drop(종목코드, inplace=True)
                    if 종목코드 in self.realtime_tracking_df.index:
                        self.realtime_tracking_df.drop(종목코드, inplace=True)
                        logger.info(f"종목코드: {종목코드} 트래킹 리스트에서 drop!")
                        self.websocket_req_queue.put(
                            dict(
                                action_id="실시간해제",
                                종목코드=종목코드,
                            )
                        )
                        if 종목코드 in self.realtime_registered_codes_set:
                            self.realtime_registered_codes_set.remove(종목코드)
                        self.current_realtime_count -= 1

    def on_receive_condition_list(self, data):
        self.condition_df = data['df']
        self.condition_name_to_index_dict = dict(zip(self.condition_df["조건명"], self.condition_df["조건index"]))
        self.condition_index_to_name_dict = dict(zip(self.condition_df["조건index"], self.condition_df["조건명"]))
        self.buyConditionComboBox.addItems(self.condition_df["조건명"])
        self.sellConditionComboBox.addItems(self.condition_df["조건명"])
        self.load_settings(is_init=False)
        logger.info("조건검색식리스트 가져오기 성공!")

    @log_exceptions
    def on_receive_realtime_condition_event(self, data):
        조건식idx = data['조건식idx']
        종목코드 = data['종목코드']
        편입편출 = data['편입편출']
        # 조건식 기반 매수
        if all(
            [
                self.current_realtime_count < self.max_realtime_count,
                self.condition_name_to_index_dict[self.buyConditionComboBox.currentText()] == 조건식idx,
                편입편출 == "I",
                not self.is_no_transaction,
                len(self.realtime_tracking_df) < self.maxAutoTradeCountSpinBox.value(),
                종목코드 not in self.account_info_df.index,
                종목코드 not in self.realtime_tracking_df.index,
            ]
        ):
            logger.debug(f"종목코드: {종목코드} 실시간등록 / 주식기본정보 요청 진행")
            self.register_realtime_info(종목코드)
            self.tr_req_queue.put(
                dict(
                    action_id="주식기본정보",
                    종목코드=종목코드,
                )
            )
            self.realtime_tracking_df.loc[종목코드] = {
                "종목명": None,
                "현재가": None,
                "매입가": None,
                "수익률(%)": None,
                "트레일링 발동 여부": False,
                "트레일링 발동 후 고가": None,
                "매수주문여부": False,
                "매도주문여부": False,
            }
        # 조건식 기반 매도
        if all(
            [
                종목코드 in self.realtime_tracking_df.index and self.realtime_tracking_df.at[종목코드, "매수주문여부"] == True,
                종목코드 in self.realtime_tracking_df.index and self.realtime_tracking_df.at[종목코드, "매도주문여부"] == False,
                self.condition_name_to_index_dict[self.sellConditionComboBox.currentText()] == 조건식idx,
                편입편출 == "I",
                not self.is_no_transaction,
            ]
        ):
            logger.info(f"종목코드: {종목코드} 조건식 기반 매도!")
            self.sell_order(종목코드)

    def sell_order(self, 종목코드):
        if 종목코드 not in self.account_info_df.index:
            logger.info(f"종목코드: {종목코드} is not in account info!")
            return
        self.realtime_tracking_df.at[종목코드, "매도주문여부"] = True
        logger.debug(f"종목코드: {종목코드} 매도 진행")
        시장가여부 = self.marketSellRadioButton.isChecked()
        주문가격 = ''
        주문수량 = self.account_info_df.at[종목코드, "매매가능수량"]
        현재가 = self.account_info_df.at[종목코드, "현재가"]
        if not 시장가여부:
            틱단위 = self.get_tick_size(현재가)
            주문가격 = self.get_order_price(현재가 + self.limitSellSpinBox.value() * 틱단위)
        self.order_tr_req_queue.put(
            dict(
                action_id="매도주문",
                종목코드=종목코드,
                주문수량=주문수량,
                주문가격=주문가격,
                시장가여부=시장가여부,
            )
        )

    def on_receive_realtime_tick(self, data):
        종목코드 = data['종목코드']
        현재가 = data['현재가']
        if 종목코드 in self.account_info_df.index:
            self.account_info_df.at[종목코드, "현재가"] = 현재가
            매입가 = self.account_info_df.at[종목코드, "매입가"]
            수익률 = round((현재가 - 매입가) / 매입가 * 100 - self.transaction_cost, 2)
            self.account_info_df.at[종목코드, "수익률(%)"] = 수익률
            if 종목코드 in self.realtime_tracking_df.index:
                self.on_realtime_tracking_df_update(종목코드, 현재가, 수익률)

    def on_realtime_tracking_df_update(self, 종목코드, 현재가, 수익률):
        self.realtime_tracking_df.at[종목코드, "현재가"] = 현재가
        self.realtime_tracking_df.at[종목코드, "수익률(%)"] = 수익률
        if self.is_no_transaction:
            return
        매도주문여부 = self.realtime_tracking_df.at[종목코드, "매도주문여부"]
        트레일링발동여부 = self.realtime_tracking_df.at[종목코드, "트레일링 발동 여부"]
        트레일링발동후고가 = self.realtime_tracking_df.at[종목코드, "트레일링 발동 후 고가"]
        if 트레일링발동여부 and not pd.isnull(트레일링발동후고가):
            트레일링발동후고가 = max(트레일링발동후고가, 현재가)
            self.realtime_tracking_df.at[종목코드, "트레일링 발동 후 고가"] = 트레일링발동후고가
        if 매도주문여부 == False and self.stopLossCheckBox.isChecked() and 수익률 < self.stopLossDoubleSpinBox.value():
            logger.info(f"종목코드: {종목코드} 수익률: {수익률: .4f} < {self.stopLossDoubleSpinBox.value()}으로 스탑로스 발동!")
            self.sell_order(종목코드)
        if all(
            [
                트레일링발동여부 == False,
                매도주문여부 == False,
                self.trailingStopCheckBox.isChecked(),
                수익률 >= self.trailingStopDoubleSpinBox1.value(),
            ]
        ):
            logger.info(f"종목코드: {종목코드} 수익률: {수익률: .4f} >= {self.trailingStopDoubleSpinBox1.value()}으로 트레일링 스탑 발동!")
            self.realtime_tracking_df.at[종목코드, "트레일링 발동 후 고가"] = 현재가
            self.realtime_tracking_df.at[종목코드, "트레일링 발동 여부"] = True

        if all(
            [
                트레일링발동여부 == True,
                매도주문여부 == False,
                not pd.isnull(트레일링발동후고가) and (현재가 - 트레일링발동후고가) / 트레일링발동후고가 * 100 < self.trailingStopDoubleSpinBox2.value(),
            ]
        ):
            logger.info(f"종목코드: {종목코드} 고가대비 하락률(%): {(현재가 - 트레일링발동후고가) / 트레일링발동후고가 * 100: .4f}으로 트레일링 스탑 주문 발동!")
            self.sell_order(종목코드)

    def receive_websocket_result(self):
        self.timer1.stop()
        try:
            if not self.websocket_result_queue.empty():
                data = self.websocket_result_queue.get()
                if data['action_id'] == "실시간체결":
                    self.on_receive_realtime_tick(data)
                elif data['action_id'] == "조건검색식리스트":
                    self.on_receive_condition_list(data)
                elif data['action_id'] == "조건식실시간편입편출":
                    self.on_receive_realtime_condition_event(data)
                elif data['action_id'] == "주문접수및체결":
                    self.on_receive_order_result(data)
        except Exception as e:
            logger.exception(e)
        self.timer1.start(10)

    @log_exceptions
    def load_settings(self, is_init=True):
        self.buyAmountLineEdit.setText(self.settings.value('buyAmountLineEdit', defaultValue="200,000", type=str))
        self.marketBuyRadioButton.setChecked(self.settings.value('marketBuyRadioButton', defaultValue=True, type=bool))
        self.limitBuyRadioButton.setChecked(self.settings.value('limitBuyRadioButton', defaultValue=False, type=bool))
        self.marketSellRadioButton.setChecked(self.settings.value('marketSellRadioButton', defaultValue=True, type=bool))
        self.limitSellRadioButton.setChecked(self.settings.value('limitSellRadioButton', defaultValue=False, type=bool))
        self.stopLossCheckBox.setChecked(self.settings.value('stopLossCheckBox', defaultValue=True, type=bool))
        self.trailingStopCheckBox.setChecked(self.settings.value('trailingStopCheckBox', defaultValue=True, type=bool))
        self.limitBuySpinBox.setValue(self.settings.value("limitBuySpinBox", 0, int))
        self.amendOrderSpinBox.setValue(self.settings.value("amendOrderSpinBox", 60, int))
        self.maxAutoTradeCountSpinBox.setValue(self.settings.value("maxAutoTradeCountSpinBox", 10, int))
        self.limitSellSpinBox.setValue(self.settings.value("limitSellSpinBox", 0, int))
        self.stopLossDoubleSpinBox.setValue(self.settings.value("stopLossDoubleSpinBox", -2.0, float))
        self.trailingStopDoubleSpinBox1.setValue(self.settings.value("trailingStopDoubleSpinBox1", 2.0, float))
        self.trailingStopDoubleSpinBox2.setValue(self.settings.value("trailingStopDoubleSpinBox2", -1.0, float))
        if not is_init:
            self.buyConditionComboBox.setCurrentIndex(self.settings.value('buyConditionComboBox', 0, type=int))
            self.sellConditionComboBox.setCurrentIndex(self.settings.value('sellConditionComboBox', 0, type=int))
        self.marketStartTimeEdit.setTime(QTime.fromString(self.settings.value('marketStartTimeEdit', "090000"), "HHmmss"))
        self.marketEndTimeEdit.setTime(QTime.fromString(self.settings.value('marketEndTimeEdit', "153000"), "HHmmss"))

    @log_exceptions
    def save_settings(self):
        # Write window size and position to config file
        self.settings.setValue('buyAmountLineEdit', self.buyAmountLineEdit.text())
        self.settings.setValue('buyConditionComboBox', self.buyConditionComboBox.currentIndex())
        self.settings.setValue('sellConditionComboBox', self.sellConditionComboBox.currentIndex())
        self.settings.setValue('marketBuyRadioButton', self.marketBuyRadioButton.isChecked())
        self.settings.setValue('limitBuyRadioButton', self.limitBuyRadioButton.isChecked())
        self.settings.setValue('marketSellRadioButton', self.marketSellRadioButton.isChecked())
        self.settings.setValue('limitSellRadioButton', self.limitSellRadioButton.isChecked())
        self.settings.setValue('stopLossCheckBox', self.stopLossCheckBox.isChecked())
        self.settings.setValue('trailingStopCheckBox', self.trailingStopCheckBox.isChecked())
        self.settings.setValue("limitBuySpinBox", self.limitBuySpinBox.value())
        self.settings.setValue("amendOrderSpinBox", self.amendOrderSpinBox.value())
        self.settings.setValue("stopLossDoubleSpinBox", self.stopLossDoubleSpinBox.value())
        self.settings.setValue("trailingStopDoubleSpinBox1", self.trailingStopDoubleSpinBox1.value())
        self.settings.setValue("trailingStopDoubleSpinBox2", self.trailingStopDoubleSpinBox2.value())
        self.settings.setValue("limitSellSpinBox", self.limitSellSpinBox.value())
        self.settings.setValue("maxAutoTradeCountSpinBox", self.maxAutoTradeCountSpinBox.value())
        self.settings.setValue('marketStartTimeEdit', self.marketStartTimeEdit.time().toString("HHmmss"))
        self.settings.setValue('marketEndTimeEdit', self.marketEndTimeEdit.time().toString("HHmmss"))


sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    logger.debug(f"exctype: {exctype}, value: {value}, traceback: {traceback}")
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook


if __name__ == "__main__":
    tr_req_queue = Queue()
    tr_result_queue = Queue()
    order_tr_req_queue = Queue()
    websocket_req_queue = Queue()
    websocket_result_queue = Queue()
    tr_gen_process = Process(
        target=tr_general_req_func,
        args=(tr_req_queue, tr_result_queue),
        daemon=True,
    )
    tr_order_process = Process(
        target=tr_order_req_func,
        args=(order_tr_req_queue, ),
        daemon=True,
    )
    tr_websocket_process = Process(
        target=run_websocket,
        args=(websocket_req_queue, websocket_result_queue),
        daemon=True,
    )
    tr_gen_process.start()
    tr_order_process.start()
    tr_websocket_process.start()

    app = QApplication(sys.argv)
    kiwoom_api = KiwoomAPI(
        tr_req_queue=tr_req_queue,
        tr_result_queue=tr_result_queue,
        order_tr_req_queue=order_tr_req_queue,
        websocket_req_queue=websocket_req_queue,
        websocket_result_queue=websocket_result_queue,
    )
    sys.exit(app.exec_())