import time
import datetime
import functools
import inspect
import requests
import random

from enhanced_logging import logger, log_trading, log_tr_request, log_error, log_info, log_debug
import pandas as pd

from config import api_key, api_secret_key, host


def log_exceptions(func):
    """함수 시그니처에 맞게 인자 자동 조정 + try-except 걸어주는 loguru용 데코레이터"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # 함수가 실제 몇 개 positional argument를 기대하는지 확인
            sig = inspect.signature(func)
            parameters = sig.parameters
            param_len = len(parameters)

            # self 빼고 나머지 인자 개수 확인
            if 'self' in parameters:
                param_len -= 1

            # args를 필요한 만큼만 잘라서 함수 호출
            new_args = args[:param_len + 1]  # self + 필요한 만큼

            return func(*new_args, **kwargs)
        except Exception as e:
            log_error(f"Exception occurred in {func.__qualname__}: {str(e)}", exception=True)

    return wrapper


class KiwoomTR:
    def __init__(self):
        log_info("KiwoomTR 초기화 시작")
        self.token = self.login()
        log_info("KiwoomTR 초기화 완료")

    @staticmethod
    def login():
        log_tr_request("토큰 발급 요청 시작")
        params = {
            'grant_type': 'client_credentials',  # grant_type
            'appkey': api_key,  # 앱키
            'secretkey': api_secret_key,  # 시크릿키
        }
        endpoint = '/oauth2/token'
        url = host + endpoint
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',  # 컨텐츠타입
        }

        try:
            response = requests.post(url, headers=headers, json=params)
            response.raise_for_status()
            token = response.json()['token']
            log_tr_request("토큰 발급 성공")
            return token
        except requests.HTTPError as e:
            error_message = f"HTTP Error: {e}\nResponse Body: {response.text}"
            log_error(f"토큰 발급 실패: {error_message}")
            raise requests.HTTPError(error_message) from e

    # 종목정보 리스트
    @log_exceptions
    def fn_ka10099(self, data, cont_yn='N', next_key=''):
        log_tr_request(f"종목정보 리스트 요청 - cont_yn: {cont_yn}")
        endpoint = '/api/dostk/stkinfo'
        url = host + endpoint

        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'authorization': f'Bearer {self.token}',
            'cont-yn': cont_yn,
            'next-key': next_key,
            'api-id': 'ka10099',
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            log_tr_request("종목정보 리스트 요청 성공")
            return response.json()['list']
        except requests.HTTPError as e:
            error_message = f"HTTP Error: {e}\nResponse Body: {response.text}"
            log_error(f"종목정보 리스트 요청 실패: {error_message}")
            raise requests.HTTPError(error_message) from e

    # 일별주가요청
    @log_exceptions
    def fn_ka10086(self, data, cont_yn='N', next_key=''):
        log_tr_request(f"일별주가 요청 - 종목: {data.get('stk_cd', 'Unknown')}")
        endpoint = '/api/dostk/mrkcond'
        url = host + endpoint

        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'authorization': f'Bearer {self.token}',
            'cont-yn': cont_yn,
            'next-key': next_key,
            'api-id': 'ka10086',
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            has_next = response.headers.get('cont-yn') == "Y"
            next_key = response.headers.get('next-key', '')
            res = response.json()['daly_stkpc']
            df = pd.DataFrame(res)
            df = df[::-1].reset_index(drop=True)
            for column_name in ["open_pric", "high_pric", "low_pric", "close_pric"]:
                df[column_name] = df[column_name].apply(lambda x: abs(int(x)))
            column_name_to_kor_name_map = {
                "date": "날짜",
                "open_pric": "시가",
                "high_pric": "고가",
                "low_pric": "저가",
                "close_pric": "종가",
                "pred_rt": "전일비",
                "flu_rt": "등락률",
                "trde_qty": "거래량",
                "amt_mn": "금액(백만)",
                "crd_rt": "신용비",
                "ind": "개인",
                "orgn": "기관",
                "for_qty": "외인수량",
                "frgn": "외국계",
                "prm": "프로그램",
                "for_rt": "외인비",
                "for_poss": "외인보유",
                "for_wght": "외인비중",
                "for_netprps": "외인순매수",
                "orgn_netprps": "기관순매수",
                "ind_netprps": "개인순매수",
                "crd_remn_rt": "신용잔고율",
            }
            df.rename(columns=column_name_to_kor_name_map, inplace=True)
            log_tr_request(f"일별주가 요청 성공 - 데이터 {len(df)}건")
            return df, has_next, next_key
        except requests.HTTPError as e:
            error_message = f"HTTP Error: {e}\nResponse Body: {response.text}"
            log_error(f"일별주가 요청 실패: {error_message}")
            raise requests.HTTPError(error_message) from e

    # 계좌평가잔고내역요청
    @log_exceptions
    def fn_kt00018(self, data, cont_yn='N', next_key=''):
        log_tr_request(f"계좌평가잔고 요청 - cont_yn: {cont_yn}")
        endpoint = '/api/dostk/acnt'
        url = host + endpoint

        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'authorization': f'Bearer {self.token}',
            'cont-yn': cont_yn,
            'next-key': next_key,
            'api-id': 'kt00018',
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            res = response.json()
            has_next = response.headers.get('cont-yn') == "Y"
            next_key = response.headers.get('next-key', '')
            account_info_dict = dict(
                총매입금액=int(res['tot_pur_amt']),
                총평가금액=int(res['tot_evlt_amt']),
                총평가손익금액=int(res['tot_evlt_pl']),
                총수익률=float(res['tot_prft_rt']),
                추정예탁자산=int(res['prsm_dpst_aset_amt']),
            )
            df = pd.DataFrame(res['acnt_evlt_remn_indv_tot'])
            column_name_to_kor_name_map = {
                "stk_cd": "종목코드",
                "stk_nm": "종목명",
                "evltv_prft": "평가손익",
                "prft_rt": "수익률(%)",
                "pur_pric": "매입가",
                "pred_close_pric": "전일종가",
                "rmnd_qty": "보유수량",
                "trde_able_qty": "매매가능수량",
                "cur_prc": "현재가",
                "pred_buyq": "전일매수수량",
                "pred_sellq": "전일매도수량",
                "tdy_buyq": "금일매수수량",
                "tdy_sellq": "금일매도수량",
                "pur_amt": "매입금액",
                "pur_cmsn": "매입수수료",
                "evlt_amt": "평가금액",
                "sell_cmsn": "평가수수료",
                "tax": "세금",
                "sum_cmsn": "수수료합",
                "poss_rt": "보유비중(%)",
                "crd_tp": "신용구분",
                "crd_tp_nm": "신용구분명",
                "crd_loan_dt": "대출일",
            }
            if len(df) > 0:
                df.rename(columns=column_name_to_kor_name_map, inplace=True)
                df["종목코드"] = df["종목코드"].apply(lambda x: x.replace("_AL", "").replace("A", ""))
                for col in df.columns:
                    if col != "종목코드":
                        df[col] = pd.to_numeric(df[col], errors='ignore')

            log_tr_request(f"계좌평가잔고 요청 성공 - 보유종목 {len(df)}개, 총평가금액: {account_info_dict['총평가금액']:,}원")
            log_trading(f"계좌현황 - 총평가금액: {account_info_dict['총평가금액']:,}원, 총수익률: {account_info_dict['총수익률']:.2f}%")
            return account_info_dict, df, has_next, next_key
        except requests.HTTPError as e:
            error_message = f"HTTP Error: {e}\nResponse Body: {response.text}"
            log_error(f"계좌평가잔고 요청 실패: {error_message}")
            raise requests.HTTPError(error_message) from e

    @log_exceptions
    def reqeust_all_account_info(self):
        log_tr_request("전체 계좌정보 연속 조회 시작")
        params = {
            'qry_tp': '1',
            'dmst_stex_tp': 'KRX',
        }
        dfs = []
        next_key = ''
        has_next = False
        while True:
            time.sleep(1)
            account_info_dict, df, has_next, next_key = self.fn_kt00018(
                data=params,
                cont_yn='Y' if has_next else 'N',
                next_key=next_key,
            )
            dfs.append(df)
            if not has_next:
                break
        all_df = pd.concat(dfs).reset_index(drop=True)
        all_df.reset_index(drop=True, inplace=True)
        log_tr_request("전체 계좌정보 연속 조회 완료")
        return account_info_dict, all_df

    @log_exceptions
    def request_daily_chart_info(
            self,
            stock_code="005930",
            start_date=datetime.datetime.now().strftime("%Y%m%d"),
            max_req_num=10,
    ):
        log_tr_request(f"일봉 차트 정보 요청 - 종목: {stock_code}, 시작일: {start_date}")
        params = {
            'stk_cd': f'{stock_code}_AL',
            'qry_dt': start_date,
            'indc_tp': '0',
        }

        dfs = []
        next_key = ''
        has_next = False
        for _ in range(max_req_num):
            time.sleep(1)
            df, has_next, next_key = self.fn_ka10086(
                data=params,
                cont_yn='Y' if has_next else 'N',
                next_key=next_key,
            )
            dfs.append(df)
            if not has_next:
                break
        all_df = pd.concat(dfs).reset_index(drop=True)
        all_df.sort_values(by=['날짜'], ascending=True, inplace=True)
        all_df.reset_index(drop=True, inplace=True)
        log_tr_request(f"일봉 차트 정보 요청 완료 - 종목: {stock_code}, 데이터: {len(all_df)}건")
        return all_df

    # 시세표성정보요청
    @log_exceptions
    def fn_ka10007(self, data, cont_yn='N', next_key=''):
        종목코드 = data.get('stk_cd', '').replace('_AL', '')
        log_tr_request(f"주식기본정보 요청 - 종목: {종목코드}")
        endpoint = '/api/dostk/mrkcond'
        url = host + endpoint

        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'authorization': f'Bearer {self.token}',
            'cont-yn': cont_yn,
            'next-key': next_key,
            'api-id': 'ka10007',
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            res = response.json()
            basic_info = dict(
                종목명=res['stk_nm'],
                상한가=abs(int(res['upl_pric'])),
                하한가=abs(int(res['lst_pric'])),
                현재가=abs(float(res['cur_prc'])),
            )
            log_tr_request(f"주식기본정보 요청 성공 - {basic_info['종목명']}({종목코드}), 현재가: {basic_info['현재가']:,}원")
            return basic_info
        except requests.HTTPError as e:
            error_message = f"HTTP Error: {e}\nResponse Body: {response.text}"
            log_error(f"주식기본정보 요청 실패 - 종목: {종목코드}, 에러: {error_message}")
            raise requests.HTTPError(error_message) from e

    # 주식 매수주문
    @log_exceptions
    def fn_kt10000(self, data, cont_yn='N', next_key=''):
        종목코드 = data.get('stk_cd', '')
        주문수량 = data.get('ord_qty', '')
        주문가격 = data.get('ord_uv', '')
        log_trading(f"매수주문 요청 - 종목: {종목코드}, 수량: {주문수량}, 가격: {주문가격}")

        endpoint = '/api/dostk/ordr'
        url = host + endpoint

        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'authorization': f'Bearer {self.token}',
            'cont-yn': cont_yn,
            'next-key': next_key,
            'api-id': 'kt10000',
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            order_no = response.json()['ord_no']
            log_trading(f"매수주문 성공 - 종목: {종목코드}, 주문번호: {order_no}")
            return order_no
        except requests.HTTPError as e:
            error_message = f"HTTP Error: {e}\nResponse Body: {response.text}"
            log_error(f"매수주문 실패 - 종목: {종목코드}, 에러: {error_message}")
            raise requests.HTTPError(error_message) from e

    # 주식 매도주문
    @log_exceptions
    def fn_kt10001(self, data, cont_yn='N', next_key=''):
        종목코드 = data.get('stk_cd', '')
        주문수량 = data.get('ord_qty', '')
        주문가격 = data.get('ord_uv', '')
        log_trading(f"매도주문 요청 - 종목: {종목코드}, 수량: {주문수량}, 가격: {주문가격}")

        endpoint = '/api/dostk/ordr'
        url = host + endpoint

        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'authorization': f'Bearer {self.token}',
            'cont-yn': cont_yn,
            'next-key': next_key,
            'api-id': 'kt10001',
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            order_no = response.json()['ord_no']
            log_trading(f"매도주문 성공 - 종목: {종목코드}, 주문번호: {order_no}")
            return order_no
        except requests.HTTPError as e:
            error_message = f"HTTP Error: {e}\nResponse Body: {response.text}"
            log_error(f"매도주문 실패 - 종목: {종목코드}, 에러: {error_message}")
            raise requests.HTTPError(error_message) from e

    # 주식 정정주문
    @log_exceptions
    def fn_kt10002(self, data, cont_yn='N', next_key=''):
        종목코드 = data.get('stk_cd', '')
        원주문번호 = data.get('orig_ord_no', '')
        정정수량 = data.get('mdfy_qty', '')
        정정가격 = data.get('mdfy_uv', '')
        log_trading(f"정정주문 요청 - 종목: {종목코드}, 원주문번호: {원주문번호}, 정정수량: {정정수량}, 정정가격: {정정가격}")

        endpoint = '/api/dostk/ordr'
        url = host + endpoint

        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'authorization': f'Bearer {self.token}',
            'cont-yn': cont_yn,
            'next-key': next_key,
            'api-id': 'kt10002',
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            order_no = response.json()['ord_no']
            log_trading(f"정정주문 성공 - 종목: {종목코드}, 정정주문번호: {order_no}")
            return order_no
        except requests.HTTPError as e:
            error_message = f"HTTP Error: {e}\nResponse Body: {response.text}"
            log_error(f"정정주문 실패 - 종목: {종목코드}, 에러: {error_message}")
            raise requests.HTTPError(error_message) from e

    # 주식 취소주문
    @log_exceptions
    def fn_kt10003(self, data, cont_yn='N', next_key=''):
        종목코드 = data.get('stk_cd', '')
        원주문번호 = data.get('orig_ord_no', '')
        log_trading(f"취소주문 요청 - 종목: {종목코드}, 원주문번호: {원주문번호}")

        endpoint = '/api/dostk/ordr'
        url = host + endpoint

        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'authorization': f'Bearer {self.token}',
            'cont-yn': cont_yn,
            'next-key': next_key,
            'api-id': 'kt10003',
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            order_no = response.json()['ord_no']
            log_trading(f"취소주문 성공 - 종목: {종목코드}, 취소주문번호: {order_no}")
            return order_no
        except requests.HTTPError as e:
            error_message = f"HTTP Error: {e}\nResponse Body: {response.text}"
            log_error(f"취소주문 실패 - 종목: {종목코드}, 에러: {error_message}")
            raise requests.HTTPError(error_message) from e

    # 전일대비등락률상위요청
    @log_exceptions
    def fn_ka10027(self, data, cont_yn='N', next_key=''):
        log_tr_request("등락률 상위 종목 요청")
        endpoint = '/api/dostk/rkinfo'
        url = host + endpoint

        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'authorization': f'Bearer {self.token}',
            'cont-yn': cont_yn,
            'next-key': next_key,
            'api-id': 'ka10027',
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            has_next = response.headers.get('cont-yn') == "Y"
            next_key = response.headers.get('next-key', '')

            res = response.json()
            df = pd.DataFrame(res['pred_pre_flu_rt_upper'])
            column_name_to_kor_name_map = {
                "stk_cls": "종목분류",
                "stk_cd": "종목코드",
                "stk_nm": "종목명",
                "cur_prc": "현재가",
                "pred_pre_sig": "전일대비기호",
                "pred_pre": "전일대비",
                "flu_rt": "등락률",
                "sel_req": "매도잔량",
                "buy_req": "매수잔량",
                "now_trde_qty": "현재거래량",
                "cntr_str": "체결강도",
                "cnt": "횟수",
            }
            df.rename(columns=column_name_to_kor_name_map, inplace=True)
            df["종목코드"] = df["종목코드"].apply(lambda x: x.replace("_AL", "").replace("A", ""))
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='ignore')

            log_tr_request(f"등락률 상위 종목 요청 성공 - 데이터: {len(df)}건")
            return df, has_next, next_key
        except requests.HTTPError as e:
            error_message = f"HTTP Error: {e}\nResponse Body: {response.text}"
            log_error(f"등락률 상위 종목 요청 실패: {error_message}")
            raise requests.HTTPError(error_message) from e

    def request_fluctuation_ranking(self, max_req_num=5):
        log_tr_request("등락률 랭킹 요청 시작")
        params = {
            'mrkt_tp': '000',
            'sort_tp': '1',
            'trde_qty_cnd': '0000',
            'stk_cnd': '0',
            'crd_cnd': '0',
            'updown_incls': '1',
            'pric_cnd': '0',
            'trde_prica_cnd': '0',
            'stex_tp': '3',
        }
        dfs = []
        next_key = ''
        has_next = False
        for _ in range(max_req_num):
            time.sleep(1)
            df, has_next, next_key = self.fn_ka10027(
                data=params,
                cont_yn='Y' if has_next else 'N',
                next_key=next_key,
            )
            dfs.append(df)
            if not has_next:
                break
        all_df = pd.concat(dfs).reset_index(drop=True)
        log_tr_request(f"등락률 랭킹 요청 완료 - 총 데이터: {len(all_df)}건")
        return all_df


if __name__ == '__main__':
    kiwoom_tr = KiwoomTR()
    params = {
        'stk_cd': '005930',
    }
    basic_info_dict = kiwoom_tr.fn_ka10007(params)
    print(basic_info_dict)