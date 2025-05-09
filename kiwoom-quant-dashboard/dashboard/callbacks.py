
# dashboard/callbacks.py
from dash import Input, Output, State, html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from api.kiwoom_api import KiwoomAPI
from data.fetcher import DataFetcher
from strategies.value.magic_formula import MagicFormula
from strategies.value.kang_quality import KangQualityStrategy
from strategies.momentum.dual_momentum import DualMomentumStrategy
from strategies.value.piotroski_f import PiotroskiFScore
from strategies.asset_allocation.quant_king import QuantKingAssetAllocation
from strategies.custom.multiple_factor import MultipleFactorStrategy


def register_callbacks(app):
    """대시보드 콜백 함수 등록"""
    
    # 탭 전환 콜백
    @app.callback(
        Output("tab-content", "children"),
        Input("tabs", "value")
    )
    def render_tab_content(tab):
        """탭 선택에 따른 내용 렌더링"""
        if tab == "tab-market":
            return create_market_layout()
        elif tab == "tab-portfolio":
            return create_portfolio_layout()
        elif tab == "tab-strategy":
            return create_strategy_layout()
        elif tab == "tab-stock-detail":
            return create_stock_detail_layout()
        return html.Div("탭을 선택해주세요.")
    
    # 시장 데이터 탭 콜백
    @app.callback(
        [Output("market-indices-table", "children"),
         Output("sector-performance-chart", "figure"),
         Output("market-top-volume-table", "children"),
         Output("market-sentiment-chart", "figure"),
         Output("market-data-store", "data")],
        Input("interval-component", "n_intervals")
    )
    def update_market_data(n_intervals):
        """시장 데이터 업데이트"""
        # API 클라이언트 및 데이터 수집기 초기화
        api_client = KiwoomAPI()
        data_fetcher = DataFetcher(api_client)
        
        # 임시 데이터 (실제 구현 시 API에서 데이터를 가져와야 함)
        # 지수 데이터
        indices_data = {
            "KOSPI": {"value": 2487.56, "change": 14.21, "change_percent": 0.57},
            "KOSDAQ": {"value": 832.35, "change": -3.42, "change_percent": -0.41},
            "KOSPI200": {"value": 331.45, "change": 2.13, "change_percent": 0.65},
            "KRX100": {"value": 5234.76, "change": 21.87, "change_percent": 0.42}
        }
        
        # 지수 현황 테이블
        indices_table = dbc.Table([
            html.Thead([
                html.Tr([
                    html.Th("지수명"),
                    html.Th("지수값"),
                    html.Th("전일대비"),
                    html.Th("등락률(%)")
                ])
            ]),
            html.Tbody([
                html.Tr([
                    html.Td(index),
                    html.Td(f"{data['value']:,.2f}"),
                    html.Td(f"{data['change']:+,.2f}", style={"color": "red" if data['change'] > 0 else "blue"}),
                    html.Td(f"{data['change_percent']:+,.2f}%", style={"color": "red" if data['change_percent'] > 0 else "blue"})
                ]) for index, data in indices_data.items()
            ])
        ], bordered=True, hover=True, responsive=True, className="table-sm")
        
        # 업종별 등락률 데이터
        sectors = ['반도체', '금융', '제약', '철강', '통신', '화학', '건설', '자동차', '유통', 'IT']
        change_percents = np.random.normal(0, 2, len(sectors))
        
        # 업종별 등락률 차트
        sector_fig = go.Figure()
        colors = ['red' if c > 0 else 'blue' for c in change_percents]
        
        sector_fig.add_trace(go.Bar(
            x=sectors,
            y=change_percents,
            marker_color=colors,
            text=[f"{c:+.2f}%" for c in change_percents],
            textposition='outside'
        ))
        
        sector_fig.update_layout(
            title="업종별 등락률",
            xaxis_title="",
            yaxis_title="등락률(%)",
            height=300,
            margin=dict(l=40, r=40, t=40, b=50),
            plot_bgcolor="white",
            xaxis=dict(
                gridcolor="lightgray",
                showgrid=False
            ),
            yaxis=dict(
                gridcolor="lightgray",
                zeroline=True,
                zerolinecolor="black",
                zerolinewidth=1
            )
        )
        
        # 시장 거래대금 상위종목 데이터
        top_volume_data = [
            {"종목코드": "005930", "종목명": "삼성전자", "현재가": 72300, "전일대비": 700, "등락률": 0.98, "거래대금": 687235},
            {"종목코드": "000660", "종목명": "SK하이닉스", "현재가": 146500, "전일대비": -1000, "등락률": -0.68, "거래대금": 342821},
            {"종목코드": "035420", "종목명": "NAVER", "현재가": 219000, "전일대비": 6500, "등락률": 3.06, "거래대금": 236417},
            {"종목코드": "051910", "종목명": "LG화학", "현재가": 478000, "전일대비": 15000, "등락률": 3.24, "거래대금": 198362},
            {"종목코드": "035720", "종목명": "카카오", "현재가": 52800, "전일대비": -600, "등락률": -1.12, "거래대금": 157489},
            {"종목코드": "005380", "종목명": "현대차", "현재가": 189500, "전일대비": 2500, "등락률": 1.34, "거래대금": 145682},
            {"종목코드": "068270", "종목명": "셀트리온", "현재가": 164500, "전일대비": -3500, "등락률": -2.08, "거래대금": 138975},
            {"종목코드": "028260", "종목명": "삼성물산", "현재가": 123000, "전일대비": 1500, "등락률": 1.23, "거래대금": 107834},
            {"종목코드": "066570", "종목명": "LG전자", "현재가": 87900, "전일대비": -400, "등락률": -0.45, "거래대금": 98754},
            {"종목코드": "207940", "종목명": "삼성바이오로직스", "현재가": 736000, "전일대비": 4000, "등락률": 0.55, "거래대금": 87632}
        ]
        
        # 거래대금 상위종목 테이블
        top_volume_table = dash_table.DataTable(
            data=top_volume_data,
            columns=[
                {"name": "종목코드", "id": "종목코드"},
                {"name": "종목명", "id": "종목명"},
                {"name": "현재가", "id": "현재가", "type": "numeric", "format": {"specifier": ","}},
                {"name": "전일대비", "id": "전일대비", "type": "numeric", "format": {"specifier": "+,"}},
                {"name": "등락률(%)", "id": "등락률", "type": "numeric", "format": {"specifier": "+.2f"}},
                {"name": "거래대금(백만)", "id": "거래대금", "type": "numeric", "format": {"specifier": ","}}
            ],
            style_table={"overflowX": "auto"},
            style_cell={
                "textAlign": "center",
                "padding": "5px",
                "minWidth": "80px"
            },
            style_header={
                "backgroundColor": "rgb(230, 230, 230)",
                "fontWeight": "bold"
            },
            style_data_conditional=[
                {
                    "if": {"filter_query": "{전일대비} > 0"},
                    "color": "red"
                },
                {
                    "if": {"filter_query": "{전일대비} < 0"},
                    "color": "blue"
                }
            ],
            page_size=10
        )
        
        # 시장 심리 지표 데이터 (예: VIX, PER, 외국인 순매수 등)
        dates = pd.date_range(end=pd.Timestamp.now(), periods=60, freq='B')
        
        vix_values = np.random.normal(20, 3, len(dates))
        vix_values = np.cumsum(np.random.normal(0, 0.3, len(dates))) + 20
        vix_values = np.clip(vix_values, 10, 35)
        
        foreign_net_buy = np.cumsum(np.random.normal(0, 100, len(dates)))
        
        # 시장 심리 지표 차트
        sentiment_fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        sentiment_fig.add_trace(
            go.Scatter(
                x=dates,
                y=vix_values,
                name="변동성 지수 (VIX)",
                line=dict(color='red', width=2)
            ),
            secondary_y=False
        )
        
        sentiment_fig.add_trace(
            go.Bar(
                x=dates,
                y=foreign_net_buy,
                name="외국인 순매수 (억원)",
                marker_color=['red' if x > 0 else 'blue' for x in foreign_net_buy]
            ),
            secondary_y=True
        )
        
        sentiment_fig.update_layout(
            title="시장 심리 지표",
            height=400,
            margin=dict(l=40, r=40, t=40, b=50),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            plot_bgcolor="white",
            xaxis=dict(
                gridcolor="lightgray",
                showgrid=True
            ),
            yaxis=dict(
                title="변동성 지수 (VIX)",
                gridcolor="lightgray",
                showgrid=True
            ),
            yaxis2=dict(
                title="외국인 순매수 (억원)",
                gridcolor="lightgray",
                showgrid=False
            )
        )
        
        # 데이터 저장
        market_data = {
            "indices": indices_data,
            "sectors": {"categories": sectors, "values": change_percents.tolist()},
            "top_volume": top_volume_data,
            "vix": {"dates": dates.strftime("%Y-%m-%d").tolist(), "values": vix_values.tolist()},
            "foreign_net_buy": {"dates": dates.strftime("%Y-%m-%d").tolist(), "values": foreign_net_buy.tolist()}
        }
        
        return indices_table, sector_fig, top_volume_table, sentiment_fig, market_data
    
    # 전략 선택 콜백
    @app.callback(
        [Output("strategy-params", "children"),
         Output("strategy-description", "children")],
        [Input("strategy-selector", "value")]
    )
    def update_strategy_params(strategy_value):
        """선택한 전략에 따른 파라미터 UI 및 설명 업데이트"""
        if strategy_value == "magic_formula":
            params_ui = html.Div([
                html.Label("선택할 종목 수:"),
                dcc.Slider(
                    id="magic-formula-n-stocks",
                    min=5,
                    max=50,
                    step=5,
                    value=30,
                    marks={i: str(i) for i in range(5, 51, 5)},
                    className="mb-3"
                ),
                
                html.Label("최소 시가총액 (억원):"),
                dcc.Slider(
                    id="magic-formula-min-market-cap",
                    min=100,
                    max=5000,
                    step=100,
                    value=500,
                    marks={i: str(i) for i in range(0, 5001, 1000)},
                    className="mb-3"
                )
            ])
            
            description = html.Div([
                html.P("조엘 그린블랫의 마법공식은 두 가지 지표를 결합한 전략입니다:"),
                html.Ol([
                    html.Li("영업이익률(EBIT/EV): 기업가치 대비 영업이익이 높은 종목"),
                    html.Li("자본수익률(ROC): 투자자본 대비 영업이익이 높은 종목")
                ]),
                html.P("두 지표에 대한 순위를 합산하여 최종 순위가 높은 종목을 선정합니다. 이 전략은 저평가된 우량 기업에 투자하는 가치투자 전략입니다.")
            ])
            
        elif strategy_value == "kang_quality":
            params_ui = html.Div([
                html.Label("선택할 종목 수:"),
                dcc.Slider(
                    id="kang-quality-n-stocks",
                    min=5,
                    max=50,
                    step=5,
                    value=30,
                    marks={i: str(i) for i in range(5, 51, 5)},
                    className="mb-3"
                ),
                
                html.Label("최소 시가총액 (억원):"),
                dcc.Slider(
                    id="kang-quality-min-market-cap",
                    min=100,
                    max=5000,
                    step=100,
                    value=500,
                    marks={i: str(i) for i in range(0, 5001, 1000)},
                    className="mb-3"
                )
            ])
            
            description = html.Div([
                html.P("강환국의 퀄리티 전략은 다음 지표들을 결합합니다:"),
                html.Ol([
                    html.Li("PER (주가수익비율) - 낮을수록 유리"),
                    html.Li("PBR (주가순자산비율) - 낮을수록 유리"),
                    html.Li("ROE (자기자본이익률) - 높을수록 유리"),
                    html.Li("GP/A (총자산 대비 매출총이익) - 높을수록 유리")
                ]),
                html.P("각 지표에 대한 순위를 합산하여 최종 순위가 높은 종목을 선정합니다. 저평가된 우량 기업을 발굴하는 전략입니다.")
            ])
            
        elif strategy_value == "dual_momentum":
            params_ui = html.Div([
                html.Label("선택할 종목 수:"),
                dcc.Slider(
                    id="dual-momentum-n-stocks",
                    min=5,
                    max=30,
                    step=5,
                    value=10,
                    marks={i: str(i) for i in range(5, 31, 5)},
                    className="mb-3"
                ),
                
                html.Label("모멘텀 계산 기간 (개월):"),
                dcc.Slider(
                    id="dual-momentum-period",
                    min=1,
                    max=24,
                    step=1,
                    value=12,
                    marks={i: str(i) for i in range(0, 25, 3)},
                    className="mb-3"
                ),
                
                html.Label("절대 모멘텀 임계값 (%):"),
                dcc.Slider(
                    id="dual-momentum-threshold",
                    min=-10,
                    max=10,
                    step=1,
                    value=0,
                    marks={i: str(i) for i in range(-10, 11, 2)},
                    className="mb-3"
                )
            ])
            
            description = html.Div([
                html.P("듀얼 모멘텀 전략은 상대 모멘텀과 절대 모멘텀을 결합한 전략입니다:"),
                html.Ol([
                    html.Li("상대 모멘텀: 다른 종목 대비 수익률이 높은 종목 선정"),
                    html.Li("절대 모멘텀: 시장 수익률 및 임계값보다 높은 수익률을 보이는 종목 선정")
                ]),
                html.P("상승 추세에 있는 강세 종목에 투자하는 모멘텀 투자 전략입니다.")
            ])
            
        elif strategy_value == "piotroski_f":
            params_ui = html.Div([
                html.Label("선택할 종목 수:"),
                dcc.Slider(
                    id="piotroski-f-n-stocks",
                    min=5,
                    max=30,
                    step=5,
                    value=20,
                    marks={i: str(i) for i in range(5, 31, 5)},
                    className="mb-3"
                ),
                
                html.Label("최소 F-Score:"),
                dcc.Slider(
                    id="piotroski-f-min-score",
                    min=5,
                    max=9,
                    step=1,
                    value=7,
                    marks={i: str(i) for i in range(5, 10)},
                    className="mb-3"
                ),
                
                html.Label("최대 PBR:"),
                dcc.Slider(
                    id="piotroski-f-max-pbr",
                    min=0.5,
                    max=3,
                    step=0.1,
                    value=1.0,
                    marks={i: str(i) for i in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]},
                    className="mb-3"
                )
            ])
            
            description = html.Div([
                html.P("피오트로스키 F-Score는 재무 상태가 개선되고 있는 저평가 가치주를 선별하는 전략입니다."),
                html.P("9가지 재무 기준에 따라 각 기업에 0-9점의 점수를 부여합니다:"),
                html.Ol([
                    html.Li("수익성 (4가지 지표): ROA > 0, OCF > 0, ROA 증가, OCF > ROA"),
                    html.Li("레버리지, 유동성, 자금조달 (3가지 지표): 장기부채 비율 감소, 유동비율 증가, 신주발행 없음"),
                    html.Li("운영효율성 (2가지 지표): 매출총이익률 증가, 자산회전율 증가")
                ]),
                html.P("F-Score가 높고 PBR이 낮은 종목을 선정하는 가치투자 전략입니다.")
            ])
            
        elif strategy_value == "quant_king":
            params_ui = html.Div([
                html.Label("모멘텀 계산 기간 (개월):"),
                dcc.Slider(
                    id="quant-king-momentum-period",
                    min=3,
                    max=24,
                    step=3,
                    value=12,
                    marks={i: str(i) for i in range(3, 25, 3)},
                    className="mb-3"
                ),
                
                html.Label("변동성 계산 기간 (일):"),
                dcc.Slider(
                    id="quant-king-volatility-lookback",
                    min=10,
                    max=60,
                    step=10,
                    value=20,
                    marks={i: str(i) for i in range(10, 61, 10)},
                    className="mb-3"
                ),
                
                html.Label("주식 최대 배분 비율 (%):"),
                dcc.Slider(
                    id="quant-king-max-stock",
                    min=0,
                    max=100,
                    step=10,
                    value=60,
                    marks={i: str(i) for i in range(0, 101, 10)},
                    className="mb-3"
                )
            ])
            
            description = html.Div([
                html.P("퀀트킹 자산배분 전략은 시장 상황에 따라 자산 간 비중을 조절하는 전략입니다."),
                html.P("주요 특징:"),
                html.Ul([
                    html.Li("시장 추세(이동평균선)에 따라 공격/방어 전략 선택"),
                    html.Li("모멘텀이 높은 자산에 집중 투자"),
                    html.Li("변동성에 따라 주식 비중 조절"),
                    html.Li("주식, 채권, 금, 현금 등 다양한 자산군 활용")
                ]),
                html.P("시장 상황에 적응하는 유연한 자산배분 전략입니다.")
            ])
            
        elif strategy_value == "multiple_factor":
            params_ui = html.Div([
                html.Label("선택할 종목 수:"),
                dcc.Slider(
                    id="multiple-factor-n-stocks",
                    min=5,
                    max=50,
                    step=5,
                    value=20,
                    marks={i: str(i) for i in range(5, 51, 5)},
                    className="mb-3"
                ),
                
                html.Label("최소 시가총액 (억원):"),
                dcc.Slider(
                    id="multiple-factor-min-market-cap",
                    min=100,
                    max=5000,
                    step=100,
                    value=500,
                    marks={i: str(i) for i in range(0, 5001, 1000)},
                    className="mb-3"
                ),
                
                html.Label("팩터별 가중치 (합계 100%):"),
                html.Div([
                    html.Div([
                        html.Label("PER:"),
                        dcc.Slider(
                            id="multiple-factor-per-weight",
                            min=0,
                            max=50,
                            step=5,
                            value=20,
                            marks={i: str(i) for i in range(0, 51, 10)}
                        )
                    ], className="mb-2"),
                    
                    html.Div([
                        html.Label("PBR:"),
                        dcc.Slider(
                            id="multiple-factor-pbr-weight",
                            min=0,
                            max=50,
                            step=5,
                            value=20,
                            marks={i: str(i) for i in range(0, 51, 10)}
                        )
                    ], className="mb-2"),
                    
                    html.Div([
                        html.Label("ROE:"),
                        dcc.Slider(
                            id="multiple-factor-roe-weight",
                            min=0,
                            max=50,
                            step=5,
                            value=20,
                            marks={i: str(i) for i in range(0, 51, 10)}
                        )
                    ], className="mb-2"),
                    
                    html.Div([
                        html.Label("모멘텀(3개월):"),
                        dcc.Slider(
                            id="multiple-factor-momentum-weight",
                            min=0,
                            max=50,
                            step=5,
                            value=15,
                            marks={i: str(i) for i in range(0, 51, 10)}
                        )
                    ], className="mb-2"),
                    
                    html.Div([
                        html.Label("GP/A:"),
                        dcc.Slider(
                            id="multiple-factor-gpa-weight",
                            min=0,
                            max=50,
                            step=5,
                            value=15,
                            marks={i: str(i) for i in range(0, 51, 10)}
                        )
                    ], className="mb-2"),
                    
                    html.Div([
                        html.Label("배당수익률:"),
                        dcc.Slider(
                            id="multiple-factor-dividend-weight",
                            min=0,
                            max=50,
                            step=5,
                            value=10,
                            marks={i: str(i) for i in range(0, 51, 10)}
                        )
                    ], className="mb-2")
                ])
            ])
            
            description = html.Div([
                html.P("다중 팩터 전략은 여러 투자 팩터를 조합하여 종목을 선별하는 사용자 정의 전략입니다."),
                html.P("사용 가능한 주요 팩터:"),
                html.Ul([
                    html.Li("가치 팩터: PER, PBR, 배당수익률"),
                    html.Li("퀄리티 팩터: ROE, GP/A"),
                    html.Li("모멘텀 팩터: 3개월 수익률")
                ]),
                html.P("각 팩터에 가중치를 설정하여 자신만의 맞춤형 투자 전략을 구성할 수 있습니다.")
            ])
            
        else:
            params_ui = html.Div("전략을 선택해주세요.")
            description = html.Div("")
            
        return params_ui, description
    
    # 전략 실행 콜백
    @app.callback(
        Output("strategy-result-table", "children"),
        [Input("run-strategy-button", "n_clicks")],
        [State("strategy-selector", "value")]
    )
    def run_strategy(n_clicks, strategy_value):
        """선택한 전략 실행 및 결과 표시"""
        if n_clicks is None:
            return html.Div("전략을 실행해주세요.")
            
        # 전략 초기화
        if strategy_value == "magic_formula":
            strategy = MagicFormula()
        elif strategy_value == "kang_quality":
            strategy = KangQualityStrategy()
        elif strategy_value == "dual_momentum":
            strategy = DualMomentumStrategy()
        elif strategy_value == "piotroski_f":
            strategy = PiotroskiFScore()
        elif strategy_value == "quant_king":
            strategy = QuantKingAssetAllocation()
        elif strategy_value == "multiple_factor":
            strategy = MultipleFactorStrategy()
        else:
            return html.Div("알 수 없는 전략입니다.")
            
        # 임시 데이터 (실제 구현 시 API에서 데이터를 가져와야 함)
        if strategy_value in ["magic_formula", "kang_quality", "piotroski_f", "multiple_factor"]:
            # 가치 투자 전략용 데이터
            # 재무제표 데이터 생성
            codes = [f"{i:06d}" for i in range(1, 31)]
            names = [f"종목{i}" for i in range(1, 31)]
            np.random.seed(42)  # 재현성을 위한 시드 설정
            
            financial_data = pd.DataFrame({
                "종목코드": codes,
                "종목명": names,
                "시가총액": np.random.randint(10000000000, 100000000000000, len(codes)),
                "PER": np.random.uniform(5, 30, len(codes)),
                "PBR": np.random.uniform(0.5, 5, len(codes)),
                "ROE": np.random.uniform(5, 30, len(codes)),
                "GP/A": np.random.uniform(0, 0.5, len(codes)) * 100,
                "영업이익": np.random.randint(10000000000, 1000000000000, len(codes)),
                "당기순이익": np.random.randint(5000000000, 500000000000, len(codes)),
                "EBIT": np.random.randint(10000000000, 1000000000000, len(codes)),
                "EV": np.random.randint(50000000000, 5000000000000, len(codes)),
                "자본총계": np.random.randint(50000000000, 5000000000000, len(codes)),
                "자산총계": np.random.randint(100000000000, 10000000000000, len(codes)),
                "투자자본": np.random.randint(50000000000, 5000000000000, len(codes)),
                "매출총이익": np.random.randint(10000000000, 1000000000000, len(codes)),
                "매출액": np.random.randint(50000000000, 5000000000000, len(codes)),
                "영업현금흐름": np.random.randint(-10000000000, 500000000000, len(codes)),
                "배당수익률": np.random.uniform(0, 5, len(codes))
            })
            
            # 현재가 데이터 생성
            current_prices = pd.DataFrame({
                "종목코드": codes,
                "종목명": names,
                "현재가": np.random.randint(10000, 1000000, len(codes)),
                "전일대비": np.random.randint(-50000, 50000, len(codes)),
                "등락률": np.random.uniform(-5, 5, len(codes))
            })
            
            # 전략 실행 데이터 준비
            data = {
                "financial_data": financial_data,
                "current_prices": current_prices
            }
            
            if strategy_value == "piotroski_f":
                # 이전 기간 재무제표 데이터 추가
                financial_data_prev = financial_data.copy()
                financial_data_prev["당기순이익"] = financial_data_prev["당기순이익"] * np.random.uniform(0.7, 1.2, len(codes))
                financial_data_prev["영업이익"] = financial_data_prev["영업이익"] * np.random.uniform(0.7, 1.2, len(codes))
                financial_data_prev["자본총계"] = financial_data_prev["자본총계"] * np.random.uniform(0.8, 1.1, len(codes))
                financial_data_prev["자산총계"] = financial_data_prev["자산총계"] * np.random.uniform(0.8, 1.1, len(codes))
                financial_data_prev["매출총이익"] = financial_data_prev["매출총이익"] * np.random.uniform(0.7, 1.2, len(codes))
                financial_data_prev["매출액"] = financial_data_prev["매출액"] * np.random.uniform(0.7, 1.2, len(codes))
                
                data["financial_data_prev"] = financial_data_prev
                
            if strategy_value == "multiple_factor":
                # 가격 히스토리 데이터 생성
                price_data = {}
                
                for code, name in zip(codes, names):
                    days = 250
                    dates = pd.date_range(end=datetime.now(), periods=days)
                    prices = np.cumsum(np.random.normal(0, 1, days)) + 100
                    prices = np.clip(prices, 50, 500)
                    
                    df = pd.DataFrame({
                        "일자": dates,
                        "종목코드": code,
                        "종목명": name,
                        "시가": prices * np.random.uniform(0.98, 0.99, days),
                        "고가": prices * np.random.uniform(1.01, 1.03, days),
                        "저가": prices * np.random.uniform(0.97, 0.99, days),
                        "종가": prices,
                        "거래량": np.random.randint(100000, 1000000, days)
                    })
                    
                    price_data[code] = df
                    
                data["price_data"] = price_data
                
        elif strategy_value == "dual_momentum":
            # 모멘텀 전략용 데이터
            # 가격 히스토리 데이터 생성
            codes = [f"{i:06d}" for i in range(1, 31)]
            names = [f"종목{i}" for i in range(1, 31)]
            
            price_data = {}
            
            for code, name in zip(codes, names):
                days = 250
                dates = pd.date_range(end=datetime.now(), periods=days)
                prices = np.cumsum(np.random.normal(0, 1, days)) + 100
                prices = np.clip(prices, 50, 500)
                
                df = pd.DataFrame({
                    "일자": dates,
                    "종목코드": code,
                    "종목명": name,
                    "시가": prices * np.random.uniform(0.98, 0.99, days),
                    "고가": prices * np.random.uniform(1.01, 1.03, days),
                    "저가": prices * np.random.uniform(0.97, 0.99, days),
                    "종가": prices,
                    "거래량": np.random.randint(100000, 1000000, days)
                })
                
                price_data[code] = df
                
            # 시장 지수 데이터
            days = 250
            dates = pd.date_range(end=datetime.now(), periods=days)
            prices = np.cumsum(np.random.normal(0, 0.5, days)) + 100
            prices = np.clip(prices, 80, 120)
            
            index_data = pd.DataFrame({
                "일자": dates,
                "종가": prices,
                "시가": prices * np.random.uniform(0.99, 0.995, days),
                "고가": prices * np.random.uniform(1.005, 1.01, days),
                "저가": prices * np.random.uniform(0.99, 0.995, days),
                "거래량": np.random.randint(1000000, 10000000, days)
            })
            
            data = {
                "price_data": price_data,
                "index_data": index_data
            }
            
        elif strategy_value == "quant_king":
            # 자산배분 전략용 데이터
            # 자산 데이터 생성
            days = 250
            dates = pd.date_range(end=datetime.now(), periods=days)
            
            # 주식 지수
            stock_prices = np.cumsum(np.random.normal(0, 0.5, days)) + 100
            stock_prices = np.clip(stock_prices, 80, 120)
            
            # 채권 지수
            bond_prices = np.cumsum(np.random.normal(0, 0.2, days)) + 100
            bond_prices = np.clip(bond_prices, 90, 110)
            
            # 금 지수
            gold_prices = np.cumsum(np.random.normal(0, 0.3, days)) + 100
            gold_prices = np.clip(gold_prices, 85, 115)
            
            # 현금(MMF) 지수
            cash_prices = np.linspace(100, 102, days)  # 안정적인 상승
            
            stock_index = pd.DataFrame({
                "일자": dates,
                "종가": stock_prices,
                "시가": stock_prices * np.random.uniform(0.99, 0.995, days),
                "고가": stock_prices * np.random.uniform(1.005, 1.01, days),
                "저가": stock_prices * np.random.uniform(0.99, 0.995, days)
            })
            
            bond_index = pd.DataFrame({
                "일자": dates,
                "종가": bond_prices,
                "시가": bond_prices * np.random.uniform(0.995, 0.998, days),
                "고가": bond_prices * np.random.uniform(1.002, 1.005, days),
                "저가": bond_prices * np.random.uniform(0.995, 0.998, days)
            })
            
            gold_index = pd.DataFrame({
                "일자": dates,
                "종가": gold_prices,
                "시가": gold_prices * np.random.uniform(0.99, 0.995, days),
                "고가": gold_prices * np.random.uniform(1.005, 1.01, days),
                "저가": gold_prices * np.random.uniform(0.99, 0.995, days)
            })
            
            cash_index = pd.DataFrame({
                "일자": dates,
                "종가": cash_prices,
                "시가": cash_prices,
                "고가": cash_prices,
                "저가": cash_prices
            })
            
            data = {
                "asset_data": {
                    "stock_index": stock_index,
                    "bond_index": bond_index,
                    "gold_index": gold_index,
                    "cash_index": cash_index
                }
            }
            
        else:
            return html.Div("지원되지 않는 전략입니다.")
        
        # 전략 실행
        result = strategy.run(data)
        
        if result.empty:
            return html.Div("전략 실행 결과가 없습니다.")
        
        # 결과 테이블 생성
        if strategy_value == "quant_king":
            # 자산배분 전략 결과 테이블
            table = dbc.Table.from_dataframe(
                result[["자산", "배분비율", "모멘텀", "변동성"]],
                striped=True,
                bordered=True,
                hover=True,
                responsive=True
            )
            
            # 원형 차트 추가
            fig = px.pie(
                result,
                values="배분비율",
                names="자산",
                title="자산배분 비율",
                hole=0.3
            )
            
            fig.update_layout(
                margin=dict(l=20, r=20, t=30, b=20),
                height=300
            )
            
            return html.Div([
                html.Div([
                    html.H5(f"시장 추세: {result['시장추세'].iloc[0]}", 
                           style={"color": "red" if result['시장추세'].iloc[0] == "상승" else "blue"}),
                    html.H6(f"기준일자: {result['기준일자'].iloc[0]}")
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col(table, width=6),
                    dbc.Col(dcc.Graph(figure=fig), width=6)
                ])
            ])
            
        else:
            # 일반 전략 결과 테이블
            result_columns = result.columns.tolist()
            display_columns = result_columns[:8]  # 처음 8개 컬럼만 표시
            
            table = dash_table.DataTable(
                data=result.to_dict("records"),
                columns=[
                    {"name": col, "id": col, "type": "numeric" if pd.api.types.is_numeric_dtype(result[col]) else "text"}
                    for col in display_columns
                ],
                style_table={"overflowX": "auto"},
                style_cell={
                    "textAlign": "center",
                    "padding": "5px",
                    "minWidth": "80px"
                },
                style_header={
                    "backgroundColor": "rgb(230, 230, 230)",
                    "fontWeight": "bold"
                },
                style_data_conditional=[
                    {
                        "if": {"filter_query": "{전일대비} > 0"},
                        "color": "red"
                    },
                    {
                        "if": {"filter_query": "{전일대비} < 0"},
                        "color": "blue"
                    },
                    {
                        "if": {"filter_query": "{등락률} > 0"},
                        "color": "red"
                    },
                    {
                        "if": {"filter_query": "{등락률} < 0"},
                        "color": "blue"
                    }
                ],
                page_size=10
            )
            
            return html.Div([
                html.H5(f"{strategy.name} 실행 결과 (상위 {len(result)} 종목)", className="mb-3"),
                table
            ])
    
    # 백테스트 실행 콜백
    @app.callback(
        Output("backtest-performance-chart", "figure"),
        [Input("run-backtest-button", "n_clicks")],
        [State("strategy-selector", "value"),
         State("backtest-period-slider", "value")]
    )
    def run_backtest(n_clicks, strategy_value, period_range):
        """선택한 전략의 백테스트 실행 및 결과 차트 생성"""
        if n_clicks is None:
            # 빈 차트 반환
            fig = go.Figure()
            fig.update_layout(
                title="백테스트를 실행해주세요",
                height=500
            )
            return fig
            
        # 백테스트 기간 설정
        start_year = period_range[0]
        end_year = period_range[1]
        total_years = end_year - start_year + 1
        
        # 데이터 생성 (실제 구현 시 API에서 데이터를 가져와야 함)
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=365 * end_year),
            end=datetime.now(),
            freq="M"
        )
        
        # 전략 이름 설정
        if strategy_value == "magic_formula":
            strategy_name = "마법공식"
        elif strategy_value == "kang_quality":
            strategy_name = "강환국 퀄리티 전략"
        elif strategy_value == "dual_momentum":
            strategy_name = "듀얼 모멘텀 전략"
        elif strategy_value == "piotroski_f":
            strategy_name = "피오트로스키 F-Score"
        elif strategy_value == "quant_king":
            strategy_name = "퀀트킹 자산배분"
        elif strategy_value == "multiple_factor":
            strategy_name = "다중 팩터 전략"
        else:
            strategy_name = "알 수 없는 전략"
            
        # 시뮬레이션 데이터 생성
        np.random.seed(42)  # 재현성을 위한 시드 설정
        
        # 전략 수익률 (연간 20% 내외, 변동 있음)
        strategy_returns = np.random.normal(0.016, 0.03, len(dates))  # 월 1.6% 평균 수익률
        strategy_cumulative = (1 + strategy_returns).cumprod() * 100
        
        # 코스피 수익률 (연간 8% 내외, 변동 있음)
        kospi_returns = np.random.normal(0.007, 0.025, len(dates))  # 월 0.7% 평균 수익률
        kospi_cumulative = (1 + kospi_returns).cumprod() * 100
        
        # 월별 투자금액 (1억원 시작)
        investment_amount = 100000000
        
        # 백테스트 차트 생성
        fig = go.Figure()
        
        # 전략 수익률 라인
        fig.add_trace(go.Scatter(
            x=dates,
            y=strategy_cumulative,
            name=f"{strategy_name}",
            line=dict(color="red", width=2)
        ))
        
        # KOSPI 수익률 라인
        fig.add_trace(go.Scatter(
            x=dates,
            y=kospi_cumulative,
            name="KOSPI",
            line=dict(color="blue", width=2)
        ))
        
        # 차트 레이아웃 설정
        fig.update_layout(
            title=f"{strategy_name} 백테스트 결과 ({start_year}년 ~ {end_year}년)",
            xaxis_title="날짜",
            yaxis_title="누적 수익률 (시작=100)",
            height=500,
            margin=dict(l=40, r=40, t=40, b=40),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            plot_bgcolor="white",
            xaxis=dict(
                gridcolor="lightgray",
                showgrid=True
            ),
            yaxis=dict(
                gridcolor="lightgray",
                showgrid=True
            )
        )
        
        # 성과 지표 계산
        strategy_cagr = (strategy_cumulative.iloc[-1] / 100) ** (1 / total_years) - 1
        kospi_cagr = (kospi_cumulative.iloc[-1] / 100) ** (1 / total_years) - 1
        
        strategy_std = np.std(strategy_returns) * np.sqrt(12)  # 연 변동성
        kospi_std = np.std(kospi_returns) * np.sqrt(12)  # 연 변동성
        
        strategy_sharpe = strategy_cagr / strategy_std
        kospi_sharpe = kospi_cagr / kospi_std
        
        # 최대 낙폭 계산
        strategy_drawdowns = []
        peak = strategy_cumulative[0]
        for value in strategy_cumulative:
            if value > peak:
                peak = value
            drawdown = (value - peak) / peak
            strategy_drawdowns.append(drawdown)
        
        strategy_max_drawdown = min(strategy_drawdowns) * 100
        
        # 성과 지표 주석 추가
        annotations = [
            dict(
                x=0.01,
                y=0.99,
                xref="paper",
                yref="paper",
                text=f"<b>성과 지표</b><br>" +
                     f"{strategy_name} CAGR: {strategy_cagr:.2%}<br>" +
                     f"KOSPI CAGR: {kospi_cagr:.2%}<br>" +
                     f"{strategy_name} 샤프비율: {strategy_sharpe:.2f}<br>" +
                     f"{strategy_name} 최대낙폭: {strategy_max_drawdown:.2f}%",
                showarrow=False,
                bgcolor="white",
                bordercolor="black",
                borderwidth=1,
                borderpad=4,
                font=dict(size=12)
            )
        ]
        
        fig.update_layout(annotations=annotations)
        
        return fig