# data/fetcher.py
from api.kiwoom_api import KiwoomAPI
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any
import threading
import time

class DataFetcher:
    """데이터 수집 클래스"""
    
    def __init__(self, api_client: Optional[KiwoomAPI] = None):
        """데이터 수집기 초기화
        
        Args:
            api_client: KiwoomAPI 인스턴스 (기본값: 새 인스턴스 생성)
        """
        self.api = api_client if api_client else KiwoomAPI()
        self._lock = threading.Lock()
        
    def get_market_codes(self, market_type: str = "0") -> pd.DataFrame:
        """시장별 종목 코드 리스트 조회
        
        Args:
            market_type: 시장 구분 코드 ('0':코스피, '10':코스닥, '3':ELW, '8':ETF, '50':KONEX)
            
        Returns:
            pd.DataFrame: 종목 코드 데이터프레임
        """
        with self._lock:
            response = self.api.get_market_code_list(market_type)
            
        if response and 'data' in response:
            df = pd.DataFrame(response['data'])
            return df
        else:
            return pd.DataFrame()
    
    def get_daily_price(self, code: str, days: int = 365) -> pd.DataFrame:
        """일별 주가 데이터 조회
        
        Args:
            code: 종목 코드
            days: 조회할 일 수 (기본값: 365일)
            
        Returns:
            pd.DataFrame: 일별 주가 데이터프레임
        """
        today = datetime.now()
        from_date = (today - timedelta(days=days)).strftime("%Y%m%d")
        to_date = today.strftime("%Y%m%d")
        
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
                
            return df
        else:
            return pd.DataFrame()
    
    def get_multiple_daily_price(self, codes: List[str], days: int = 365) -> Dict[str, pd.DataFrame]:
        """여러 종목의 일별 주가 데이터 조회
        
        Args:
            codes: 종목 코드 리스트
            days: 조회할 일 수 (기본값: 365일)
            
        Returns:
            Dict[str, pd.DataFrame]: 종목코드를 키로, 데이터프레임을 값으로 하는 딕셔너리
        """
        result = {}
        
        for code in codes:
            df = self.get_daily_price(code, days)
            result[code] = df
            
        return result
    
    def get_financial_data(self, code: str, year: Optional[str] = None, quarter: Optional[str] = None) -> pd.DataFrame:
        """재무제표 데이터 조회
        
        Args:
            code: 종목 코드
            year: 조회 연도 (YYYY)
            quarter: 조회 분기 ('1', '2', '3', '4')
            
        Returns:
            pd.DataFrame: 재무제표 데이터프레임
        """
        with self._lock:
            response = self.api.get_financial_statement(code, year, quarter)
            time.sleep(0.1)  # API 호출 제한 방지
            
        if response and 'data' in response:
            df = pd.DataFrame(response['data'])
            return df
        else:
            return pd.DataFrame()
    
    def get_current_prices(self, codes: Union[str, List[str]]) -> pd.DataFrame:
        """현재가 조회
        
        Args:
            codes: 종목 코드 또는 종목 코드 리스트
            
        Returns:
            pd.DataFrame: 현재가 데이터프레임
        """
        with self._lock:
            response = self.api.get_current_price(codes)
            
        if response and 'data' in response:
            df = pd.DataFrame(response['data'])
            return df
        else:
            return pd.DataFrame()