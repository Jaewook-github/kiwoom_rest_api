# dashboard/layouts/market.py
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc


def create_market_layout():
    """시장 데이터 탭 레이아웃 생성"""
    return html.Div([
        html.H2("시장 개요", className="mb-4"),
        
        # 시장 지수 대시보드
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("주요 지수"),
                    dbc.CardBody([
                        html.Div(id="market-indices-table")
                    ])
                ], className="h-100")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("업종별 등락률"),
                    dbc.CardBody([
                        dcc.Graph(id="sector-performance-chart", config={"displayModeBar": False})
                    ])
                ], className="h-100")
            ], width=6)
        ], className="mb-4"),
        
        # 시장 거래대금 상위종목
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("시장 거래대금 상위종목"),
                    dbc.CardBody([
                        html.Div(id="market-top-volume-table")
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # 시장 심리 지표
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("시장 심리 지표"),
                    dbc.CardBody([
                        dcc.Graph(id="market-sentiment-chart", config={"displayModeBar": False})
                    ])
                ])
            ], width=12)
        ])
    ])