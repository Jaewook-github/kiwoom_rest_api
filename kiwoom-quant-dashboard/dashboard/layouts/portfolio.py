# dashboard/layouts/portfolio.py
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc


def create_portfolio_layout():
    """포트폴리오 분석 탭 레이아웃 생성"""
    return html.Div([
        html.H2("포트폴리오 분석", className="mb-4"),
        
        # 계좌 요약 및 자산 배분
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("계좌 요약"),
                    dbc.CardBody([
                        html.Div(id="account-summary")
                    ])
                ], className="h-100")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("자산 배분"),
                    dbc.CardBody([
                        dcc.Graph(id="asset-allocation-chart", config={"displayModeBar": False})
                    ])
                ], className="h-100")
            ], width=6)
        ], className="mb-4"),
        
        # 보유 종목 현황
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("보유 종목 현황"),
                    dbc.CardBody([
                        html.Div(id="portfolio-holdings-table")
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # 포트폴리오 성과
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("포트폴리오 성과"),
                    dbc.CardBody([
                        dcc.Graph(id="portfolio-performance-chart", config={"displayModeBar": False})
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # 리스크 분석
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("리스크 분석"),
                    dbc.CardBody([
                        dcc.Graph(id="portfolio-risk-chart", config={"displayModeBar": False})
                    ])
                ])
            ], width=12)
        ])
    ])