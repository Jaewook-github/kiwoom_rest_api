import time
from collections import deque
from multiprocessing import Queue

from loguru import logger

from utils import KiwoomTR

# 일반 TR을 처리하는 함수
def tr_general_req_func(tr_req_in_queue: Queue, tr_req_out_queue: Queue):
    logger.debug(f"tr_general_req_func start!")
    kiwoom_tr = KiwoomTR()
    tr_name_to_last_reg_call_time_list_dict = dict(
        계좌조회=deque(maxlen=1), # 1초에 하나씩
        주식기본정보=deque(maxlen=1),
    )

    def tr_validation(tr_key=''):
        if len(tr_name_to_last_reg_call_time_list_dict[tr_key]) > 0:
            last_reg_unix_time = tr_name_to_last_reg_call_time_list_dict[tr_key][0]
            if time.time() - last_reg_unix_time < 1:
                time.sleep(0.05)
                return False
        tr_name_to_last_reg_call_time_list_dict[tr_key].append(time.time())
        return True

    while True:
        data = tr_req_in_queue.get()
        # logger.info(f"TR 일반 요청: {data}")
        if data['action_id'] == "계좌조회":
            if not tr_validation(tr_key='계좌조회'):
                tr_req_in_queue.put(data)
                continue
            else:
                account_info_dict, df = kiwoom_tr.request_all_account_info()
                tr_req_out_queue.put(
                    dict(
                        action_id='계좌조회',
                        df=df,
                        account_info_dict=account_info_dict,
                    )
                )
        elif data['action_id'] == "주식기본정보":
            # 언제 마지막 TR 요청이었는지 체크 -> 조건에 안맞으면 다시 loop
            if not tr_validation(tr_key='주식기본정보'):
                tr_req_in_queue.put(data)
                continue
            else:
                params = {
                    'stk_cd': f"{data['종목코드']}_AL",
                }
                basic_info_dict = kiwoom_tr.fn_ka10007(params)
                tr_req_out_queue.put(
                    dict(
                        action_id="주식기본정보",
                        basic_info_dict=basic_info_dict,
                        종목코드=data['종목코드'],
                    )
                )


def tr_order_req_func(tr_order_req_in_queue: Queue):
    time.sleep(3)
    logger.debug(f"tr_order_req_func start!")
    kiwoom_tr = KiwoomTR()
    while True:
        data = tr_order_req_in_queue.get()
        logger.debug(f"Order Process: {data}")
        if data['action_id'] == "매수주문":
            params = {
                'dmst_stex_tp': 'KRX',  # 국내거래소구분 KRX, NXT, SOR
                'stk_cd': data['종목코드'],  # 종목코드
                'ord_qty': str(int(data['주문수량'])), # 주문수량
                'ord_uv': '' if data['시장가여부'] else str(int(data['주문가격'])), # 주문단가 NXT는 시장가 불가능
                'trde_tp': '3' if data['시장가여부'] else '0',
                'cond_uv': '', # 조건단가
            }
            kiwoom_tr.fn_kt10000(params)
        elif data['action_id'] == "매도주문":
            params = {
                'dmst_stex_tp': 'KRX', # 국내거래소구분 KRX, NXT, SOR
                'stk_cd': data['종목코드'], # 종목코드
                'ord_qty': str(int(data['주문수량'])), # 주문수량
                'ord_uv': '' if data['시장가여부'] else str(int(data['주문가격'])), # 주문단가 NXT는 시장가 불가능
                'trde_tp': '3' if data['시장가여부'] else '0',
                'cond_uv': '', # 조건단가
            }
            kiwoom_tr.fn_kt10001(params)
        elif data['action_id'] == "정정주문":
            params = {
                'dmst_stex_tp': 'KRX', # 국내거래소구분 KRX, NXT, SOR
                'orig_ord_no': data['주문번호'], # 원주문번호
                'stk_cd': data['종목코드'], # 종목코드
                'mdfy_qty': str(int(data['주문수량'])), # 정정수량
                'mdfy_uv': str(int(data['주문가격'])), # 정정단가
                'mdfy_cond_uv': '', # 정정조건단가
            }
            kiwoom_tr.fn_kt10002(params)
        time.sleep(1)