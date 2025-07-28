import time
import datetime
import functools
import inspect
import requests
import random

import pandas as pd
from loguru import logger

from config import api_key, api_secret_key, host

def log_exceptions(func):
    """함수 시그니처에 맞게 인자를 자동 조정 + try-except 걸어주는 loguru용 데코레이터 함수"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # 함수가 실제 몇개 positional arguments를 기대하는지 확인
            sig = inspect.signature(func)
            parameters = sig.parameters
            param_len = len(parameters)

            # self 빼고 나머지 인자 개수 확인
            if 'self' in parameters:
                param_len -= 1

            # args를 필요한 만큼만 잘라서 함수 호출
            new_args = args[:param_len + 1] # self + 필요한 만큼

            return func(*new_args, **kwargs)
        except Exception as e:
            logger.exception(f"Exception occurred in {func.__qualname__}")
    return wrapper

######################################################################

class KiwoomTR:
    def __init__(self):
        self.token = self.login()

    @staticmethod
    def login():
        time.sleep(random.random())
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
        response = requests.post(url, headers=headers, json=params)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            # 에러를 response 내용까지 추가해서 출력
            error_message = f"HTTPError: {e}\nResponse Body: {response.text}"
            raise requests.HTTPError(error_message) from e
        token = response.json()['token']
        logger.info(f'접근 토큰 발급: {token}')
        return token

    # 종목 정보 리스트
    @log_exceptions
    def fn_ka10099(self, data, cont_yn='N', next_key=''):
        '''
        1. 키움증권 API 가이드에서 샘플 함수 복사
        2. self, 변수 추가 / token 변수 지우기 / @log_exceptions 추가
        3. host 지우기
        4. response 부분 상황에 맞게 수정
        '''

        # 1. 요청할 API URL
        endpoint = '/api/dostk/stkinfo'
        url = host + endpoint
        # 2. header 데이터
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',  # 컨텐츠타입
            'authorization': f'Bearer {self.token}',  # 접근토큰
            'cont-yn': cont_yn,  # 연속조회여부
            'next-key': next_key,  # 연속조회키
            'api-id': 'ka10099',  # TR명
        }
        # 3. http POST 요청
        response = requests.post(url, headers=headers, json=data)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            # 에러를 response 내용까지 추가해서 출력
            error_message = f"HTTPError: {e}\nResponse Body: {response.text}"
            raise requests.HTTPError(error_message) from e
        return response.json()['list']

    # 일별 주가 요청
    @log_exceptions
    def fn_ka10086(self, data, cont_yn='N', next_key=''):
        '''
        1. 키움증권 API 가이드에서 샘플 함수 복사
        2. self, 변수 추가 / token 변수 지우기 / @log_exceptions 추가
        3. host 지우기
        4. response 부분 상황에 맞게 수정
        '''

        # 1. 요청할 API URL
        endpoint = '/api/dostk/mrkcond'
        url = host + endpoint
        # 2. header 데이터
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',  # 컨텐츠타입
            'authorization': f'Bearer {self.token}',  # 접근토큰
            'cont-yn': cont_yn,  # 연속조회여부
            'next-key': next_key,  # 연속조회키
            'api-id': 'ka10086',  # TR명
        }

        # 3. http POST 요청
        response = requests.post(url, headers=headers, json=data)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            # 에러를 response 내용까지 추가해서 출력
            error_message = f"HTTPError: {e}\nResponse Body: {response.text}"
            raise requests.HTTPError(error_message) from e
        has_next = response.headers.get('cont-yn') == "Y"
        next_key = response.headers.get('next-key', '')
        res = response.json()['daly_stkpc']  # 일별 주가
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
            "flu_rt": "등락율",
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
        return df, has_next, next_key

    # 계좌 평가 잔고 내역 요청
    @log_exceptions
    def fn_kt00018(self, data, cont_yn='N', next_key=''):
        '''
        1. 키움증권 API 가이드에서 샘플 함수 복사
        2. self, 변수 추가 / token 변수 지우기 / @log_exceptions 추가
        3. host 지우기
        4. response 부분 상황에 맞게 수정
        '''

        endpoint = '/api/dostk/acnt'
        url = host + endpoint

        # 2. header 데이터
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',  # 컨텐츠타입
            'authorization': f'Bearer {self.token}',  # 접근토큰
            'cont-yn': cont_yn,  # 연속조회여부
            'next-key': next_key,  # 연속조회키
            'api-id': 'kt00018',  # TR명
        }

        # 3. http POST 요청
        response = requests.post(url, headers=headers, json=data)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            # 에러를 response 내용까지 추가해서 출력
            error_message = f"HTTPError: {e}\nResponse Body: {response.text}"
            raise requests.HTTPError(error_message) from e

        res = response.json()
        has_next = response.headers.get('cont-yn') == "Y"
        next_key = response.headers.get('next-key', '')
        account_info_dict = dict(
            총매입금액=int(res['tot_pur_amt']),
            총평가금액=int(res['tot_evlt_amt']),
            촐평가손익금액=int(res['tot_evlt_pl']),
            총수익률=float(res['tot_prft_rt']),
            추정예탁자산=int(res['prsm_dpst_aset_amt'])
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
            "crd_tp": "신용구분",
            "crd_tp_nm": "신용구분명",
            "crd_loan_dt": "대출일",
        }
        if len(df) > 0:
            df.rename(columns=column_name_to_kor_name_map, inplace=True)
            df["종목코드"] = df["종목코드"].apply(lambda x: x.replace("A", ""))
            for col in df.columns:
                if col != "종목코드":
                    df[col] = pd.to_numeric(df[col], errors='ignore')
        return account_info_dict, df, has_next, next_key

    @log_exceptions
    def request_all_account_info(self):
        # 계좌정보 연속 조회
        params = {
            'qry_tp': '1',  # 조회구분 1:합산, 2:개별
            'dmst_stex_tp': 'KRX',  # 국내거래소구분 KRX:한국거래소,NXT:넥스트트레이드
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
        return account_info_dict, all_df

    # @log_exceptions
    # def request_daily_chart_info(
    #         self,
    #         stock_code="005930",
    #         start_date=datetime.datetime.now().strftime("%Y%m%d"),
    #         max_req_num=10, # 최대 연속조회 요청 수
    # ):
    
#################################################################

    # dfs = []
    # next_key = ''
    # has_next = False
    # for _ in range(max_req_num):
    #     time.sleep(1)
    #     df, has_next, next_key = self.fn_ka10086(
    #         data=params,
    #         cont_yn='Y' if has_next else 'N',
    #         next_key=next_key,
    #     )
    #     dfs.append(df)
    #     if not has_next:
    #         break
    # all_df = pd.concat(dfs).reset_index(drop=True)
    # all_df.sort_values(by=['날짜'], ascending=True, inplace=True)
    # all_df.reset_index(drop=True, inplace=True)
    # return all_df

    # 시세표성정보요청
    @log_exceptions
    def fn_ka10007(self, data, cont_yn='N', next_key=''):
        '''
        1. 키움증권 API 가이드에서 샘플 함수 복사
        2. self, 변수 추가 / token 변수 지우기 / @log_exceptions 추가
        3. host 지우기
        4. response 부분 상황에 맞게 수정
        '''

        # 1. 요청할 API URL
        endpoint = '/api/dostk/mrkcond'
        url = host + endpoint

        # 2. header 데이터
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',  # 컨텐츠타입
            'authorization': f'Bearer {self.token}',  # 접근토큰
            'cont-yn': cont_yn,  # 연속조회여부
            'next-key': next_key,  # 연속조회키
            'api-id': 'ka10007',  # TR명
        }

        # 3. http POST 요청
        response = requests.post(url, headers=headers, json=data)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            # 에러를 response 내용까지 추가해서 출력
            error_message = f"HTTPError: {e}\nResponse Body: {response.text}"
            raise requests.HTTPError(error_message) from e
        res = response.json()
        account_info_dict = dict(
            종목명=res['stk_nm'],
            상한가=abs(int(res['upl_pric'])),
            하한가=abs(int(res['lst_pric'])),
            현재가=abs(float(res['cur_prc'])),
        )
        return account_info_dict

    # 주식 매수주문(kt10000)
    @log_exceptions
    def fn_kt10000(self, data, cont_yn='N', next_key=''):
        '''
        1. 키움증권 API 가이드에서 샘플 함수 복사
        2. self, 변수 추가 / token 변수 지우기 / @log_exceptions 추가
        3. host 지우기
        4. response 부분 상황에 맞게 수정
        '''

        # 1. 요청할 API URL
        endpoint = '/api/dostk/ordr'
        url = host + endpoint

        # 2. header 데이터
        headers = {
            'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
            'authorization': f'Bearer {self.token}', # 접근토큰
            'cont-yn': cont_yn, # 연속조회여부
            'next-key': next_key, # 연속조회키
            'api-id': 'kt10000',  # 주식 매수주문 TR 코드
        }

        # 3. http POST 요청
        response = requests.post(url, headers=headers, json=data)
        
        # 4. 응답 처리
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            # 에러를 response 내용까지 추가해서 출력
            error_message = f"HTTPError: {e}\nResponse Body: {response.text}"
            raise requests.HTTPError(error_message) from e
        return response.json()['ord_no']

    # 주식 매도주문
    @log_exceptions
    def fn_kt10001(self, data, cont_yn='N', next_key=''):
        '''
        1. 키움증권 API 가이드에서 샘플 함수 복사
        2. self, 변수 추가 / token 변수 지우기 / @log_exceptions 추가
        3. host 지우기
        4. response 부분 상황에 맞게 수정
        '''

        # 1. 요청할 API URL
        endpoint = '/api/dostk/ordr'
        url = host + endpoint

        # 2. header 데이터
        headers = {
            'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
            'authorization': f'Bearer {self.token}', # 접근토큰
            'cont-yn': cont_yn, # 연속조회여부
            'next-key': next_key, # 연속조회키
            'api-id': 'kt10001',  # 주식 매도주문 TR 코드
        }

        # 3. http POST 요청
        response = requests.post(url, headers=headers, json=data)

        # 4. 응답 처리
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            # 에러를 response 내용까지 추가해서 출력
            error_message = f"HTTPError: {e}\nResponse Body: {response.text}"
            raise requests.HTTPError(error_message) from e
        return response.json()['ord_no']

    # 주식 정정주문
    @log_exceptions
    def fn_kt10002(self, data, cont_yn='N', next_key=''):
        '''
        1. 키움증권 API 가이드에서 샘플 함수 복사
        2. self, 변수 추가 / token 변수 지우기 / @log_exceptions 추가
        3. host 지우기
        4. response 부분 상황에 맞게 수정
        '''

        # 1. 요청할 API URL
        endpoint = '/api/dostk/ordr'
        url = host + endpoint

        # 2. header 데이터
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',  # 컨텐츠타입
            'authorization': f'Bearer {self.token}',  # 접근토큰
            'cont-yn': cont_yn,  # 연속조회여부
            'next-key': next_key,  # 연속조회키
            'api-id': 'kt10002',  # TR명
        }

        # 3. http POST 요청
        response = requests.post(url, headers=headers, json=data)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            # 에러를 response 내용까지 추가해서 출력
            error_message = f"HTTPError: {e}\nResponse Body: {response.text}"
            raise requests.HTTPError(error_message) from e
        return response.json()['ord_no']

    # 주식 취소주문
    @log_exceptions
    def fn_kt10003(self, data, cont_yn='N', next_key=''):
        '''
        1. 키움증권 API 가이드에서 샘플 함수 복사
        2. self, 변수 추가 / token 변수 지우기 / @log_exceptions 추가
        3. host 지우기
        4. response 부분 상황에 맞게 수정
        '''

        # 1. 요청할 API URL
        endpoint = '/api/dostk/ordr'
        url = host + endpoint

        # 2. header 데이터
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',  # 컨텐츠타입
            'authorization': f'Bearer {self.token}',  # 접근토큰
            'cont-yn': cont_yn,  # 연속조회여부
            'next-key': next_key,  # 연속조회키
            'api-id': 'kt10003',  # TR명
        }

        # 3. http POST 요청
        response = requests.post(url, headers=headers, json=data)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            # 에러를 response 내용까지 추가해서 출력
            error_message = f"HTTPError: {e}\nResponse Body: {response.text}"
            raise requests.HTTPError(error_message) from e
        return response.json()['ord_no']


    # 전일대비등락률상위요청(ka10027)
    @log_exceptions
    def fn_ka10027(self, data, cont_yn='N', next_key=''):
        '''
        1. 키움증권 API 가이드에서 샘플 함수 복사
        2. self, 변수 추가 / token 변수 지우기 / @log_exceptions 추가
        3. host 지우기
        4. response 부분 상황에 맞게 수정
        '''

        # 1. 요청할 API URL
        endpoint = '/api/dostk/rkinfo'
        url = host + endpoint

        # 2. header 데이터
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',  # 컨텐츠타입
            'authorization': f'Bearer {self.token}',  # 접근토큰
            'cont-yn': cont_yn,  # 연속조회여부
            'next-key': next_key,  # 연속조회키
            'api-id': 'ka10027',  # TR명
        }

        # 3. http POST 요청
        response = requests.post(url, headers=headers, json=data)
        
        # 4. 응답 처리
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            # HTTP 에러 발생 시 상세 정보 포함하여 예외 발생
            error_message = f"HTTP Error: {e}"
            if response.text:
                error_message += f"\nResponse: {response.text}"
            raise requests.HTTPError(error_message) from e
        has_next = response.headers.get('cont-yn') == "Y"
        next_key = response.headers.get('next-key', '')

        res = response.json()
        df = pd.DataFrame(res['pred_pre_flu_rt_upper'])
        column_name_to_kor_name_map = {
            "stk_cls": "종목분류",
            "stk_cd": "종목코드",
            "stk_nm": "종목명",
            "cur_price": "현재가",
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
        return df, has_next, next_key


    def request_fluctuation_ranking(self, max_req_num=5): # 연속 조회 함수
        params = {
            'mrkt_tp': '000', # 시장구분 000:전체, 001:코스피, 101:코스닥
            'sort_tp': '1', # 정렬구분 1:상승률, 2:상승폭, 3:하락률, 4:하락폭, 5:보합
            'trde_qty_cnd': '0000',
            # 거래량조건 0000:전체조회, 0010:만주이상, 0050:5만주이상, 0100:10만주이상, 0150:15만주이상, 0200:20만주이상, 0300:30만주이상, 0500:50만주이상, 1000:백만주이상
            'stk_cnd': '0',
            # 종목조건 0:전체조회, 1:관리종목제외, 4:우선주+관리주제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기, 11:정리매매종목제외, 12:증50만보기, 13:증60만보기, 14:ETF제외, 15:스펙제외, 16:ETF+ETN제외
            'crd_cnd': '0', # 신용조건 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 9:신용융자전체
            'updown_incls': '1', # 상하한포함 0:불 포함, 1:포함
            'pric_cnd': '0', # 가격조건 0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~5천원, 4:5천원~1만원, 5:1만원이상, 8:1천원이상, 10: 1만원미만
            'trde_prica_cnd': '0',
            # 거래대금조건 0:전체조회, 3:3천만원이상, 5:5천만원이상, 10:1억원이상, 30:3억원이상, 50:5억원이상, 100:10억원이상, 300:30억원이상, 500:50억원이상, 1000:100억원이상, 3000:300억원이상, 5000:500억원이상
            'stex_tp': '3', # 거래소구분 1:KRX, 2:NXT 3.통합
        }
        dfs = []
        next_key = ''
        has_next = False
        for i in range(1, max_req_num):
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
        return all_df



if __name__ == '__main__':
    kiwoom_tr = KiwoomTR()

    # all_df = kiwoom_tr.request_fluctuation_ranking() # 전일대비등락률상위요청
    # print(all_df.to_string())

    params = {
        'stk_cd': '005930_AL',  # 종목코드 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
        'qry_dt': datetime.datetime.now().strftime('%Y%m%d'),  # 조회일자 YYYYMMDD
        'indc_tp': '0',  # 표시구분 0:수량, 1:금액(백만원)
    }
    df, has_next, next_key = kiwoom_tr.fn_ka10086(data=params)
    print(df.to_string())


    # params = {
    #     'stk_cd': '005930',  # 종목코드 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
    # }
    # basic_info_dict = kiwoom_tr.fn_ka10007(params)
    # print(basic_info_dict)