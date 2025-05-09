# dashboard/layouts/stock_detail.py
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc


def create_stock_detail_layout():
    """종목 상세정보 탭 레이아웃 생성"""
    return html.Div([
        html.H2("종목 상세 정보", className="mb-4"),
        
        # 종목 검색 및 기본 정보
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("종목 검색"),
                    dbc.CardBody([
                        html.Div([
                            dcc.Input(
                                id="stock-search-input",
                                type="text",
                                placeholder="종목명 또는 코드 입력",
                                className="form-control mb-2"
                            ),
                            html.Button("검색", id="stock-search-button", className="btn btn-primary")
                        ])
                    ])
                ])
            ], width=4),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("기본 정보"),
                    dbc.CardBody([
                        html.Div(id="stock-basic-info")
                    ])
                ], className="h-100")
            ], width=8)
        ], className="mb-4"),
        
        # 가격 차트 및 재무 지표
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("가격 차트"),
                    dbc.CardBody([
                        html.Div([
                            dcc.RadioItems(
                                id="chart-period-selector",
                                options=[
                                    {"label": "1개월", "value": "1M"},
                                    {"label": "3개월", "value": "3M"},
                                    {"label": "6개월", "value": "6M"},
                                    {"label": "1년", "value": "1Y"},
                                    {"label": "3년", "value": "3Y"},
                                    {"label": "5년", "value": "5Y"}
                                ],
                                value="1Y",
                                inline=True,
                                className="mb-2"
                            ),
                            
                            dcc.Graph(id="stock-price-chart", config={"displayModeBar": False})
                        ])
                    ])
                ])
            ], width=8),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("주요 재무 지표"),
                    dbc.CardBody([
                        html.Div(id="stock-financial-indicators")
                    ])
                ], className="h-100")
            ], width=4)
        ], className="mb-4"),
        
        # 기술적 지표 및 뉴스
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("기술적 지표"),
                    dbc.CardBody([
                        dcc.Dropdown(
                            id="technical-indicator-selector",
                            options=[
                                {"label": "이동평균선", "value": "ma"},
                                {"label": "MACD", "value": "macd"},
                                {"label": "RSI", "value": "rsi"},
                                {"label": "볼린저 밴드", "value": "bollinger"},
                                {"label": "스토캐스틱", "value": "stoch"}
                            ],
                            value=["ma"],
                            multi=True,
                            className="mb-2"
                        ),
                        
                        dcc.Graph(id="technical-indicator-chart", config={"displayModeBar": False})
                    ])
                ])
            ], width=8),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("종목 뉴스 및 공시"),
                    dbc.CardBody([
                        html.Div(id="stock-news-disclosure", style={"maxHeight": "400px", "overflow": "auto"})
                    ])
                ], className="h-100")
            ], width=4)
        ], className="mb-4"),
        
        # 투자 의견 및 컨센서스
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("투자 의견 및 컨센서스"),
                    dbc.CardBody([
                        html.Div(id="stock-investment-opinion")
                    ])
                ])
            ], width=12)
        ])
    ])