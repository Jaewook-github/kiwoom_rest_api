# dashboard/components/charts.py
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Union, Any


def create_price_chart(df: pd.DataFrame, x: str = '일자', y: Union[str, List[str]] = '종가',
                      title: str = '주가 차트', include_volume: bool = False) -> go.Figure:
    """주가 차트 생성
    
    Args:
        df: 데이터프레임
        x: x축 컬럼명
        y: y축 컬럼명 (문자열 또는 문자열 리스트)
        title: 차트 제목
        include_volume: 거래량 차트 포함 여부
        
    Returns:
        go.Figure: Plotly 그림 객체
    """
    if include_volume and '거래량' in df.columns:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                           vertical_spacing=0.03, row_heights=[0.7, 0.3])
        
        # 가격 차트
        if isinstance(y, str):
            fig.add_trace(go.Scatter(
                x=df[x], 
                y=df[y], 
                mode='lines', 
                name=y,
                line=dict(width=2)
            ), row=1, col=1)
        else:
            for col in y:
                fig.add_trace(go.Scatter(
                    x=df[x], 
                    y=df[col], 
                    mode='lines', 
                    name=col,
                    line=dict(width=1.5)
                ), row=1, col=1)
        
        # 거래량 차트
        colors = ['red' if close > open else 'blue' 
                  for open, close in zip(df.get('시가', [0]), df.get('종가', [0]))]
        
        fig.add_trace(go.Bar(
            x=df[x],
            y=df['거래량'],
            marker=dict(color=colors),
            name='거래량',
            showlegend=False
        ), row=2, col=1)
        
        # Y축 제목 설정
        fig.update_yaxes(title_text='가격', row=1, col=1)
        fig.update_yaxes(title_text='거래량', row=2, col=1)
        
    else:
        fig = go.Figure()
        
        # 가격 차트
        if isinstance(y, str):
            fig.add_trace(go.Scatter(
                x=df[x], 
                y=df[y], 
                mode='lines', 
                name=y,
                line=dict(width=2)
            ))
        else:
            for col in y:
                fig.add_trace(go.Scatter(
                    x=df[x], 
                    y=df[col], 
                    mode='lines', 
                    name=col,
                    line=dict(width=1.5)
                ))
    
    # 레이아웃 설정
    fig.update_layout(
        title=title,
        xaxis_title=x,
        height=500,
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig


def create_candlestick_chart(df: pd.DataFrame, x: str = '일자', open_col: str = '시가',
                           high_col: str = '고가', low_col: str = '저가', close_col: str = '종가',
                           title: str = '캔들스틱 차트', ma_periods: List[int] = [5, 20, 60],
                           include_volume: bool = True) -> go.Figure:
    """캔들스틱 차트 생성
    
    Args:
        df: 데이터프레임
        x: x축 컬럼명
        open_col: 시가 컬럼명
        high_col: 고가 컬럼명
        low_col: 저가 컬럼명
        close_col: 종가 컬럼명
        title: 차트 제목
        ma_periods: 이동평균 기간 리스트
        include_volume: 거래량 차트 포함 여부
        
    Returns:
        go.Figure: Plotly 그림 객체
    """
    if include_volume and '거래량' in df.columns:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                           vertical_spacing=0.03, row_heights=[0.7, 0.3])
    else:
        fig = go.Figure()
    
    # 캔들스틱 차트
    candlestick = go.Candlestick(
        x=df[x],
        open=df[open_col],
        high=df[high_col],
        low=df[low_col],
        close=df[close_col],
        name='가격',
        showlegend=False
    )
    
    if include_volume and '거래량' in df.columns:
        fig.add_trace(candlestick, row=1, col=1)
    else:
        fig.add_trace(candlestick)
    
    # 이동평균선 추가
    for period in ma_periods:
        ma_col = f'MA{period}'
        df[ma_col] = df[close_col].rolling(window=period).mean()
        
        ma_trace = go.Scatter(
            x=df[x],
            y=df[ma_col],
            mode='lines',
            name=f'{period}일 이동평균',
            line=dict(width=1.5)
        )
        
        if include_volume and '거래량' in df.columns:
            fig.add_trace(ma_trace, row=1, col=1)
        else:
            fig.add_trace(ma_trace)
    
    # 거래량 차트 추가
    if include_volume and '거래량' in df.columns:
        # 상승/하락 구분
        colors = ['red' if close > open else 'blue' 
                 for open, close in zip(df[open_col], df[close_col])]
        
        fig.add_trace(go.Bar(
            x=df[x],
            y=df['거래량'],
            marker=dict(color=colors),
            name='거래량',
            showlegend=False
        ), row=2, col=1)
        
        # Y축 제목 설정
        fig.update_yaxes(title_text='가격', row=1, col=1)
        fig.update_yaxes(title_text='거래량', row=2, col=1)
    
    # 레이아웃 설정
    fig.update_layout(
        title=title,
        xaxis_title=x,
        height=600,
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=50, r=50, t=50, b=50),
        xaxis_rangeslider_visible=False
    )
    
    return fig


def create_performance_chart(dates: List[str], portfolio_values: List[float], 
                           benchmark_values: Optional[List[float]] = None,
                           title: str = '포트폴리오 성과', display_drawdown: bool = True) -> go.Figure:
    """성과 차트 생성
    
    Args:
        dates: 날짜 리스트
        portfolio_values: 포트폴리오 가치 리스트
        benchmark_values: 벤치마크 가치 리스트 (없으면 None)
        title: 차트 제목
        display_drawdown: 낙폭 차트 표시 여부
        
    Returns:
        go.Figure: Plotly 그림 객체
    """
    if display_drawdown:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                           vertical_spacing=0.03, row_heights=[0.7, 0.3])
    else:
        fig = go.Figure()
    
    # 포트폴리오 수익률 계산
    portfolio_returns = np.array(portfolio_values) / portfolio_values[0] * 100
    
    # 벤치마크 수익률 계산
    if benchmark_values:
        benchmark_returns = np.array(benchmark_values) / benchmark_values[0] * 100
    
    # 수익률 차트
    portfolio_trace = go.Scatter(
        x=dates,
        y=portfolio_returns,
        mode='lines',
        name='포트폴리오',
        line=dict(width=2, color='red')
    )
    
    if display_drawdown:
        fig.add_trace(portfolio_trace, row=1, col=1)
    else:
        fig.add_trace(portfolio_trace)
    
    # 벤치마크 추가
    if benchmark_values:
        benchmark_trace = go.Scatter(
            x=dates,
            y=benchmark_returns,
            mode='lines',
            name='벤치마크',
            line=dict(width=2, color='blue')
        )
        
        if display_drawdown:
            fig.add_trace(benchmark_trace, row=1, col=1)
        else:
            fig.add_trace(benchmark_trace)
    
    # 낙폭 차트 추가
    if display_drawdown:
        # 포트폴리오 낙폭 계산
        peak = np.maximum.accumulate(portfolio_returns)
        drawdown = (portfolio_returns - peak) / peak * 100
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=drawdown,
            mode='lines',
            name='낙폭',
            fill='tozeroy',
            fillcolor='rgba(255, 0, 0, 0.2)',
            line=dict(color='red', width=1)
        ), row=2, col=1)
        
        # Y축 제목 설정
        fig.update_yaxes(title_text='수익률 (%)', row=1, col=1)
        fig.update_yaxes(title_text='낙폭 (%)', row=2, col=1)
    
    # 레이아웃 설정
    fig.update_layout(
        title=title,
        xaxis_title='날짜',
        height=600,
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig