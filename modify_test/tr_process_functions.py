import time
from collections import deque
from multiprocessing import Queue

from enhanced_logging import logger, log_tr_request, log_trading, log_error, log_info, log_debug
from utils import KiwoomTR


def tr_general_req_func(tr_req_in_queue: Queue, tr_req_out_queue: Queue):
    log_info("tr_general_req_func 프로세스 시작!")
    try:
        kiwoom_tr = KiwoomTR()
        tr_name_to_last_req_call_time_list_dict = dict(
            계좌조회=deque(maxlen=1),
            주식기본정보=deque(maxlen=1),
            #  ...
        )

        def tr_validation(tr_key=''):
            if len(tr_name_to_last_req_call_time_list_dict[tr_key]) > 0:
                last_req_unix_time = tr_name_to_last_req_call_time_list_dict[tr_key][0]
                if time.time() - last_req_unix_time < 1:
                    time.sleep(0.05)
                    return False
            tr_name_to_last_req_call_time_list_dict[tr_key].append(time.time())
            return True

        while True:
            try:
                data = tr_req_in_queue.get()
                log_debug(f"TR 일반 요청 수신: {data}")

                if data['action_id'] == "계좌조회":
                    if not tr_validation(tr_key="계좌조회"):
                        tr_req_in_queue.put(data)
                        continue
                    else:
                        log_tr_request("계좌조회 요청 처리 시작")
                        account_info_dict, df = kiwoom_tr.reqeust_all_account_info()
                        log_tr_request("계좌조회 요청 처리 완료")
                        tr_req_out_queue.put(
                            dict(
                                action_id='계좌조회',
                                df=df,
                                account_info_dict=account_info_dict,
                            )
                        )

                elif data['action_id'] == "주식기본정보":
                    if not tr_validation(tr_key="주식기본정보"):
                        tr_req_in_queue.put(data)
                        continue
                    else:
                        종목코드 = data['종목코드']
                        log_tr_request(f"주식기본정보 요청 처리 시작 - 종목: {종목코드}")
                        params = {
                            'stk_cd': f"{종목코드}_AL",
                        }
                        basic_info_dict = kiwoom_tr.fn_ka10007(params)
                        log_tr_request(f"주식기본정보 요청 처리 완료 - 종목: {종목코드}")
                        tr_req_out_queue.put(
                            dict(
                                action_id="주식기본정보",
                                basic_info_dict=basic_info_dict,
                                종목코드=종목코드,
                            )
                        )

            except Exception as e:
                log_error(f"TR 일반 요청 처리 중 에러: {str(e)}", exception=True)

    except Exception as e:
        log_error(f"tr_general_req_func 프로세스 초기화 실패: {str(e)}", exception=True)


def tr_order_req_func(tr_order_req_in_queue: Queue):
    time.sleep(3)
    log_info("tr_order_req_func 프로세스 시작!")

    try:
        kiwoom_tr = KiwoomTR()

        while True:
            try:
                data = tr_order_req_in_queue.get()
                log_debug(f"주문 요청 수신: {data}")

                if data['action_id'] == "매수주문":
                    종목코드 = data['종목코드']
                    주문수량 = data['주문수량']
                    주문가격 = data.get('주문가격', '')
                    시장가여부 = data['시장가여부']

                    log_trading(f"매수주문 처리 시작 - 종목: {종목코드}, 수량: {주문수량}, 시장가: {시장가여부}")

                    params = {
                        'dmst_stex_tp': 'KRX',
                        'stk_cd': 종목코드,
                        'ord_qty': str(int(주문수량)),
                        'ord_uv': '' if 시장가여부 else str(int(주문가격)),
                        'trde_tp': '3' if 시장가여부 else '0',
                        'cond_uv': '',
                    }
                    order_no = kiwoom_tr.fn_kt10000(params)
                    log_trading(f"매수주문 처리 완료 - 종목: {종목코드}, 주문번호: {order_no}")

                elif data['action_id'] == "매도주문":
                    종목코드 = data['종목코드']
                    주문수량 = data['주문수량']
                    주문가격 = data.get('주문가격', '')
                    시장가여부 = data['시장가여부']

                    log_trading(f"매도주문 처리 시작 - 종목: {종목코드}, 수량: {주문수량}, 시장가: {시장가여부}")

                    params = {
                        'dmst_stex_tp': 'KRX',
                        'stk_cd': 종목코드,
                        'ord_qty': str(int(주문수량)),
                        'ord_uv': '' if 시장가여부 else str(int(주문가격)),
                        'trde_tp': '3' if 시장가여부 else '0',
                        'cond_uv': '',
                    }
                    order_no = kiwoom_tr.fn_kt10001(params)
                    log_trading(f"매도주문 처리 완료 - 종목: {종목코드}, 주문번호: {order_no}")

                elif data['action_id'] == "정정주문":
                    종목코드 = data['종목코드']
                    주문번호 = data['주문번호']
                    주문수량 = data['주문수량']
                    주문가격 = data['주문가격']

                    log_trading(f"정정주문 처리 시작 - 종목: {종목코드}, 원주문번호: {주문번호}")

                    params = {
                        'dmst_stex_tp': 'KRX',
                        'orig_ord_no': 주문번호,
                        'stk_cd': 종목코드,
                        'mdfy_qty': str(int(주문수량)),
                        'mdfy_uv': str(int(주문가격)),
                        'mdfy_cond_uv': '',
                    }
                    new_order_no = kiwoom_tr.fn_kt10002(params)
                    log_trading(f"정정주문 처리 완료 - 종목: {종목코드}, 정정주문번호: {new_order_no}")

                time.sleep(1)

            except Exception as e:
                log_error(f"주문 요청 처리 중 에러: {str(e)}", exception=True)

    except Exception as e:
        log_error(f"tr_order_req_func 프로세스 초기화 실패: {str(e)}", exception=True)