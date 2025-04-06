"""
종목 분석 모듈
"""
import asyncio
from typing import Dict, Any, List, Optional, Tuple, Set
import pandas as pd
import numpy as np

from utils.logger import logger
from utils.decorators import async_measure_time
from api.rest_api import KiwoomRestAPI


class StockAnalyzer:
    """종목 분석 클래스"""

    def __init__(self, rest_api: KiwoomRestAPI):
        """
        초기화

        Args:
            rest_api: REST API 인스턴스
        """
        self.rest_api = rest_api

        # 데이터 캐시
        self.stock_info_cache = {}  # 기본 정보 캐시
        self.daily_data_cache = {}  # 일봉 데이터 캐시
        self.ma_data_cache = {}  # 이동평균 데이터 캐시

        # 캐시 만료 시간 (초)
        self.cache_ttl = 300  # 5분
        self.cache_timestamps = {}

        logger.info("종목 분석기 초기화 완료")

    @async_measure_time
    async def get_stock_info(self, stock_code: str) -> Dict[str, Any]:
        """
        종목 기본 정보 조회

        Args:
            stock_code: 종목코드

        Returns:
            종목 정보
        """
        # 캐시에 있고 만료되지 않았으면 캐시 데이터 반환
        if self._check_cache_valid(stock_code, 'stock_info'):
            return self.stock_info_cache.get(stock_code, {})

        try:
            # API 호출
            stock_info = await self.rest_api.get_stock_info(stock_code)

            # 캐시에 저장
            self._update_cache(stock_code, 'stock_info', stock_info)

            return stock_info

        except Exception as e:
            logger.error(f"종목 {stock_code} 정보 조회 중 오류: {str(e)}")
            return {}

    @async_measure_time
    async def get_daily_data(self, stock_code: str, days: int = 20) -> pd.DataFrame:
        """
        일봉 데이터 조회

        Args:
            stock_code: 종목코드
            days: 조회 기간 (일)

        Returns:
            일봉 데이터 DataFrame
        """
        # 캐시 키 생성 (종목코드+기간)
        cache_key = f"{stock_code}_{days}"

        # 캐시에 있고 만료되지 않았으면 캐시 데이터 반환
        if self._check_cache_valid(cache_key, 'daily_data'):
            return self.daily_data_cache.get(cache_key, pd.DataFrame())

        try:
            # API 호출
            daily_data = await self.rest_api.get_daily_chart(stock_code, days)

            # 데이터프레임 변환
            if daily_data:
                df = pd.DataFrame(daily_data)

                # 필요한 컬럼 변환
                if 'stck_bsop_date' in df.columns:
                    df['date'] = pd.to_datetime(df['stck_bsop_date'], format='%Y%m%d')
                if 'stck_clpr' in df.columns:
                    df['close'] = pd.to_numeric(df['stck_clpr'])
                if 'stck_oprc' in df.columns:
                    df['open'] = pd.to_numeric(df['stck_oprc'])
                if 'stck_hgpr' in df.columns:
                    df['high'] = pd.to_numeric(df['stck_hgpr'])
                if 'stck_lwpr' in df.columns:
                    df['low'] = pd.to_numeric(df['stck_lwpr'])
                if 'acml_vol' in df.columns:
                    df['volume'] = pd.to_numeric(df['acml_vol'])

                # 날짜 기준 정렬
                df.sort_values('date', inplace=True)

                # 캐시에 저장
                self._update_cache(cache_key, 'daily_data', df)

                return df
            else:
                return pd.DataFrame()

        except Exception as e:
            logger.error(f"종목 {stock_code} 일봉 데이터 조회 중 오류: {str(e)}")
            return pd.DataFrame()

    @async_measure_time
    async def calculate_moving_averages(self, stock_code: str, ma_periods: List[int] = [5, 20, 60]) -> Dict[
        str, List[float]]:
        """
        이동평균 계산

        Args:
            stock_code: 종목코드
            ma_periods: 이동평균 기간 목록

        Returns:
            이동평균 데이터
        """
        # 캐시 키 생성
        periods_str = '_'.join(map(str, ma_periods))
        cache_key = f"{stock_code}_{periods_str}"

        # 캐시에 있고 만료되지 않았으면 캐시 데이터 반환
        if self._check_cache_valid(cache_key, 'ma_data'):
            return self.ma_data_cache.get(cache_key, {})

        try:
            # 최대 기간 계산
            max_period = max(ma_periods)

            # 일봉 데이터 조회 (여유있게 1.5배)
            daily_df = await self.get_daily_data(stock_code, int(max_period * 1.5))

            if daily_df.empty:
                return {f"ma{period}": [] for period in ma_periods}

            result = {}

            # 각 기간별 이동평균 계산
            for period in ma_periods:
                if 'close' in daily_df.columns and len(daily_df) >= period:
                    ma_values = daily_df['close'].rolling(window=period).mean().dropna().tolist()
                    result[f"ma{period}"] = ma_values
                else:
                    result[f"ma{period}"] = []

            # 캐시에 저장
            self._update_cache(cache_key, 'ma_data', result)

            return result

        except Exception as e:
            logger.error(f"종목 {stock_code} 이동평균 계산 중 오류: {str(e)}")
            return {f"ma{period}": [] for period in ma_periods}

    async def analyze_technical_indicators(self, stock_code: str) -> Dict[str, Any]:
        """
        기술적 지표 분석

        Args:
            stock_code: 종목코드

        Returns:
            기술적 지표 분석 결과
        """
        try:
            # 일봉 데이터 조회 (60일)
            daily_df = await self.get_daily_data(stock_code, 60)

            if daily_df.empty:
                return {}

            result = {}

            # 이동평균 데이터
            ma_data = await self.calculate_moving_averages(stock_code)

            # 골든 크로스/데드 크로스 확인
            if 'ma5' in ma_data and 'ma20' in ma_data and len(ma_data['ma5']) >= 2 and len(ma_data['ma20']) >= 2:
                ma5 = ma_data['ma5']
                ma20 = ma_data['ma20']

                golden_cross = ma5[-2] < ma20[-2] and ma5[-1] > ma20[-1]
                dead_cross = ma5[-2] > ma20[-2] and ma5[-1] < ma20[-1]

                result['golden_cross'] = golden_cross
                result['dead_cross'] = dead_cross

            # RSI 계산 (14일)
            if 'close' in daily_df.columns and len(daily_df) >= 14:
                delta = daily_df['close'].diff()
                gain = delta.where(delta > 0, 0).rolling(window=14).mean()
                loss = -delta.where(delta < 0, 0).rolling(window=14).mean()

                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))

                if not rsi.empty:
                    result['rsi'] = rsi.iloc[-1]

            # MACD 계산
            if 'close' in daily_df.columns and len(daily_df) >= 26:
                exp12 = daily_df['close'].ewm(span=12, adjust=False).mean()
                exp26 = daily_df['close'].ewm(span=26, adjust=False).mean()
                macd = exp12 - exp26
                signal = macd.ewm(span=9, adjust=False).mean()

                if not macd.empty and not signal.empty:
                    result['macd'] = macd.iloc[-1]
                    result['macd_signal'] = signal.iloc[-1]
                    result['macd_histogram'] = macd.iloc[-1] - signal.iloc[-1]

            # 볼린저 밴드 (20일)
            if 'close' in daily_df.columns and len(daily_df) >= 20:
                ma20 = daily_df['close'].rolling(window=20).mean()
                std20 = daily_df['close'].rolling(window=20).std()

                upper_band = ma20 + (std20 * 2)
                lower_band = ma20 - (std20 * 2)

                if not ma20.empty and not upper_band.empty and not lower_band.empty:
                    current_price = daily_df['close'].iloc[-1]
                    result['bollinger_ma20'] = ma20.iloc[-1]
                    result['bollinger_upper'] = upper_band.iloc[-1]
                    result['bollinger_lower'] = lower_band.iloc[-1]

                    # 볼린저 밴드 위치
                    if current_price > upper_band.iloc[-1]:
                        result['bollinger_position'] = 'above'
                    elif current_price < lower_band.iloc[-1]:
                        result['bollinger_position'] = 'below'
                    else:
                        result['bollinger_position'] = 'inside'

                    # 밴드 폭
                    result['bollinger_bandwidth'] = (upper_band.iloc[-1] - lower_band.iloc[-1]) / ma20.iloc[-1] * 100

            return result

        except Exception as e:
            logger.error(f"종목 {stock_code} 기술적 지표 분석 중 오류: {str(e)}")
            return {}

    def _check_cache_valid(self, key: str, cache_type: str) -> bool:
        """
        캐시 유효성 확인

        Args:
            key: 캐시 키
            cache_type: 캐시 유형

        Returns:
            유효성 여부
        """
        cache_key = f"{cache_type}_{key}"

        # 현재 시간
        current_time = asyncio.get_event_loop().time()

        # 캐시에 없으면 False
        if cache_key not in self.cache_timestamps:
            return False

        # 만료 시간 확인
        if current_time - self.cache_timestamps[cache_key] > self.cache_ttl:
            return False

        # 캐시 자료구조에 키가 없으면 False
        if cache_type == 'stock_info' and key not in self.stock_info_cache:
            return False
        elif cache_type == 'daily_data' and key not in self.daily_data_cache:
            return False
        elif cache_type == 'ma_data' and key not in self.ma_data_cache:
            return False

        return True

    def _update_cache(self, key: str, cache_type: str, data: Any) -> None:
        """
        캐시 업데이트

        Args:
            key: 캐시 키
            cache_type: 캐시 유형
            data: 데이터
        """
        # 현재 시간 저장
        self.cache_timestamps[f"{cache_type}_{key}"] = asyncio.get_event_loop().time()

        # 해당 캐시에 데이터 저장
        if cache_type == 'stock_info':
            self.stock_info_cache[key] = data
        elif cache_type == 'daily_data':
            self.daily_data_cache[key] = data
        elif cache_type == 'ma_data':
            self.ma_data_cache[key] = data