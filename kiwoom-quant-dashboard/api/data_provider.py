"""
키움증권 REST API에서 각종 데이터를 가져오는 데이터 제공자 클래스
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any
from datetime import datetime, timedelta
import threading
import time
import logging

from api.kiwoom_api import KiwoomAPI
from utils.date_utils import format_date, get_previous_business_day

logger = logging.getLogger(__name__)


class DataProvider:
    """키움증권 API를 통한 데이터 제공 클래스"""
    
    def __init__(self, api_client: Optional[KiwoomAPI] = None):
        """데이터 제공자 초기화
        
        Args:
            api_client: KiwoomAPI 인스턴스 (기본값: 새 인스턴스 생성)
        """
        self.api = api_client if api_client else KiwoomAPI()
        self._lock = threading.Lock()
        self._cache = {}  # 데이터 캐싱
        self._cache_expiry = {}  # 캐시 만료 시간
        
    def get_market_code_list(self, market_type: str = "0", use_cache: bool = True, 
                           cache_seconds: int = 86400) -> pd.DataFrame:
        """시장별 종목 코드 리스트 조회
        
        Args:
            market_type: 시장 구분 코드 ('0':코스피, '10':코스닥, '3':ELW, '8':ETF, '50':KONEX)
            use_cache: 캐시 사용 여부
            cache_seconds: 캐시 유효 시간(초)
            
        Returns:
            pd.DataFrame: 종목 코드 데이터프레임
        """
        cache_key = f"market_code_list_{market_type}"
        
        # 캐시 확인
        if use_cache and cache_key in self._cache:
            cache_time = self._cache_expiry.get(cache_key, 0)
            if time.time() < cache_time:
                logger.debug(f"캐시에서 시장 코드 목록 가져옴: {market_type}")
                return self._cache[cache_key].copy()
        
        try:
            with self._lock:
                response = self.api.get_market_code_list(market_type)
            
            if response and 'data' in response:
                df = pd.DataFrame(response['data'])
                
                # 캐시 저장
                if use_cache:
                    self._cache[cache_key] = df.copy()
                    self._cache_expiry[cache_key] = time.time() + cache_seconds
                
                return df
            else:
                logger.warning(f"시장 코드 목록 조회 실패: {market_type}")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"시장 코드 목록 조회 중 오류: {e}")
            return pd.DataFrame()
    
    def get_stock_info(self, code: str, use_cache: bool = True, 
                     cache_seconds: int = 86400) -> Dict[str, Any]:
        """종목 기본 정보 조회
        
        Args:
            code: 종목 코드
            use_cache: 캐시 사용 여부
            cache_seconds: 캐시 유효 시간(초)
            
        Returns:
            Dict[str, Any]: 종목 기본 정보
        """
        cache_key = f"stock_info_{code}"
        
        # 캐시 확인
        if use_cache and cache_key in self._cache:
            cache_time = self._cache_expiry.get(cache_key, 0)
            if time.time() < cache_time:
                logger.debug(f"캐시에서 종목 정보 가져옴: {code}")
                return self._cache[cache_key].copy()
        
        try:
            with self._lock:
                response = self.api.get_stock_info(code)
            
            if response and 'data' in response:
                stock_info = response['data']
                
                # 캐시 저장
                if use_cache:
                    self._cache[cache_key] = stock_info.copy()
                    self._cache_expiry[cache_key] = time.time() + cache_seconds
                
                return stock_info
            else:
                logger.warning(f"종목 정보 조회 실패: {code}")
                return {}
                
        except Exception as e:
            logger.error(f"종목 정보 조회 중 오류: {e}")
            return {}
    
    def get_stock_daily_chart(self, code: str, from_date: str, to_date: Optional[str] = None,
                            use_cache: bool = True, cache_seconds: int = 3600) -> pd.DataFrame:
        """일별 주가 데이터 조회
        
        Args:
            code: 종목 코드
            from_date: 조회 시작일 (YYYYMMDD)
            to_date: 조회 종료일 (YYYYMMDD, 기본값: 현재 날짜)
            use_cache: 캐시 사용 여부
            cache_seconds: 캐시 유효 시간(초)
            
        Returns:
            pd.DataFrame: 일별 주가 데이터프레임
        """
        if to_date is None:
            to_date = format_date(datetime.now())
            
        cache_key = f"daily_chart_{code}_{from_date}_{to_date}"
        
        # 캐시 확인
        if use_cache and cache_key in self._cache:
            cache_time = self._cache_expiry.get(cache_key, 0)
            if time.time() < cache_time:
                logger.debug(f"캐시에서 일봉 데이터 가져옴: {code}")
                return self._cache[cache_key].copy()
        
        try:
            with self._lock:
                response = self.api.get_stock_daily_chart(code, from_date, to_date)
                time.sleep(0.1)  # API 호출 제한 방지
            
            if response and 'data' in response:
                df = pd.DataFrame(response['data'])
                
                # 데이터 전처리
                if not df.empty:
                    df['일자'] = pd.to_datetime(df['일자'])
                    numeric_columns = ['시가', '고가', '저가', '종가', '거래량']
                    for col in numeric_columns:
                        if col in df.columns:
                            df[col] = pd.to_numeric(df[col])
                            
                    df = df.sort_values('일자')
                
                # 캐시 저장
                if use_cache:
                    self._cache[cache_key] = df.copy()
                    self._cache_expiry[cache_key] = time.time() + cache_seconds
                
                return df
            else:
                logger.warning(f"일봉 데이터 조회 실패: {code}")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"일봉 데이터 조회 중 오류: {e}")
            return pd.DataFrame()
    
    def get_multiple_daily_charts(self, codes: List[str], from_date: str, to_date: Optional[str] = None,
                                use_cache: bool = True, cache_seconds: int = 3600) -> Dict[str, pd.DataFrame]:
        """여러 종목의 일별 주가 데이터 조회
        
        Args:
            codes: 종목 코드 리스트
            from_date: 조회 시작일 (YYYYMMDD)
            to_date: 조회 종료일 (YYYYMMDD, 기본값: 현재 날짜)
            use_cache: 캐시 사용 여부
            cache_seconds: 캐시 유효 시간(초)
            
        Returns:
            Dict[str, pd.DataFrame]: 종목별 일봉 데이터프레임 딕셔너리
        """
        result = {}
        
        for code in codes:
            df = self.get_stock_daily_chart(code, from_date, to_date, use_cache, cache_seconds)
            result[code] = df
            
            # API 과부하 방지
            time.sleep(0.2)
        
        return result
    
    def get_current_price(self, codes: Union[str, List[str]], use_cache: bool = False) -> pd.DataFrame:
        """현재가 조회
        
        Args:
            codes: 종목 코드 또는 종목 코드 리스트
            use_cache: 캐시 사용 여부 (실시간 데이터이므로 기본값은 False)
            
        Returns:
            pd.DataFrame: 현재가 데이터프레임
        """
        if isinstance(codes, str):
            codes_str = codes
            cache_key = f"current_price_{codes}"
        else:
            codes_str = ",".join(codes)
            cache_key = f"current_price_{','.join(sorted(codes))}"
        
        # 캐시 확인
        if use_cache and cache_key in self._cache:
            cache_time = self._cache_expiry.get(cache_key, 0)
            if time.time() < cache_time:
                logger.debug(f"캐시에서 현재가 정보 가져옴: {codes_str}")
                return self._cache[cache_key].copy()
        
        try:
            with self._lock:
                response = self.api.get_current_price(codes)
            
            if response and 'data' in response:
                df = pd.DataFrame(response['data'])
                
                # 캐시 저장 (매우 짧은 시간만 캐싱)
                if use_cache:
                    self._cache[cache_key] = df.copy()
                    self._cache_expiry[cache_key] = time.time() + 10  # 10초만 캐싱
                
                return df
            else:
                logger.warning(f"현재가 조회 실패: {codes_str}")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"현재가 조회 중 오류: {e}")
            return pd.DataFrame()
    
    def get_financial_statement(self, code: str, year: Optional[str] = None, quarter: Optional[str] = None,
                              use_cache: bool = True, cache_seconds: int = 86400) -> pd.DataFrame:
        """재무제표 조회
        
        Args:
            code: 종목 코드
            year: 조회 연도 (YYYY)
            quarter: 조회 분기 ('1', '2', '3', '4')
            use_cache: 캐시 사용 여부
            cache_seconds: 캐시 유효 시간(초)
            
        Returns:
            pd.DataFrame: 재무제표 데이터프레임
        """
        cache_key = f"financial_{code}"
        if year:
            cache_key += f"_{year}"
        if quarter:
            cache_key += f"_{quarter}"
        
        # 캐시 확인
        if use_cache and cache_key in self._cache:
            cache_time = self._cache_expiry.get(cache_key, 0)
            if time.time() < cache_time:
                logger.debug(f"캐시에서 재무제표 가져옴: {code}")
                return self._cache[cache_key].copy()
        
        try:
            with self._lock:
                response = self.api.get_financial_statement(code, year, quarter)
                time.sleep(0.1)  # API 호출 제한 방지
            
            if response and 'data' in response:
                df = pd.DataFrame(response['data'])
                
                # 캐시 저장
                if use_cache:
                    self._cache[cache_key] = df.copy()
                    self._cache_expiry[cache_key] = time.time() + cache_seconds
                
                return df
            else:
                logger.warning(f"재무제표 조회 실패: {code}")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"재무제표 조회 중 오류: {e}")
            return pd.DataFrame()
    
    def get_multiple_financial_statements(self, codes: List[str], year: Optional[str] = None, 
                                       quarter: Optional[str] = None, use_cache: bool = True, 
                                       cache_seconds: int = 86400) -> Dict[str, pd.DataFrame]:
        """여러 종목의 재무제표 조회
        
        Args:
            codes: 종목 코드 리스트
            year: 조회 연도 (YYYY)
            quarter: 조회 분기 ('1', '2', '3', '4')
            use_cache: 캐시 사용 여부
            cache_seconds: 캐시 유효 시간(초)
            
        Returns:
            Dict[str, pd.DataFrame]: 종목별 재무제표 데이터프레임 딕셔너리
        """
        result = {}
        
        for code in codes:
            df = self.get_financial_statement(code, year, quarter, use_cache, cache_seconds)
            result[code] = df
            
            # API 과부하 방지
            time.sleep(0.2)
        
        return result
    
    def get_market_index(self, index_code: str, from_date: str, to_date: Optional[str] = None,
                       use_cache: bool = True, cache_seconds: int = 3600) -> pd.DataFrame:
        """시장 지수 조회
        
        Args:
            index_code: 지수 코드 (ex: 'KS11': KOSPI, 'KQ11': KOSDAQ)
            from_date: 조회 시작일 (YYYYMMDD)
            to_date: 조회 종료일 (YYYYMMDD, 기본값: 현재 날짜)
            use_cache: 캐시 사용 여부
            cache_seconds: 캐시 유효 시간(초)
            
        Returns:
            pd.DataFrame: 지수 데이터프레임
        """
        if to_date is None:
            to_date = format_date(datetime.now())
            
        cache_key = f"market_index_{index_code}_{from_date}_{to_date}"
        
        # 캐시 확인
        if use_cache and cache_key in self._cache:
            cache_time = self._cache_expiry.get(cache_key, 0)
            if time.time() < cache_time:
                logger.debug(f"캐시에서 지수 데이터 가져옴: {index_code}")
                return self._cache[cache_key].copy()
        
        try:
            with self._lock:
                response = self.api.get_market_index(index_code, from_date, to_date)
                time.sleep(0.1)  # API 호출 제한 방지
            
            if response and 'data' in response:
                df = pd.DataFrame(response['data'])
                
                # 데이터 전처리
                if not df.empty:
                    df['일자'] = pd.to_datetime(df['일자'])
                    numeric_columns = ['시가', '고가', '저가', '종가', '거래량']
                    for col in numeric_columns:
                        if col in df.columns:
                            df[col] = pd.to_numeric(df[col])
                            
                    df = df.sort_values('일자')
                
                # 캐시 저장
                if use_cache:
                    self._cache[cache_key] = df.copy()
                    self._cache_expiry[cache_key] = time.time() + cache_seconds
                
                return df
            else:
                logger.warning(f"지수 데이터 조회 실패: {index_code}")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"지수 데이터 조회 중 오류: {e}")
            return pd.DataFrame()
    
    def get_account_balance(self, use_cache: bool = False) -> Dict[str, Any]:
        """계좌 잔고 조회
        
        Args:
            use_cache: 캐시 사용 여부 (실시간 데이터이므로 기본값은 False)
            
        Returns:
            Dict[str, Any]: 계좌 잔고 정보
        """
        cache_key = "account_balance"
        
        # 캐시 확인
        if use_cache and cache_key in self._cache:
            cache_time = self._cache_expiry.get(cache_key, 0)
            if time.time() < cache_time:
                logger.debug("캐시에서 계좌 잔고 가져옴")
                return self._cache[cache_key].copy()
        
        try:
            with self._lock:
                response = self.api.get_account_balance()
            
            if response and 'data' in response:
                account_data = response['data']
                
                # 캐시 저장 (매우 짧은 시간만 캐싱)
                if use_cache:
                    self._cache[cache_key] = account_data.copy()
                    self._cache_expiry[cache_key] = time.time() + 10  # 10초만 캐싱
                
                return account_data
            else:
                logger.warning("계좌 잔고 조회 실패")
                return {}
                
        except Exception as e:
            logger.error(f"계좌 잔고 조회 중 오류: {e}")
            return {}
    
    def get_order_history(self, from_date: str, to_date: Optional[str] = None,
                        use_cache: bool = True, cache_seconds: int = 3600) -> pd.DataFrame:
        """주문 내역 조회
        
        Args:
            from_date: 조회 시작일 (YYYYMMDD)
            to_date: 조회 종료일 (YYYYMMDD, 기본값: 현재 날짜)
            use_cache: 캐시 사용 여부
            cache_seconds: 캐시 유효 시간(초)
            
        Returns:
            pd.DataFrame: 주문 내역 데이터프레임
        """
        if to_date is None:
            to_date = format_date(datetime.now())
            
        cache_key = f"order_history_{from_date}_{to_date}"
        
        # 캐시 확인
        if use_cache and cache_key in self._cache:
            cache_time = self._cache_expiry.get(cache_key, 0)
            if time.time() < cache_time:
                logger.debug("캐시에서 주문 내역 가져옴")
                return self._cache[cache_key].copy()
        
        try:
            with self._lock:
                response = self.api.get_order_history(from_date, to_date)
            
            if response and 'data' in response:
                df = pd.DataFrame(response['data'])
                
                # 데이터 전처리
                if not df.empty and '주문일시' in df.columns:
                    df['주문일시'] = pd.to_datetime(df['주문일시'])
                    df = df.sort_values('주문일시', ascending=False)
                
                # 캐시 저장
                if use_cache:
                    self._cache[cache_key] = df.copy()
                    self._cache_expiry[cache_key] = time.time() + cache_seconds
                
                return df
            else:
                logger.warning("주문 내역 조회 실패")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"주문 내역 조회 중 오류: {e}")
            return pd.DataFrame()
    
    def place_order(self, code: str, order_type: str, quantity: int, 
                  price: Optional[int] = None) -> Dict[str, Any]:
        """주식 주문
        
        Args:
            code: 종목 코드
            order_type: 주문 구분 ('1':매도, '2':매수)
            quantity: 주문 수량
            price: 주문 가격 (지정가 주문일 경우)
            
        Returns:
            Dict[str, Any]: 주문 결과
        """
        try:
            with self._lock:
                response = self.api.place_order(code, order_type, quantity, price)
            
            if response and 'data' in response:
                return response['data']
            else:
                logger.warning(f"주문 실패: {code}, {order_type}, {quantity}, {price}")
                return {}
                
        except Exception as e:
            logger.error(f"주문 중 오류: {e}")
            return {}
    
    def clear_cache(self, key: Optional[str] = None):
        """캐시 초기화
        
        Args:
            key: 초기화할 캐시 키 (None인 경우 모든 캐시 초기화)
        """
        if key is None:
            self._cache.clear()
            self._cache_expiry.clear()
            logger.debug("모든 캐시 초기화")
        elif key in self._cache:
            del self._cache[key]
            if key in self._cache_expiry:
                del self._cache_expiry[key]
            logger.debug(f"캐시 초기화: {key}")