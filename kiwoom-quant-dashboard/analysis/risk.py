# analysis/risk.py
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union
import matplotlib.pyplot as plt
from scipy import stats


class RiskAnalyzer:
    """투자 리스크 분석 클래스"""
    
    def __init__(self, returns_df: Optional[pd.DataFrame] = None):
        """리스크 분석기 초기화
        
        Args:
            returns_df: 수익률 데이터프레임 (필수 컬럼: '일자', 'daily_return')
        """
        self.returns_df = returns_df
        
    def set_returns_data(self, returns_df: pd.DataFrame):
        """수익률 데이터 설정
        
        Args:
            returns_df: 수익률 데이터프레임 (필수 컬럼: '일자', 'daily_return')
        """
        self.returns_df = returns_df
        
    def calculate_value_at_risk(self, confidence_level: float = 0.95, 
                               time_horizon: int = 1, method: str = 'historical') -> float:
        """VaR(Value at Risk) 계산
        
        Args:
            confidence_level: 신뢰수준 (기본값: 95%)
            time_horizon: 시간 단위 (일) (기본값: 1일)
            method: 계산 방법 ('historical', 'parametric', 'monte_carlo')
            
        Returns:
            float: VaR 값
        """
        if self.returns_df is None or self.returns_df.empty or 'daily_return' not in self.returns_df.columns:
            return 0.0
        
        daily_returns = self.returns_df['daily_return'].dropna().values
        
        if len(daily_returns) < 30:  # 최소 30개 이상의 데이터 필요
            return 0.0
        
        # 계산 방법에 따른 VaR 계산
        if method == 'historical':
            # 역사적 시뮬레이션 방법
            percentile = 1 - confidence_level
            var = -np.percentile(daily_returns, percentile * 100)
        
        elif method == 'parametric':
            # 파라메트릭 방법 (정규분포 가정)
            mean = np.mean(daily_returns)
            std = np.std(daily_returns)
            z_score = stats.norm.ppf(confidence_level)
            var = -(mean - z_score * std)
        
        elif method == 'monte_carlo':
            # 몬테카를로 시뮬레이션 방법
            mean = np.mean(daily_returns)
            std = np.std(daily_returns)
            n_simulations = 10000
            simulated_returns = np.random.normal(mean, std, n_simulations)
            var = -np.percentile(simulated_returns, (1 - confidence_level) * 100)
        
        else:
            raise ValueError(f"지원되지 않는 계산 방법입니다: {method}")
        
        # 시간 단위 조정
        var_t = var * np.sqrt(time_horizon)
        
        return var_t
    
    def calculate_conditional_var(self, confidence_level: float = 0.95, 
                                time_horizon: int = 1, method: str = 'historical') -> float:
        """CVaR(Conditional Value at Risk) 계산
        
        Args:
            confidence_level: 신뢰수준 (기본값: 95%)
            time_horizon: 시간 단위 (일) (기본값: 1일)
            method: 계산 방법 ('historical', 'parametric', 'monte_carlo')
            
        Returns:
            float: CVaR 값
        """
        if self.returns_df is None or self.returns_df.empty or 'daily_return' not in self.returns_df.columns:
            return 0.0
        
        daily_returns = self.returns_df['daily_return'].dropna().values
        
        if len(daily_returns) < 30:  # 최소 30개 이상의 데이터 필요
            return 0.0
        
        # 계산 방법에 따른 CVaR 계산
        if method == 'historical':
            # 역사적 시뮬레이션 방법
            percentile = 1 - confidence_level
            var = -np.percentile(daily_returns, percentile * 100)
            cvar = -np.mean(daily_returns[daily_returns <= -var])
        
        elif method == 'parametric':
            # 파라메트릭 방법 (정규분포 가정)
            mean = np.mean(daily_returns)
            std = np.std(daily_returns)
            z_score = stats.norm.ppf(confidence_level)
            var = -(mean - z_score * std)
            
            # CVaR 계산 (조건부 기대값)
            z_cvar = stats.norm.pdf(z_score) / (1 - confidence_level)
            cvar = -(mean - z_cvar * std)
        
        elif method == 'monte_carlo':
            # 몬테카를로 시뮬레이션 방법
            mean = np.mean(daily_returns)
            std = np.std(daily_returns)
            n_simulations = 10000
            simulated_returns = np.random.normal(mean, std, n_simulations)
            var = -np.percentile(simulated_returns, (1 - confidence_level) * 100)
            cvar = -np.mean(simulated_returns[simulated_returns <= -var])
        
        else:
            raise ValueError(f"지원되지 않는 계산 방법입니다: {method}")
        
        # 시간 단위 조정
        cvar_t = cvar * np.sqrt(time_horizon)
        
        return cvar_t
    
    def calculate_downside_risk(self, threshold: float = 0.0) -> float:
        """하방 위험 계산
        
        Args:
            threshold: 기준 수익률 (기본값: 0%)
            
        Returns:
            float: 하방 위험 (연율화)
        """
        if self.returns_df is None or self.returns_df.empty or 'daily_return' not in self.returns_df.columns:
            return 0.0
        
        daily_returns = self.returns_df['daily_return'].dropna().values
        
        if len(daily_returns) < 2:
            return 0.0
        
        # 기준 수익률 이하의 수익률만 선택
        downside_returns = np.minimum(daily_returns - threshold, 0)
        
        # 하방 위험 계산 (연율화)
        downside_risk = np.sqrt(np.mean(downside_returns ** 2)) * np.sqrt(252)
        
        return downside_risk
    
    def calculate_beta(self, benchmark_returns_df: pd.DataFrame) -> float:
        """베타 계산
        
        Args:
            benchmark_returns_df: 벤치마크 수익률 데이터프레임 (필수 컬럼: '일자', 'daily_return')
            
        Returns:
            float: 베타
        """
        if (self.returns_df is None or self.returns_df.empty or 'daily_return' not in self.returns_df.columns or
            benchmark_returns_df is None or benchmark_returns_df.empty or 'daily_return' not in benchmark_returns_df.columns):
            return 0.0
        
        # 공통 날짜에 대한 수익률만 사용
        common_dates = set(self.returns_df['일자']).intersection(set(benchmark_returns_df['일자']))
        
        if not common_dates:
            return 0.0
        
        port_df = self.returns_df[self.returns_df['일자'].isin(common_dates)]
        bench_df = benchmark_returns_df[benchmark_returns_df['일자'].isin(common_dates)]
        
        port_df = port_df.sort_values('일자')
        bench_df = bench_df.sort_values('일자')
        
        # 베타 계산
        cov = np.cov(port_df['daily_return'].values, bench_df['daily_return'].values)[0, 1]
        var = np.var(bench_df['daily_return'].values)
        
        if var > 0:
            beta = cov / var
        else:
            beta = 0.0
        
        return beta
    
    def calculate_risk_metrics(self, benchmark_returns_df: Optional[pd.DataFrame] = None) -> Dict[str, float]:
        """리스크 지표 계산
        
        Args:
            benchmark_returns_df: 벤치마크 수익률 데이터프레임 (선택적)
            
        Returns:
            Dict[str, float]: 리스크 지표
        """
        if self.returns_df is None or self.returns_df.empty or 'daily_return' not in self.returns_df.columns:
            return {}
        
        daily_returns = self.returns_df['daily_return'].dropna().values
        
        if len(daily_returns) < 30:  # 최소 30개 이상의 데이터 필요
            return {}
        
        # 연율화 변동성
        annual_volatility = np.std(daily_returns) * np.sqrt(252)
        
        # VaR 계산 (95% 신뢰수준, 1일)
        var_95 = self.calculate_value_at_risk(confidence_level=0.95, time_horizon=1, method='historical')
        
        # CVaR 계산 (95% 신뢰수준, 1일)
        cvar_95 = self.calculate_conditional_var(confidence_level=0.95, time_horizon=1, method='historical')
        
        # 하방 위험
        downside_risk = self.calculate_downside_risk()
        
        # 최대 낙폭 (MDD)
        cumulative_returns = np.cumprod(1 + daily_returns)
        peak = np.maximum.accumulate(cumulative_returns)
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = np.min(drawdown) if len(drawdown) > 0 else 0
        
        # 왜도와 첨도
        skewness = stats.skew(daily_returns)
        kurtosis = stats.kurtosis(daily_returns)
        
        result = {
            'annual_volatility': annual_volatility,
            'var_95': var_95,
            'cvar_95': cvar_95,
            'downside_risk': downside_risk,
            'max_drawdown': max_drawdown,
            'skewness': skewness,
            'kurtosis': kurtosis
        }
        
        # 벤치마크가 있는 경우 추가 지표 계산
        if benchmark_returns_df is not None and not benchmark_returns_df.empty:
            beta = self.calculate_beta(benchmark_returns_df)
            result['beta'] = beta
            
            # 트레이너 비율
            if beta != 0:
                daily_risk_free = (1 + 0.02) ** (1/252) - 1  # 연 2% 무위험 수익률 가정
                avg_return = np.mean(daily_returns)
                excess_return = avg_return - daily_risk_free
                treynor_ratio = excess_return / beta * 252
                result['treynor_ratio'] = treynor_ratio
        
        return result
    
    def plot_return_distribution(self, title: str = "수익률 분포", figsize: tuple = (12, 8)):
        """수익률 분포 차트
        
        Args:
            title: 차트 제목
            figsize: 그림 크기
        """
        if self.returns_df is None or self.returns_df.empty or 'daily_return' not in self.returns_df.columns:
            print("수익률 데이터가 없습니다.")
            return
        
        daily_returns = self.returns_df['daily_return'].dropna().values
        
        if len(daily_returns) < 30:
            print("충분한 수익률 데이터가 없습니다.")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # 히스토그램
        ax1.hist(daily_returns, bins=50, density=True, alpha=0.6, color='blue')
        
        # 정규분포 피팅
        mu, sigma = stats.norm.fit(daily_returns)
        x = np.linspace(min(daily_returns), max(daily_returns), 100)
        ax1.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', linewidth=2)
        
        ax1.set_title(f"{title} - 히스토그램", fontsize=14)
        ax1.set_xlabel('일간 수익률', fontsize=12)
        ax1.set_ylabel('빈도', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # 통계량
        ax1.text(0.05, 0.95, f"평균: {np.mean(daily_returns):.4f}\n표준편차: {np.std(daily_returns):.4f}\n왜도: {stats.skew(daily_returns):.4f}\n첨도: {stats.kurtosis(daily_returns):.4f}",
                transform=ax1.transAxes, va='top', fontsize=10, bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
        
        # Q-Q 플롯
        stats.probplot(daily_returns, plot=ax2)
        ax2.set_title(f"{title} - Q-Q 플롯", fontsize=14)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        