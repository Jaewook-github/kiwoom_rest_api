"""
이동평균 교차 매매 전략 모듈
"""
from typing import Dict, Any, List, Optional, Tuple
import asyncio

from utils.logger import logger
from strategies.base_strategy import BaseStrategy
from api.rest_api import KiwoomRestAPI


class MACrossStrategy(BaseStrategy):
    """이동평균 교차 기반 매매 전략 클래스"""

    def __init__(self, rest_api: KiwoomRestAPI, name: str = "이동평균교차전략"):
        """
        초기화

        Args:
            rest_api: REST API 인스턴스
            name: 전략 이름
        """
        super().__init__(name)
        self.rest_api = rest_api

        # 이동평균 설정
        self.short_ma = 5  # 단기 이동평균 기간
        self.long_ma = 20  # 장기 이동평균 기간

        # 이동평균 데이터 캐시
        self.ma_cache: Dict[str, Dict[str, List[float]]] = {}
        self.cache_ttl = 300  # 캐시 유효시간 (초)
        self.cache_timestamps: Dict[str, float] = {}

        logger.info(f"이동평균 교차 전략 초기화 - 단기: {self.short_ma}일, 장기: {self.long_ma}일")

    async def get_moving_averages(self, stock_code: str) -> Dict[str, List[float]]:
        """
        종목의 이동평균 데이터 조회

        Args:
            stock_code: 종목코드

        Returns:
            이동평균 데이터
        """
        # 캐시 확인
        current_time = asyncio.get_event_loop().time()

        if (stock_code in self.ma_cache and stock_code in self.cache_timestamps and
                current_time - self.cache_timestamps[stock_code] < self.cache_ttl):
            # 캐시 유효
            return self.ma_cache[stock_code]

        try:
            # 일봉 데이터 요청
            daily_data = await self._get_daily_data(stock_code)

            if not daily_data:
                return {'ma5': [], 'ma20': []}

            # 종가 추출
            prices = [candle.get('stck_clpr', 0) for candle in daily_data]

            # 이동평균 계산
            ma5 = self._calculate_ma(prices, self.short_ma)
            ma20 = self._calculate_ma(prices, self.long_ma)

            # 캐시 저장
            self.ma_cache[stock_code] = {'ma5': ma5, 'ma20': ma20}
            self.cache_timestamps[stock_code] = current_time

            return self.ma_cache[stock_code]

        except Exception as e:
            logger.exception(f"이동평균 데이터 조회 중 오류: {str(e)}")
            return {'ma5': [], 'ma20': []}

    async def _get_daily_data(self, stock_code: str) -> List[Dict[str, Any]]:
        """
        일봉 데이터 조회

        Args:
            stock_code: 종목코드

        Returns:
            일봉 데이터 목록
        """
        try:
            # 일봉 데이터 조회 (30일)
            daily_data = await self.rest_api.get_daily_chart(stock_code, 30)

            if not daily_data:
                logger.warning(f"종목 {stock_code} 일봉 데이터 없음")
            else:
                logger.debug(f"종목 {stock_code} 일봉 데이터 조회 성공: {len(daily_data)}건")

            return daily_data

        except Exception as e:
            logger.exception(f"일봉 데이터 조회 중 오류: {str(e)}")
            return []

        except Exception as e:
            logger.exception(f"일봉 데이터 조회 중 오류: {str(e)}")
            return []

    def _calculate_ma(self, prices: List[float], period: int) -> List[float]:
        """
        이동평균 계산

        Args:
            prices: 가격 목록
            period: 이동평균 기간

        Returns:
            이동평균 목록
        """
        if len(prices) < period:
            return []

        result = []
        for i in range(len(prices) - period + 1):
            ma = sum(prices[i:i + period]) / period
            result.append(ma)

        return result

    async def analyze_buy_condition(self, stock_code: str, current_price: float,
                                    additional_info: Optional[Dict[str, Any]] = None) -> Tuple[bool, Optional[str]]:
        """
        매수 조건 분석 (골든 크로스)

        Args:
            stock_code: 종목코드
            current_price: 현재가
            additional_info: 추가 정보

        Returns:
            (매수 여부, 매수 사유)
        """
        # 이동평균 데이터 조회
        ma_data = await self.get_moving_averages(stock_code)

        ma5 = ma_data.get('ma5', [])
        ma20 = ma_data.get('ma20', [])

        if len(ma5) < 2 or len(ma20) < 2:
            # 데이터 부족
            return False, None

        # 골든 크로스 확인 (단기선이 장기선 위로 교차)
        if ma5[-2] < ma20[-2] and ma5[-1] > ma20[-1]:
            return True, "골든 크로스 발생"

        return False, None

    async def analyze_sell_condition(self, stock_code: str, holding_info: Dict[str, Any], current_price: float) -> \
    Tuple[bool, Optional[str]]:
        """
        매도 조건 분석 (데드 크로스)

        Args:
            stock_code: 종목코드
            holding_info: 보유 정보
            current_price: 현재가

        Returns:
            (매도 여부, 매도 사유)
        """
        buy_price = holding_info.get('buy_price', 0)
        if buy_price <= 0:
            return False, None

        # 기본 익절/손절 조건 확인
        sell, reason = await self.check_basic_profit_loss(stock_code, buy_price, current_price)
        if sell:
            return sell, reason

        # 이동평균 데이터 조회
        ma_data = await self.get_moving_averages(stock_code)

        ma5 = ma_data.get('ma5', [])
        ma20 = ma_data.get('ma20', [])

        if len(ma5) < 2 or len(ma20) < 2:
            # 데이터 부족
            return False, None

        # 데드 크로스 확인 (단기선이 장기선 아래로 교차)
        if ma5[-2] > ma20[-2] and ma5[-1] < ma20[-1]:
            return True, "데드 크로스 발생"

        return False, None

    def update_params(self, params: Dict[str, Any]) -> None:
        """
        전략 파라미터 업데이트

        Args:
            params: 파라미터 딕셔너리
        """
        super().update_params(params)

        if 'short_ma' in params:
            self.short_ma = params['short_ma']
        if 'long_ma' in params:
            self.long_ma = params['long_ma']

        # 캐시 초기화
        self.ma_cache.clear()
        self.cache_timestamps.clear()

        logger.info(f"이동평균 파라미터 업데이트 - 단기: {self.short_ma}일, 장기: {self.long_ma}일")