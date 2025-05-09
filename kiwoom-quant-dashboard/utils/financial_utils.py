# utils/financial_utils.py
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any
from datetime import datetime


def calculate_returns(prices: Union[List[float], np.ndarray, pd.Series], 
                     method: str = 'simple') -> np.ndarray:
    """수익률 계산
    
    Args:
        prices: 가격 시계열
        method: 계산 방법 ('simple': 단순 수익률, 'log': 로그 수익률)
        
    Returns:
        np.ndarray: 수익률 배열
    """
    prices_array = np.array(prices)
    
    if method == 'simple':
        returns = np.diff(prices_array) / prices_array[:-1]
    elif method == 'log':
        returns = np.diff(np.log(prices_array))
    else:
        returns = np.diff(prices_array) / prices_array[:-1]
    
    return returns


def calculate_cagr(initial_value: float, final_value: float, years: float) -> float:
    """CAGR(연평균성장률) 계산
    
    Args:
        initial_value: 초기 가치
        final_value: 최종 가치
        years: 투자 기간(연)
        
    Returns:
        float: CAGR
    """
    if initial_value <= 0 or final_value <= 0 or years <= 0:
        return 0.0
    
    return (final_value / initial_value) ** (1 / years) - 1


def calculate_sharpe_ratio(returns: Union[List[float], np.ndarray], 
                          risk_free_rate: float = 0.02, 
                          periods_per_year: int = 252) -> float:
    """샤프 비율 계산
    
    Args:
        returns: 수익률 시계열
        risk_free_rate: 무위험 수익률 (연율화, 기본값: 2%)
        periods_per_year: 연간 기간 수 (일별=252, 주별=52, 월별=12)
        
    Returns:
        float: 샤프 비율
    """
    returns_array = np.array(returns)
    
    # 일별 무위험 수익률로 변환
    daily_risk_free = (1 + risk_free_rate) ** (1 / periods_per_year) - 1
    
    # 초과 수익률
    excess_returns = returns_array - daily_risk_free
    
    # 샤프 비율 계산
    sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(periods_per_year)
    
    return sharpe_ratio


def calculate_sortino_ratio(returns: Union[List[float], np.ndarray], 
                           risk_free_rate: float = 0.02, 
                           periods_per_year: int = 252) -> float:
    """소르티노 비율 계산
    
    Args:
        returns: 수익률 시계열
        risk_free_rate: 무위험 수익률 (연율화, 기본값: 2%)
        periods_per_year: 연간 기간 수 (일별=252, 주별=52, 월별=12)
        
    Returns:
        float: 소르티노 비율
    """
    returns_array = np.array(returns)
    
    # 일별 무위험 수익률로 변환
    daily_risk_free = (1 + risk_free_rate) ** (1 / periods_per_year) - 1
    
    # 초과 수익률
    excess_returns = returns_array - daily_risk_free
    
    # 하방 위험 (음수 수익률만 고려)
    downside_returns = excess_returns[excess_returns < 0]
    
    if len(downside_returns) == 0:
        return float('inf')  # 하방 위험이 없는 경우
    
    # 하방 표준편차
    downside_std = np.sqrt(np.mean(downside_returns ** 2))
    
    # 소르티노 비율 계산
    sortino_ratio = np.mean(excess_returns) / downside_std * np.sqrt(periods_per_year)
    
    return sortino_ratio


def calculate_max_drawdown(prices: Union[List[float], np.ndarray, pd.Series]) -> float:
    """최대 낙폭(MDD) 계산
    
    Args:
        prices: 가격 시계열
        
    Returns:
        float: 최대 낙폭
    """
    prices_array = np.array(prices)
    
    # 누적 최대값
    peak = np.maximum.accumulate(prices_array)
    
    # 낙폭
    drawdown = (prices_array - peak) / peak
    
    # 최대 낙폭
    max_drawdown = np.min(drawdown)
    
    return max_drawdown


def calculate_win_rate(trades: List[Dict[str, Any]]) -> float:
    """승률 계산
    
    Args:
        trades: 거래 내역 리스트 [{수익률: float, ...}, ...]
        
    Returns:
        float: 승률
    """
    if not trades:
        return 0.0
    
    # 수익 거래 수
    win_trades = sum(1 for trade in trades if trade.get('수익률', 0) > 0)
    
    # 승률 계산
    win_rate = win_trades / len(trades)
    
    return win_rate


def calculate_profit_factor(trades: List[Dict[str, Any]]) -> float:
    """손익비 계산
    
    Args:
        trades: 거래 내역 리스트 [{수익률: float, ...}, ...]
        
    Returns:
        float: 손익비
    """
    if not trades:
        return 0.0
    
    # 수익 및 손실 금액
    gross_profit = sum(trade.get('수익금액', 0) for trade in trades if trade.get('수익금액', 0) > 0)
    gross_loss = sum(abs(trade.get('수익금액', 0)) for trade in trades if trade.get('수익금액', 0) < 0)
    
    # 손익비 계산
    if gross_loss == 0:
        return float('inf')  # 손실이 없는 경우
    
    profit_factor = gross_profit / gross_loss
    
    return profit_factor


def calculate_per(price: float, eps: float) -> float:
    """PER(주가수익비율) 계산
    
    Args:
        price: 주가
        eps: 주당순이익
        
    Returns:
        float: PER
    """
    if eps == 0:
        return float('inf')
    
    return price / eps


def calculate_pbr(price: float, bps: float) -> float:
    """PBR(주가순자산비율) 계산
    
    Args:
        price: 주가
        bps: 주당순자산
        
    Returns:
        float: PBR
    """
    if bps == 0:
        return float('inf')
    
    return price / bps


def calculate_roe(net_income: float, equity: float) -> float:
    """ROE(자기자본이익률) 계산
    
    Args:
        net_income: 당기순이익
        equity: 자기자본
        
    Returns:
        float: ROE
    """
    if equity == 0:
        return 0.0
    
    return net_income / equity * 100


def calculate_roa(net_income: float, assets: float) -> float:
    """ROA(총자산이익률) 계산
    
    Args:
        net_income: 당기순이익
        assets: 총자산
        
    Returns:
        float: ROA
    """
    if assets == 0:
        return 0.0
    
    return net_income / assets * 100
