# dashboard/layouts/strategy.py
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc


def create_strategy_layout():
    """퀀트 전략 탭 레이아웃 생성"""
    return html.Div([
        html.H2("퀀트 투자 전략", className="mb-4"),
        
        # 전략 선택 및 파라미터 설정
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("전략 선택"),
                    dbc.CardBody([
                        html.Label("투자 전략:"),
                        dcc.Dropdown(
                            id="strategy-selector",
                            options=[
                                {"label": "마법공식 (Magic Formula)", "value": "magic_formula"},
                                {"label": "강환국 퀄리티 전략", "value": "kang_quality"},
                                {"label": "듀얼 모멘텀 전략", "value": "dual_momentum"},
                                {"label": "피오트로스키 F-Score", "value": "piotroski_f"},
                                {"label": "퀀트킹 자산배분", "value": "quant_king"},
                                {"label": "다중 팩터 전략", "value": "multiple_factor"}
                            ],
                            value="magic_formula"
                        ),
                        
                        html.Div(id="strategy-params", className="mt-3")
                    ])
                ], className="h-100")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("전략 설명"),
                    dbc.CardBody([
                        html.Div(id="strategy-description"),
                        html.Hr(),
                        html.Button("전략 실행", id="run-strategy-button", 
                                  className="btn btn-primary mt-2")
                    ])
                ], className="h-100")
            ], width=6)
        ], className="mb-4"),
        
        # 전략 실행 결과
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("전략 결과"),
                    dbc.CardBody([
                        html.Div(id="strategy-result-table", className="mb-3"),
                        dcc.Loading(
                            id="loading-strategy-result",
                            type="circle",
                            children=html.Div(id="strategy-loading-output")
                        )
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # 백테스트 결과
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("백테스트 결과"),
                    dbc.CardBody([
                        html.Div([
                            html.Label("백테스트 기간:"),
                            dcc.RangeSlider(
                                id="backtest-period-slider",
                                min=1,
                                max=5,
                                step=1,
                                marks={
                                    1: "1년",
                                    2: "2년",
                                    3: "3년",
                                    4: "4년",
                                    5: "5년"
                                },
                                value=[3, 5]
                            )
                        ], className="mb-3"),
                        
                        html.Button("백테스트 실행", id="run-backtest-button", 
                                  className="btn btn-secondary mb-3"),
                        
                        dcc.Graph(id="backtest-performance-chart", config={"displayModeBar": False})
                    ])
                ])
            ], width=12)
        ])
    ])