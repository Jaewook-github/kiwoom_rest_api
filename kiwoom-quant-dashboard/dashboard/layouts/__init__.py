# dashboard/layouts/__init__.py
# 대시보드 레이아웃 모듈
from dashboard.layouts.main import create_main_layout
from dashboard.layouts.market import create_market_layout
from dashboard.layouts.portfolio import create_portfolio_layout
from dashboard.layouts.strategy import create_strategy_layout
from dashboard.layouts.stock_detail import create_stock_detail_layout
from dashboard.layouts.analysis import create_analysis_layout

__all__ = [
    'create_main_layout',
    'create_market_layout',
    'create_portfolio_layout',
    'create_strategy_layout',
    'create_stock_detail_layout',
    'create_analysis_layout'
]