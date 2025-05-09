# dashboard/components/forms.py
from dash import dcc, html
import dash_bootstrap_components as dbc
from typing import Dict, List, Optional, Any


def create_stock_search_form(id_prefix: str = 'stock-search') -> html.Div:
    """종목 검색 폼 생성
    
    Args:
        id_prefix: 입력 필드와 버튼의 ID 접두사
        
    Returns:
        html.Div: 종목 검색 폼
    """
    return html.Div([
        dbc.InputGroup([
            dbc.Input(
                id=f"{id_prefix}-input",
                type="text",
                placeholder="종목명 또는 코드 입력",
                className="form-control"
            ),
            dbc.Button(
                "검색", 
                id=f"{id_prefix}-button", 
                className="btn btn-primary"
            )
        ])
    ])


def create_strategy_param_form(strategy: str, parameters: Dict[str, Any]) -> html.Div:
    """전략 파라미터 폼 생성
    
    Args:
        strategy: 전략 ID
        parameters: 파라미터 딕셔너리 {파라미터명: 기본값}
        
    Returns:
        html.Div: 전략 파라미터 폼
    """
    form_items = []
    
    for param_name, default_value in parameters.items():
        # 파라미터 타입에 따른 입력 컴포넌트 생성
        if isinstance(default_value, bool):
            # 불리언 타입: 체크박스
            input_comp = dbc.Checkbox(
                id=f"{strategy}-{param_name}",
                checked=default_value,
                className="mb-2"
            )
        elif isinstance(default_value, int) or isinstance(default_value, float):
            # 숫자 타입: 슬라이더 또는 입력 필드
            if param_name.endswith('_n') or param_name == 'n_stocks':
                # 종목 수 관련 파라미터: 슬라이더
                input_comp = dcc.Slider(
                    id=f"{strategy}-{param_name}",
                    min=5,
                    max=50,
                    step=5,
                    value=default_value,
                    marks={i: str(i) for i in range(5, 51, 5)},
                    className="mb-2"
                )
            elif 'min_market_cap' in param_name:
                # 시가총액 관련 파라미터: 슬라이더
                input_comp = dcc.Slider(
                    id=f"{strategy}-{param_name}",
                    min=0,
                    max=10000,
                    step=100,
                    value=default_value / 100000000,  # 억 단위로 변환
                    marks={i: f"{i}억" for i in range(0, 10001, 1000)},
                    className="mb-2"
                )
            elif 'period' in param_name or 'window' in param_name:
                # 기간 관련 파라미터: 슬라이더
                input_comp = dcc.Slider(
                    id=f"{strategy}-{param_name}",
                    min=1,
                    max=24,
                    step=1,
                    value=default_value,
                    marks={i: str(i) for i in range(0, 25, 3)},
                    className="mb-2"
                )
            else:
                # 일반 숫자 파라미터: 입력 필드
                input_comp = dbc.Input(
                    id=f"{strategy}-{param_name}",
                    type="number",
                    value=default_value,
                    className="form-control mb-2"
                )
        elif isinstance(default_value, str):
            # 문자열 타입: 입력 필드 또는 드롭다운
            if param_name.endswith('_type') or param_name.endswith('_method'):
                # 타입 또는 메소드 선택: 드롭다운
                options = []
                if 'market_type' in param_name:
                    options = [
                        {"label": "KOSPI", "value": "0"},
                        {"label": "KOSDAQ", "value": "10"}
                    ]
                elif 'period_type' in param_name:
                    options = [
                        {"label": "일간", "value": "D"},
                        {"label": "주간", "value": "W"},
                        {"label": "월간", "value": "M"}
                    ]
                else:
                    options = [{"label": default_value, "value": default_value}]
                    
                input_comp = dcc.Dropdown(
                    id=f"{strategy}-{param_name}",
                    options=options,
                    value=default_value,
                    clearable=False,
                    className="mb-2"
                )
            else:
                # 일반 문자열: 입력 필드
                input_comp = dbc.Input(
                    id=f"{strategy}-{param_name}",
                    type="text",
                    value=default_value,
                    className="form-control mb-2"
                )
        else:
            # 기타 타입: 처리 불가
            continue
        
        # 파라미터 라벨과 입력 컴포넌트를 묶어서 폼 아이템 생성
        form_item = html.Div([
            html.Label(f"{param_name.replace('_', ' ').title()}:"),
            input_comp
        ], className="mb-3")
        
        form_items.append(form_item)
    
    # 폼 제출 버튼
    form_items.append(
        html.Button(
            "파라미터 적용",
            id=f"{strategy}-apply-button",
            className="btn btn-primary"
        )
    )
    
    return html.Div(form_items)