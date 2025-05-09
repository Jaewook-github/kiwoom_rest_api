# dashboard/components/tables.py
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
from typing import List, Dict, Optional, Any


def create_stock_table(df: pd.DataFrame, columns: Optional[List[str]] = None,
                      id: str = 'stock-table') -> dash_table.DataTable:
    """주식 정보 테이블 생성
    
    Args:
        df: 데이터프레임
        columns: 표시할 컬럼 목록 (기본값: 모든 컬럼)
        id: 테이블 ID
        
    Returns:
        dash_table.DataTable: 주식 테이블
    """
    if df.empty:
        return dash_table.DataTable(id=id)
    
    if columns:
        display_columns = [col for col in columns if col in df.columns]
        df_display = df[display_columns]
    else:
        df_display = df
    
    # 컬럼 형식 정의
    columns = []
    for col in df_display.columns:
        col_def = {"name": col, "id": col}
        
        # 숫자형 컬럼 형식 지정
        if pd.api.types.is_numeric_dtype(df_display[col]):
            if '등락률' in col or '수익률' in col or '비율' in col:
                col_def["type"] = "numeric"
                col_def["format"] = {"specifier": "+.2f"}
            elif '가격' in col or '현재가' in col or '평균가' in col:
                col_def["type"] = "numeric"
                col_def["format"] = {"specifier": ","}
            else:
                col_def["type"] = "numeric"
                col_def["format"] = {"specifier": ",.2f"}
                
        columns.append(col_def)
    
    # 테이블 생성
    table = dash_table.DataTable(
        id=id,
        data=df_display.to_dict('records'),
        columns=columns,
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
    
    return table


def create_financial_table(df: pd.DataFrame, columns: Optional[List[str]] = None,
                         id: str = 'financial-table') -> dash_table.DataTable:
    """재무 정보 테이블 생성
    
    Args:
        df: 데이터프레임
        columns: 표시할 컬럼 목록 (기본값: 모든 컬럼)
        id: 테이블 ID
        
    Returns:
        dash_table.DataTable: 재무 정보 테이블
    """
    if df.empty:
        return dash_table.DataTable(id=id)
    
    if columns:
        display_columns = [col for col in columns if col in df.columns]
        df_display = df[display_columns]
    else:
        df_display = df
    
    # 컬럼 형식 정의
    columns = []
    for col in df_display.columns:
        col_def = {"name": col, "id": col}
        
        # 숫자형 컬럼 형식 지정
        if pd.api.types.is_numeric_dtype(df_display[col]):
            if '비율' in col or 'PER' in col or 'PBR' in col or 'ROE' in col or 'ROA' in col:
                col_def["type"] = "numeric"
                col_def["format"] = {"specifier": ".2f"}
            elif '시가총액' in col or '자산' in col or '부채' in col or '자본' in col or '매출' in col or '이익' in col:
                col_def["type"] = "numeric"
                col_def["format"] = {"specifier": ","}
            else:
                col_def["type"] = "numeric"
                col_def["format"] = {"specifier": ",.2f"}
                
        columns.append(col_def)
    
    # 테이블 생성
    table = dash_table.DataTable(
        id=id,
        data=df_display.to_dict('records'),
        columns=columns,
        style_table={"overflowX": "auto"},
        style_cell={
            "textAlign": "center",
            "padding": "5px",
            "minWidth": "100px"
        },
        style_header={
            "backgroundColor": "rgb(230, 230, 230)",
            "fontWeight": "bold"
        },
        page_size=10
    )
    
    return table


def create_trade_history_table(df: pd.DataFrame, id: str = 'trade-history-table') -> dash_table.DataTable:
    """거래 내역 테이블 생성
    
    Args:
        df: 데이터프레임
        id: 테이블 ID
        
    Returns:
        dash_table.DataTable: 거래 내역 테이블
    """
    if df.empty:
        return dash_table.DataTable(id=id)
    
    # 컬럼 형식 정의
    columns = []
    for col in df.columns:
        col_def = {"name": col, "id": col}
        
        # 숫자형 컬럼 형식 지정
        if pd.api.types.is_numeric_dtype(df[col]):
            if '가격' in col:
                col_def["type"] = "numeric"
                col_def["format"] = {"specifier": ","}
            elif '수량' in col:
                col_def["type"] = "numeric"
                col_def["format"] = {"specifier": ","}
            elif '금액' in col or '수수료' in col:
                col_def["type"] = "numeric"
                col_def["format"] = {"specifier": ","}
            else:
                col_def["type"] = "numeric"
                col_def["format"] = {"specifier": ",.2f"}
                
        columns.append(col_def)
    
    # 테이블 생성
    table = dash_table.DataTable(
        id=id,
        data=df.to_dict('records'),
        columns=columns,
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
                "if": {"filter_query": "{거래유형} = 매수"},
                "color": "red"
            },
            {
                "if": {"filter_query": "{거래유형} = 매도"},
                "color": "blue"
            }
        ],
        page_size=20
    )
    
    return table