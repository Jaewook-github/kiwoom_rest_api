"""
기본 매매 전략 모듈
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple

from config import config
from utils.logger import logger


class BaseStrategy(ABC):
    """기본 매매 전략 추상 클래스"""

    def __init__(self, name: str):
        """
        초기화

        Args:
            name: 전략 이름
        """
        self.name = name
        self.config = config.get('trading')

        # 기본 매매 설정
        self.take_profit_pct = self.config.get('take_profit_pct', 2.0)
        self.stop_loss_pct = self.config.get('stop_loss_pct', -2.0)
        self.max_budget_per_stock = self.config.get('max_budget_per_stock', 500000)
        self.max_stocks = self.config.get('max_stocks', 5)

        logger.info(f"전략 '{name}' 초기화 - 익절: {self.take_profit_pct}%, 손절: {self.stop_loss_pct}%")

    @abstractmethod
    async def analyze_buy_condition(self, stock_code: str, current_price: float,
                                    additional_info: Optional[Dict[str, Any]] = None) -> Tuple[bool, Optional[str]]:
        """
        매수 조건 분석

        Args:
            stock_code: 종목코드
            current_price: 현재가
            additional_info: 추가 정보

        Returns:
            (매수 여부, 매수 사유)
        """
        pass

    @abstractmethod
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
        pass

    async def calculate_quantity(self, stock_code: str, current_price: float, available_cash: float) -> int:
        """
        매수 수량 계산

        Args:
            stock_code: 종목코드
            current_price: 현재가
            available_cash: 사용 가능 현금

        Returns:
            매수 수량
        """
        # 최대 투자 가능 금액 (사용 가능 현금과 종목당 최대 금액 중 작은 값)
        max_budget = min(available_cash, self.max_budget_per_stock)

        # 현재가 기준 최대 매수 가능 수량 계산
        if current_price <= 0:
            return 0

        quantity = int(max_budget / current_price)

        # 수량이 0이면 매수 불가
        if quantity <= 0:
            logger.warning(f"종목 {stock_code} 매수 수량이 0입니다. 현재가: {current_price:,.0f}원")
            return 0

        return quantity

    async def check_basic_profit_loss(self, stock_code: str, buy_price: float, current_price: float) -> Tuple[
        bool, Optional[str]]:
        """
        기본 익절/손절 조건 확인

        Args:
            stock_code: 종목코드
            buy_price: 매수가
            current_price: 현재가

        Returns:
            (매도 여부, 매도 사유)
        """
        # 손익률 계산
        profit_rate = (current_price - buy_price) / buy_price * 100

        # 익절 조건
        if profit_rate >= self.take_profit_pct:
            return True, f"익절 - 수익률: {profit_rate:.2f}%"

        # 손절 조건
        if profit_rate <= self.stop_loss_pct:
            return True, f"손절 - 손실률: {profit_rate:.2f}%"

        # 추가 손익 조건 (하위 클래스에서 구현)
        return False, None

    def update_params(self, params: Dict[str, Any]) -> None:
        """
        전략 파라미터 업데이트

        Args:
            params: 파라미터 딕셔너리
        """
        if 'take_profit_pct' in params:
            self.take_profit_pct = params['take_profit_pct']
        if 'stop_loss_pct' in params:
            self.stop_loss_pct = params['stop_loss_pct']
        if 'max_budget_per_stock' in params:
            self.max_budget_per_stock = params['max_budget_per_stock']
        if 'max_stocks' in params:
            self.max_stocks = params['max_stocks']

        logger.info(f"전략 '{self.name}' 파라미터 업데이트 - 익절: {self.take_profit_pct}%, 손절: {self.stop_loss_pct}%")