# dashboard/layouts/analysis.py
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta


def create_analysis_layout():
    """분석 화면 레이아웃 생성"""
    return html.Div([
        html.H2("성과 분석", className="mb-4"),
        
        # 백테스트 설정
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("백테스트 설정"),
                    dbc.CardBody([
                        html.Div([
                            html.Label("전략 선택:"),
                            dcc.Dropdown(
                                id="backtest-strategy-selector",
                                options=[
                                    {"label": "마법공식 (Magic Formula)", "value": "magic_formula"},
                                    {"label": "강환국 퀄리티 전략", "value": "kang_quality"},
                                    {"label": "듀얼 모멘텀 전략", "value": "dual_momentum"},
                                    {"label": "피오트로스키 F-Score", "value": "piotroski_f"},
                                    {"label": "퀀트킹 자산배분", "value": "quant_king"},
                                    {"label": "그레이엄 전략", "value": "graham"},
                                    {"label": "퀄리티 팩터 전략", "value": "quality_factor"},
                                    {"label": "상대 강도 전략", "value": "relative_strength"},
                                    {"label": "다중 팩터 전략", "value": "multiple_factor"}
                                ],
                                value="magic_formula",
                                clearable=False,
                                className="mb-3"
                            ),
                            
                            html.Label("백테스트 기간:"),
                            dcc.DatePickerRange(
                                id="backtest-date-range",
                                min_date_allowed=datetime.now() - timedelta(days=365*10),
                                max_date_allowed=datetime.now(),
                                start_date=datetime.now() - timedelta(days=365*3),
                                end_date=datetime.now(),
                                className="mb-3"
                            ),
                            
                            html.Label("초기 투자금액:"),
                            dcc.Input(
                                id="backtest-initial-capital",
                                type="number",
                                value=100000000,
                                step=10000000,
                                className="form-control mb-3"
                            ),
                            
                            html.Label("리밸런싱 주기:"),
                            dcc.Dropdown(
                                id="backtest-rebalancing-freq",
                                options=[
                                    {"label": "월별", "value": "M"},
                                    {"label": "분기별", "value": "Q"},
                                    {"label": "반기별", "value": "H"},
                                    {"label": "연간", "value": "Y"}
                                ],
                                value="M",
                                clearable=False,
                                className="mb-3"
                            ),
                            
                            html.Label("벤치마크:"),
                            dcc.Dropdown(
                                id="backtest-benchmark",
                                options=[
                                    {"label": "KOSPI", "value": "KOSPI"},
                                    {"label": "KOSDAQ", "value": "KOSDAQ"},
                                    {"label": "KOSPI 200", "value": "KOSPI200"},
                                    {"label": "없음", "value": "none"}
                                ],
                                value="KOSPI",
                                clearable=False,
                                className="mb-3"
                            ),
                            
                            html.Button("백테스트 실행", id="run-backtest-analysis-button", 
                                      className="btn btn-primary")
                        ])
                    ])
                ], className="h-100")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("전략 파라미터"),
                    dbc.CardBody([
                        html.Div(id="backtest-strategy-params")
                    ])
                ], className="h-100")
            ], width=4),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("백테스트 정보"),
                    dbc.CardBody([
                        html.Div(id="backtest-info-display")
                    ])
                ], className="h-100")
            ], width=5)
        ], className="mb-4"),
        
        # 백테스트 결과
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("백테스트 성과"),
                    dbc.CardBody([
                        dcc.Loading(
                            id="loading-backtest-result",
                            type="circle",
                            children=[
                                dcc.Graph(id="backtest-performance-graph", config={"displayModeBar": False})
                            ]
                        )
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # 성과 지표 및 리스크 분석
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("성과 지표"),
                    dbc.CardBody([
                        html.Div(id="performance-metrics-table")
                    ])
                ], className="h-100")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("리스크 분석"),
                    dbc.CardBody([
                        html.Div(id="risk-metrics-table")
                    ])
                ], className="h-100")
            ], width=6)
        ], className="mb-4"),
        
        # 매매 내역 및 포트폴리오 구성
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("매매 내역"),
                    dbc.CardBody([
                        html.Div(id="backtest-trade-history-table", style={"height": "400px", "overflow": "auto"})
                    ])
                ])
            ], width=7),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("최종 포트폴리오 구성"),
                    dbc.CardBody([
                        html.Div(id="backtest-final-portfolio")
                    ])
                ], className="h-100")
            ], width=5)
        ])
    ])