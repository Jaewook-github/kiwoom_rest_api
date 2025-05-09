"""
키움증권 REST API 퀀트 대시보드 프로젝트의 대시보드 레이아웃 모듈
"""

# dashboard/layouts/main.py
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dashboard.layouts.market import create_market_layout
from dashboard.layouts.portfolio import create_portfolio_layout
from dashboard.layouts.strategy import create_strategy_layout
from dashboard.layouts.stock_detail import create_stock_detail_layout


def create_main_layout():
    """대시보드 메인 레이아웃 생성"""
    return html.Div([
        # 헤더
        html.Div([
            html.H1("키움증권 퀀트 투자 대시보드", className="text-center mb-4"),
            html.Hr()
        ], className="container mt-4"),
        
        # 탭 메뉴
        dbc.Container([
            dcc.Tabs(id="tabs", value="tab-market", children=[
                dcc.Tab(label="시장 데이터", value="tab-market", className="custom-tab"),
                dcc.Tab(label="포트폴리오 분석", value="tab-portfolio", className="custom-tab"),
                dcc.Tab(label="퀀트 전략", value="tab-strategy", className="custom-tab"),
                dcc.Tab(label="종목 상세정보", value="tab-stock-detail", className="custom-tab"),
            ], className="custom-tabs"),
            
            # 탭 내용
            html.Div(id="tab-content", className="pt-4")
        ]),
        
        # 데이터 저장소
        dcc.Store(id="market-data-store"),
        dcc.Store(id="portfolio-data-store"),
        dcc.Store(id="stock-data-store"),
        
        # 주기적 데이터 업데이트
        dcc.Interval(
            id="interval-component",
            interval=60 * 1000,  # 1분마다 갱신
            n_intervals=0
        )
    ])
