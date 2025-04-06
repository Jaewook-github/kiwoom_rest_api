"""
핵심 패키지
"""
# 순환 참조 제거
# from trader import KiwoomAutoTrader
from core.order_manager import OrderManager
from core.condition_manager import ConditionManager

__all__ = [
    'KiwoomAutoTrader',
    'OrderManager',
    'ConditionManager'
]

# 마지막에 임포트하여 순환 참조 해결
from core.trader import KiwoomAutoTrader