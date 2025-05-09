# data/processor.py
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any
from datetime import datetime, timedelta


class DataProcessor:
    """데이터 전처리 클래스"""
    
    def process_stock_daily_price(self, df: pd.DataFrame) -> pd.DataFrame:
        """일별 주가 데이터 전처리
        
        Args:
            df: 원본 주가 데이터
            
        Returns:
            pd.DataFrame: 전처리된 주가 데이터
        """
        if df.empty:
            return df
            
        # 데이터 타입 변환
        if '일자' in df.columns:
            df['일자'] = pd.to_datetime(df['일자'])
            
        numeric_columns = ['시가', '고가', '저가', '종가', '거래량', '거래대금']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
        # 결측치 처리
        df = df.dropna(subset=['종가'])
        
        # 날짜 기준 정렬
        df = df.sort_values('일자')
        
        # 이동평균선 계산
        if '종가' in df.columns:
            df['MA5'] = df['종가'].rolling(window=5).mean()
            df['MA20'] = df['종가'].rolling(window=20).mean()
            df['MA60'] = df['종가'].rolling(window=60).mean()
            df['MA120'] = df['종가'].rolling(window=120).mean()
            
        # 일간 수익률 계산
        if '종가' in df.columns:
            df['일간수익률'] = df['종가'].pct_change()
            
        # 거래대금 계산 (거래량 * 종가)
        if '거래량' in df.columns and '종가' in df.columns and '거래대금' not in df.columns:
            df['거래대금'] = df['거래량'] * df['종가']
            
        return df
        
    def process_financial_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """재무제표 데이터 전처리
        
        Args:
            df: 원본 재무제표 데이터
            
        Returns:
            pd.DataFrame: 전처리된 재무제표 데이터
        """
        if df.empty:
            return df
            
        # 데이터 타입 변환
        numeric_columns = df.select_dtypes(include=['object']).columns
        for col in numeric_columns:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except:
                pass
                
        # 결측치 처리
        df = df.fillna(0)
        
        # 파생 지표 계산
        if '당기순이익' in df.columns and '자본총계' in df.columns:
            df['ROE'] = df['당기순이익'] / df['자본총계'] * 100
            
        if '당기순이익' in df.columns and '자산총계' in df.columns:
            df['ROA'] = df['당기순이익'] / df['자산총계'] * 100
            
        if '영업이익' in df.columns and '매출액' in df.columns:
            df['영업이익률'] = df['영업이익'] / df['매출액'] * 100
            
        if '당기순이익' in df.columns and '매출액' in df.columns:
            df['순이익률'] = df['당기순이익'] / df['매출액'] * 100
            
        if '유동자산' in df.columns and '유동부채' in df.columns:
            df['유동비율'] = df['유동자산'] / df['유동부채'] * 100
            
        if '부채총계' in df.columns and '자산총계' in df.columns:
            df['부채비율'] = df['부채총계'] / df['자산총계'] * 100
            
        return df
        
    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """기술적 지표 계산
        
        Args:
            df: 원본 주가 데이터
            
        Returns:
            pd.DataFrame: 기술적 지표가 추가된 데이터
        """
        if df.empty or '종가' not in df.columns:
            return df
            
        # RSI 계산 (14일)
        delta = df['종가'].diff()
        gain = delta.mask(delta < 0, 0)
        loss = -delta.mask(delta > 0, 0)
        
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        
        rs = avg_gain / avg_loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # 볼린저 밴드 (20일)
        df['MA20'] = df['종가'].rolling(window=20).mean()
        std_dev = df['종가'].rolling(window=20).std()
        df['UpperBand'] = df['MA20'] + (std_dev * 2)
        df['LowerBand'] = df['MA20'] - (std_dev * 2)
        
        # MACD (12, 26, 9)
        ema12 = df['종가'].ewm(span=12, adjust=False).mean()
        ema26 = df['종가'].ewm(span=26, adjust=False).mean()
        df['MACD'] = ema12 - ema26
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD'] - df['Signal']
        
        # 스토캐스틱 (14, 3, 3)
        low_14 = df['저가'].rolling(window=14).min()
        high_14 = df['고가'].rolling(window=14).max()
        df['%K'] = ((df['종가'] - low_14) / (high_14 - low_14)) * 100
        df['%D'] = df['%K'].rolling(window=3).mean()
        
        return df
        
    def merge_datasets(self, price_data: pd.DataFrame, financial_data: pd.DataFrame, on: str = '종목코드') -> pd.DataFrame:
        """가격 데이터와 재무 데이터 병합
        
        Args:
            price_data: 가격 데이터
            financial_data: 재무 데이터
            on: 병합 기준 컬럼
            
        Returns:
            pd.DataFrame: 병합된 데이터
        """
        if price_data.empty or financial_data.empty:
            return pd.DataFrame()
            
        # 최신 가격 데이터만 사용
        if '일자' in price_data.columns:
            latest_prices = price_data.sort_values('일자').groupby(on).last().reset_index()
        else:
            latest_prices = price_data
            
        # 데이터 병합
        merged_data = pd.merge(latest_prices, financial_data, on=on, how='inner')
        
        return merged_data