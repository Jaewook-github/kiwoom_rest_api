# utils/visualization.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional, Union, Any, Tuple
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_price_chart(df: pd.DataFrame, x: str = '일자', y: Union[str, List[str]] = '종가',
                    title: str = '주가 차트', figsize: tuple = (12, 6)) -> plt.Figure:
    """주가 차트 그리기
    
    Args:
        df: 데이터프레임
        x: x축 컬럼명
        y: y축 컬럼명 (문자열 또는 문자열 리스트)
        title: 차트 제목
        figsize: 그림 크기
        
    Returns:
        plt.Figure: Matplotlib 그림 객체
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    if isinstance(y, str):
        ax.plot(df[x], df[y], linewidth=2)
    else:
        for col in y:
            ax.plot(df[x], df[col], label=col, linewidth=1.5)
        ax.legend()
    
    ax.set_title(title)
    ax.set_xlabel(x)
    ax.set_ylabel(y if isinstance(y, str) else 'Price')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    return fig


def plot_candlestick_chart(df: pd.DataFrame, x: str = '일자', open_col: str = '시가',
                          high_col: str = '고가', low_col: str = '저가', close_col: str = '종가',
                          title: str = '캔들스틱 차트', figsize: tuple = (12, 6)) -> plt.Figure:
    """캔들스틱 차트 그리기
    
    Args:
        df: 데이터프레임
        x: x축 컬럼명
        open_col: 시가 컬럼명
        high_col: 고가 컬럼명
        low_col: 저가 컬럼명
        close_col: 종가 컬럼명
        title: 차트 제목
        figsize: 그림 크기
        
    Returns:
        plt.Figure: Matplotlib 그림 객체
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # 날짜 정렬
    df = df.sort_values(by=x)
    
    # 최소 25개 데이터가 없으면 리샘플링
    if len(df) < 25:
        df_plot = df
    else:
        # 데이터가 많은 경우 리샘플링
        n_samples = min(50, len(df))
        idx = np.linspace(0, len(df) - 1, n_samples).astype(int)
        df_plot = df.iloc[idx]
    
    # 상승/하락 구분
    up = df_plot[close_col] > df_plot[open_col]
    down = df_plot[close_col] <= df_plot[open_col]
    
    # 캔들 그리기
    width = 0.8
    
    # 상승봉
    ax.bar(df_plot.index[up], df_plot[close_col][up] - df_plot[open_col][up],
          bottom=df_plot[open_col][up], width=width, color='red', alpha=0.7)
    
    # 하락봉
    ax.bar(df_plot.index[down], df_plot[close_col][down] - df_plot[open_col][down],
          bottom=df_plot[open_col][down], width=width, color='blue', alpha=0.7)
    
    # 꼬리 그리기
    ax.vlines(df_plot.index[up], df_plot[low_col][up], df_plot[high_col][up],
             color='red', linewidth=1)
    ax.vlines(df_plot.index[down], df_plot[low_col][down], df_plot[high_col][down],
             color='blue', linewidth=1)
    
    # x축 레이블 설정
    if isinstance(df_plot[x].iloc[0], pd.Timestamp):
        x_labels = [d.strftime('%Y-%m-%d') for d in df_plot[x]]
    else:
        x_labels = df_plot[x]
    
    plt.xticks(df_plot.index[::max(1, len(df_plot)//10)], 
              [x_labels[i] for i in range(0, len(x_labels), max(1, len(df_plot)//10))], 
              rotation=45)
    
    ax.set_title(title)
    ax.set_xlabel(x)
    ax.set_ylabel('Price')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    return fig


def plot_plotly_candlestick_chart(df: pd.DataFrame, x: str = '일자', open_col: str = '시가',
                                 high_col: str = '고가', low_col: str = '저가', close_col: str = '종가',
                                 volume_col: Optional[str] = '거래량', ma_periods: List[int] = [5, 20, 60],
                                 title: str = '캔들스틱 차트') -> go.Figure:
    """Plotly 캔들스틱 차트 그리기
    
    Args:
        df: 데이터프레임
        x: x축 컬럼명
        open_col: 시가 컬럼명
        high_col: 고가 컬럼명
        low_col: 저가 컬럼명
        close_col: 종가 컬럼명
        volume_col: 거래량 컬럼명 (None인 경우 거래량 차트 제외)
        ma_periods: 이동평균선 기간 리스트
        title: 차트 제목
        
    Returns:
        go.Figure: Plotly 그림 객체
    """
    # 날짜 정렬
    df = df.sort_values(by=x)
    
    # 서브플롯 생성 (거래량 포함 여부에 따라)
    if volume_col and volume_col in df.columns:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                           vertical_spacing=0.02, row_heights=[0.7, 0.3])
    else:
        fig = go.Figure()
    
    # 캔들스틱 차트
    fig.add_trace(go.Candlestick(
        x=df[x],
        open=df[open_col],
        high=df[high_col],
        low=df[low_col],
        close=df[close_col],
        name='Price',
        showlegend=False
    ))
    
    # 이동평균선 추가
    for period in ma_periods:
        ma_col = f'MA{period}'
        df[ma_col] = df[close_col].rolling(window=period).mean()
        
        fig.add_trace(go.Scatter(
            x=df[x],
            y=df[ma_col],
            mode='lines',
            name=f'{period}-day MA',
            line=dict(width=1)
        ))
    
    # 거래량 차트 추가
    if volume_col and volume_col in df.columns:
        # 상승/하락 색상 구분
        colors = ['red' if close > open else 'blue' 
                 for open, close in zip(df[open_col], df[close_col])]
        
        fig.add_trace(go.Bar(
            x=df[x],
            y=df[volume_col],
            name='Volume',
            marker=dict(color=colors, line=dict(width=0)),
            showlegend=False
        ), row=2, col=1)
    
    # 차트 레이아웃 설정
    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        height=600,
        template='plotly_white'
    )
    
    # Y축 설정
    if volume_col and volume_col in df.columns:
        fig.update_yaxes(title_text='Volume', row=2, col=1)
    
    return fig


def plot_correlation_matrix(df: pd.DataFrame, columns: Optional[List[str]] = None,
                           title: str = '상관관계 매트릭스', figsize: tuple = (10, 8)) -> plt.Figure:
    """상관관계 매트릭스 그리기
    
    Args:
        df: 데이터프레임
        columns: 상관관계를 계산할 컬럼 리스트 (None인 경우 모든 숫자형 컬럼 사용)
        title: 차트 제목
        figsize: 그림 크기
        
    Returns:
        plt.Figure: Matplotlib 그림 객체
    """
    # 숫자형 컬럼 선택
    if columns is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    else:
        numeric_cols = [col for col in columns if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]
    
    # 상관관계 계산
    corr_matrix = df[numeric_cols].corr()
    
    # 그림 생성
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)
    
    plt.title(title)
    plt.tight_layout()
    
    return fig


def plot_returns_distribution(returns: Union[List[float], np.ndarray, pd.Series],
                             title: str = '수익률 분포', figsize: tuple = (12, 6)) -> plt.Figure:
    """수익률 분포 그리기
    
    Args:
        returns: 수익률 시계열
        title: 차트 제목
        figsize: 그림 크기
        
    Returns:
        plt.Figure: Matplotlib 그림 객체
    """
    returns_array = np.array(returns)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # 히스토그램
    sns.histplot(returns_array, kde=True, ax=ax, color='skyblue')
    
    # 통계량
    mean = np.mean(returns_array)
    std = np.std(returns_array)
    skew = pd.Series(returns_array).skew()
    kurt = pd.Series(returns_array).kurtosis()
    
    # 텍스트 정보
    stats_text = (f"Mean: {mean:.4f}\nStd Dev: {std:.4f}\n"
                 f"Skewness: {skew:.4f}\nKurtosis: {kurt:.4f}")
    
    # 통계량 표시
    props = dict(boxstyle='round', facecolor='white', alpha=0.7)
    ax.text(0.05, 0.95, stats_text, transform=ax.transAxes, 
           verticalalignment='top', bbox=props)
    
    # 평균 및 표준편차 선 추가
    ax.axvline(mean, color='red', linestyle='--', alpha=0.7, label=f'Mean: {mean:.4f}')
    ax.axvline(mean + std, color='green', linestyle='--', alpha=0.5, label=f'+1 Std Dev: {mean+std:.4f}')
    ax.axvline(mean - std, color='green', linestyle='--', alpha=0.5, label=f'-1 Std Dev: {mean-std:.4f}')
    
    ax.set_title(title)
    ax.set_xlabel('Return')
    ax.set_ylabel('Frequency')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    return fig


def plot_drawdown_chart(prices: Union[List[float], np.ndarray, pd.Series],
                       dates: Optional[List[Union[str, datetime]]] = None,
                       title: str = '낙폭 차트', figsize: tuple = (12, 6)) -> plt.Figure:
    """낙폭 차트 그리기
    
    Args:
        prices: 가격 시계열
        dates: 날짜 시계열 (None인 경우 인덱스 사용)
        title: 차트 제목
        figsize: 그림 크기
        
    Returns:
        plt.Figure: Matplotlib 그림 객체
    """
    prices_array = np.array(prices)
    
    # 낙폭 계산
    peak = np.maximum.accumulate(prices_array)
    drawdown = (prices_array - peak) / peak * 100  # 백분율로 변환
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, gridspec_kw={'height_ratios': [2, 1]})
    
    # x축 데이터
    x = dates if dates is not None else np.arange(len(prices_array))
    
    # 가격 차트
    ax1.plot(x, prices_array, linewidth=2)
    ax1.set_title(title)
    ax1.set_ylabel('Price')
    ax1.grid(True, alpha=0.3)
    
    # 낙폭 차트
    ax2.fill_between(x, drawdown, 0, color='red', alpha=0.3)
    ax2.set_ylabel('Drawdown (%)')
    ax2.set_xlabel('Date' if dates is not None else 'Index')
    ax2.grid(True, alpha=0.3)
    
    # 최대 낙폭 표시
    max_dd = np.min(drawdown)
    max_dd_idx = np.argmin(drawdown)
    
    ax2.scatter(x[max_dd_idx], max_dd, color='darkred', s=50, zorder=5)
    ax2.text(x[max_dd_idx], max_dd, f' {max_dd:.2f}%', 
            verticalalignment='bottom', horizontalalignment='left')
    
    plt.tight_layout()
    
    return fig


def plot_asset_allocation(weights: Dict[str, float], title: str = '자산 배분',
                         figsize: tuple = (8, 8)) -> plt.Figure:
    """자산 배분 원형 차트 그리기
    
    Args:
        weights: 자산별 비중 딕셔너리 {'자산명': 비중}
        title: 차트 제목
        figsize: 그림 크기
        
    Returns:
        plt.Figure: Matplotlib 그림 객체
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # 데이터 준비
    labels = list(weights.keys())
    sizes = list(weights.values())
    
    # 색상 설정
    colors = plt.cm.tab10(np.arange(len(labels)) % 10)
    
    # 원형 차트
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=None, 
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        wedgeprops=dict(width=0.5)  # 도넛 차트
    )
    
    # 범례 설정
    ax.legend(
        wedges, 
        labels,
        title="Assets",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )
    
    # 텍스트 스타일 설정
    plt.setp(autotexts, size=10, weight="bold")
    
    ax.set_title(title, fontsize=14)
    
    plt.tight_layout()
    
    return fig


def plot_strategy_comparison(strategy_returns: Dict[str, pd.Series], 
                            benchmark_returns: Optional[pd.Series] = None,
                            title: str = '전략 비교', figsize: tuple = (12, 6)) -> plt.Figure:
    """전략 비교 차트 그리기
    
    Args:
        strategy_returns: 전략별 수익률 시리즈 딕셔너리 {'전략명': 수익률 시리즈}
        benchmark_returns: 벤치마크 수익률 시리즈 (None인 경우 제외)
        title: 차트 제목
        figsize: 그림 크기
        
    Returns:
        plt.Figure: Matplotlib 그림 객체
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # 전략별 누적 수익률 계산 및 그리기
    for name, returns in strategy_returns.items():
        cumulative_returns = (1 + returns).cumprod()
        ax.plot(cumulative_returns.index, cumulative_returns, label=name, linewidth=2)
    
    # 벤치마크 누적 수익률 추가
    if benchmark_returns is not None:
        cumulative_benchmark = (1 + benchmark_returns).cumprod()
        ax.plot(cumulative_benchmark.index, cumulative_benchmark, 
               label='Benchmark', linewidth=2, linestyle='--', color='black')
    
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Return')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # y축 로그 스케일 적용 (옵션)
    # ax.set_yscale('log')
    
    plt.tight_layout()
    
    return fig
