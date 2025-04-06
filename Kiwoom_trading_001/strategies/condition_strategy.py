"""
조건검색 기반 매매 전략 모듈
"""
from typing import Dict, Any, List, Optional, Tuple, Set

from ..utils.logger import logger
from ..strategies.base_strategy import BaseStrategy


class ConditionStrategy(BaseStrategy):
    """조건검색 기반 매매 전략 클래스"""

    def __init__(self, name: str = "조건검색기반전략"):
        """
        초기화

        Args:
            name: 전략 이름
        """
        super().__init__(name)

        # 편입/이탈 종목 캐시
        self.in_stocks: Set[str] = set()  # 편입된 종목
        self.out_stocks: Set[str] = set()  # 이탈된 종목

        # 조건별 매수 가능 종목
        self.buy_candidates: Dict[str, List[str]] = {}  # 조건ID: [종목코드, ...]

        # 추가 설정
        self.max_daily_loss_pct = self.config.get('max_daily_loss_pct', -5.0)
        self.partial_profit_ratio = self.config.get('partial_profit_ratio', 0.5)

        logger.info(f"조건검색 기반 전략 초기화 - 최대 손실률: {self.max_daily_loss_pct}%")

    async def analyze_buy_condition(self, stock_code: str, current_price: float,
                                    additional_info: Optional[Dict[str, Any]] = None) -> Tuple[bool, Optional[str]]:
        """
        매수 조건 분석

        Args:
            stock_code: 종목코드
            current_price: 현재가
            additional_info: 추가 정보 (조건검색 결과 등)

        Returns:
            (매수 여부, 매수 사유)
        """
        # 조건검색 편입 여부 확인
        if additional_info and 'condition_id' in additional_info:
            condition_id = additional_info['condition_id']
            condition_name = additional_info.get('condition_name', condition_id)

            # 매수 후보에 추가
            if condition_id not in self.buy_candidates:
                self.buy_candidates[condition_id] = []

            if stock_code not in self.buy_candidates[condition_id]:
                self.buy_candidates[condition_id].append(stock_code)

            # 편입 종목 기록
            self.in_stocks.add(stock_code)

            return True, f"조건검색 편입 - {condition_name}"

        # 추가적인 매수 조건을 여기에 구현
        return False, None

    async def analyze_sell_condition(self, stock_code: str, holding_info: Dict[str, Any], current_price: float) -> \
    Tuple[bool, Optional[str]]:
        """
        매도 조건 분석

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

        # 조건검색 이탈 여부 확인
        if stock_code in self.out_stocks:
            return True, "조건검색 이탈"

        # 당일 최대 손실 확인 (시가 정보가 있는 경우)
        if 'open_price' in holding_info:
            open_price = holding_info['open_price']
            daily_loss_pct = (current_price - open_price) / open_price * 100

            if daily_loss_pct <= self.max_daily_loss_pct:
                return True, f"당일 최대 손실 도달 - 손실률: {daily_loss_pct:.2f}%"

        # 추가적인 매도 조건을 여기에 구현
        return False, None

    async def check_partial_profit(self, stock_code: str, holding_info: Dict[str, Any], current_price: float) -> Tuple[
        bool, int, Optional[str]]:
        """
        부분 익절 조건 확인

        Args:
            stock_code: 종목코드
            holding_info: 보유 정보
            current_price: 현재가

        Returns:
            (부분 매도 여부, 매도 수량, 매도 사유)
        """
        buy_price = holding_info.get('buy_price', 0)
        quantity = holding_info.get('quantity', 0)

        if buy_price <= 0 or quantity <= 0:
            return False, 0, None

        # 수익률 계산
        profit_rate = (current_price - buy_price) / buy_price * 100

        # 익절 조건 도달 시 부분 매도
        if profit_rate >= self.take_profit_pct:
            # 부분 매도 수량 계산 (기본: 50%)
            sell_quantity = int(quantity * self.partial_profit_ratio)

            if sell_quantity <= 0:
                return False, 0, None

            return True, sell_quantity, f"부분 익절 - 수익률: {profit_rate:.2f}%"

        return False, 0, None

    def handle_condition_result(self, result_info: Dict[str, Any]) -> None:
        """
        조건검색 결과 처리

        Args:
            result_info: 조건검색 결과 정보
        """
        condition_id = result_info.get('condition_id')
        stock_codes = result_info.get('stock_codes', [])

        if not condition_id or not stock_codes:
            return

        # 매수 후보 업데이트
        self.buy_candidates[condition_id] = stock_codes

        # 편입 종목 추가
        for code in stock_codes:
            self.in_stocks.add(code)

        logger.info(f"조건 {condition_id} 매수 후보 {len(stock_codes)}개 업데이트")

    def handle_realtime_condition(self, realtime_info: Dict[str, Any]) -> None:
        """
        실시간 조건검색 결과 처리

        Args:
            realtime_info: 실시간 조건검색 정보
        """
        stock_code = realtime_info.get('stock_code')
        status = realtime_info.get('status')  # 'in' 또는 'out'

        if not stock_code or not status:
            return

        if status == 'in':
            self.in_stocks.add(stock_code)
            self.out_stocks.discard(stock_code)  # 이탈 목록에서 제거
        elif status == 'out':
            self.out_stocks.add(stock_code)
            # 편입 상태는 유지 (다른 조건에서 편입 상태일 수 있음)

        logger.debug(f"실시간 조건 {status}: {stock_code}")

    def reset_candidates(self) -> None:
        """매수 후보 목록 초기화"""
        self.buy_candidates.clear()
        self.in_stocks.clear()
        self.out_stocks.clear()