# analysis/performance.py
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union
import matplotlib.pyplot as plt


class PerformanceAnalyzer:
    """투자 성과 분석 클래스"""
    
    def __init__(self, portfolio_df: Optional[pd.DataFrame] = None, 
                benchmark_df: Optional[pd.DataFrame] = None):
        """성과 분석기 초기화
        
        Args:
            portfolio_df: 포트폴리오 데이터프레임 (필수 컬럼: '일자', '가치')
            benchmark_df: 벤치마크 데이터프레임 (필수 컬럼: '일자', '가치')
        """
        self.portfolio_df = portfolio_df
        self.benchmark_df = benchmark_df
        
    def set_portfolio_data(self, portfolio_df: pd.DataFrame):
        """포트폴리오 데이터 설정
        
        Args:
            portfolio_df: 포트폴리오 데이터프레임 (필수 컬럼: '일자', '가치')
        """
        self.portfolio_df = portfolio_df
        
    def set_benchmark_data(self, benchmark_df: pd.DataFrame):
        """벤치마크 데이터 설정
        
        Args:
            benchmark_df: 벤치마크 데이터프레임 (필수 컬럼: '일자', '가치')
        """
        self.benchmark_df = benchmark_df
        
    def calculate_returns(self, df: pd.DataFrame, value_column: str = '가치') -> pd.DataFrame:
        """수익률 계산
        
        Args:
            df: 데이터프레임
            value_column: 가치 컬럼명
            
        Returns:
            pd.DataFrame: 수익률이 추가된 데이터프레임
        """
        if df is None or df.empty or '일자' not in df.columns or value_column not in df.columns:
            return pd.DataFrame()
        
        result_df = df.copy()
        result_df = result_df.sort_values('일자')
        
        # 일간 수익률 계산
        result_df['daily_return'] = result_df[value_column].pct_change()
        
        # 누적 수익률 계산
        result_df['cumulative_return'] = (1 + result_df['daily_return']).cumprod() - 1
        
        return result_df
    
    def calculate_performance_metrics(self, returns_df: pd.DataFrame, risk_free_rate: float = 0.02) -> Dict[str, float]:
        """성과 지표 계산
        
        Args:
            returns_df: 수익률 데이터프레임
            risk_free_rate: 무위험 수익률 (연율화, 기본값: 2%)
            
        Returns:
            Dict[str, float]: 성과 지표
        """
        if returns_df is None or returns_df.empty or 'daily_return' not in returns_df.columns:
            return {}
        
        # 일별 수익률
        daily_returns = returns_df['daily_return'].dropna().values
        
        if len(daily_returns) < 2:
            return {}
        
        # 투자 기간 (연 단위)
        days = len(daily_returns)
        years = days / 252 if days >= 252 else days / days
        
        # 총 수익률
        total_return = returns_df['cumulative_return'].iloc[-1]
        
        # 연율화 수익률 (CAGR)
        cagr = (1 + total_return) ** (1 / max(years, 0.01)) - 1
        
        # 연율화 변동성
        annual_volatility = np.std(daily_returns) * np.sqrt(252)
        
        # 샤프 비율
        daily_risk_free = (1 + risk_free_rate) ** (1/252) - 1
        excess_returns = daily_returns - daily_risk_free
        sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252) if np.std(excess_returns) > 0 else 0
        
        # 소르티노 비율 (하방 위험만 고려)
        downside_returns = np.minimum(daily_returns - daily_risk_free, 0)
        downside_deviation = np.sqrt(np.mean(downside_returns ** 2)) * np.sqrt(252)
        sortino_ratio = np.mean(excess_returns) * np.sqrt(252) / downside_deviation if downside_deviation > 0 else 0
        
        # 최대 낙폭 (MDD)
        cumulative_returns = np.cumprod(1 + daily_returns)
        peak = np.maximum.accumulate(cumulative_returns)
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = np.min(drawdown) if len(drawdown) > 0 else 0
        
        # 수익률 대비 위험 (Return to Risk)
        return_to_risk = cagr / annual_volatility if annual_volatility > 0 else 0
        
        # 수익률 대비 최대 낙폭 (Return to Max Drawdown)
        return_to_drawdown = -cagr / max_drawdown if max_drawdown < 0 else 0
        
        return {
            'total_return': total_return,
            'cagr': cagr,
            'annual_volatility': annual_volatility,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'max_drawdown': max_drawdown,
            'return_to_risk': return_to_risk,
            'return_to_drawdown': return_to_drawdown
        }
    
    def analyze_performance(self, risk_free_rate: float = 0.02) -> Dict[str, Any]:
        """포트폴리오 성과 분석
        
        Args:
            risk_free_rate: 무위험 수익률 (연율화, 기본값: 2%)
            
        Returns:
            Dict[str, Any]: 성과 분석 결과
        """
        if self.portfolio_df is None or self.portfolio_df.empty:
            return {
                'success': False,
                'message': '포트폴리오 데이터가 없습니다.'
            }
        
        # 포트폴리오 수익률 계산
        portfolio_returns_df = self.calculate_returns(self.portfolio_df)
        portfolio_metrics = self.calculate_performance_metrics(portfolio_returns_df, risk_free_rate)
        
        result = {
            'success': True,
            'portfolio': {
                'returns': portfolio_returns_df,
                'metrics': portfolio_metrics
            }
        }
        
        # 벤치마크가 있는 경우 벤치마크 성과 분석
        if self.benchmark_df is not None and not self.benchmark_df.empty:
            benchmark_returns_df = self.calculate_returns(self.benchmark_df)
            benchmark_metrics = self.calculate_performance_metrics(benchmark_returns_df, risk_free_rate)
            
            result['benchmark'] = {
                'returns': benchmark_returns_df,
                'metrics': benchmark_metrics
            }
            
            # 포트폴리오와 벤치마크를 비교 분석
            if portfolio_metrics and benchmark_metrics:
                result['comparison'] = {
                    'alpha': portfolio_metrics['cagr'] - benchmark_metrics['cagr'],
                    'excess_return': portfolio_metrics['total_return'] - benchmark_metrics['total_return'],
                    'tracking_error': self._calculate_tracking_error(portfolio_returns_df, benchmark_returns_df),
                    'information_ratio': self._calculate_information_ratio(portfolio_returns_df, benchmark_returns_df)
                }
        
        return result
    
    def _calculate_tracking_error(self, portfolio_returns_df: pd.DataFrame, benchmark_returns_df: pd.DataFrame) -> float:
        """추적 오차 계산
        
        Args:
            portfolio_returns_df: 포트폴리오 수익률 데이터프레임
            benchmark_returns_df: 벤치마크 수익률 데이터프레임
            
        Returns:
            float: 추적 오차 (연율화)
        """
        # 공통 날짜에 대한 수익률만 사용
        common_dates = set(portfolio_returns_df['일자']).intersection(set(benchmark_returns_df['일자']))
        
        if not common_dates:
            return 0.0
        
        port_df = portfolio_returns_df[portfolio_returns_df['일자'].isin(common_dates)]
        bench_df = benchmark_returns_df[benchmark_returns_df['일자'].isin(common_dates)]
        
        port_df = port_df.sort_values('일자')
        bench_df = bench_df.sort_values('일자')
        
        # 초과 수익률 계산
        port_returns = port_df['daily_return'].values
        bench_returns = bench_df['daily_return'].values
        
        excess_returns = port_returns - bench_returns
        
        # 추적 오차 계산 (초과 수익률의 표준편차, 연율화)
        tracking_error = np.std(excess_returns) * np.sqrt(252)
        
        return tracking_error
    
    def _calculate_information_ratio(self, portfolio_returns_df: pd.DataFrame, benchmark_returns_df: pd.DataFrame) -> float:
        """정보 비율 계산
        
        Args:
            portfolio_returns_df: 포트폴리오 수익률 데이터프레임
            benchmark_returns_df: 벤치마크 수익률 데이터프레임
            
        Returns:
            float: 정보 비율
        """
        # 공통 날짜에 대한 수익률만 사용
        common_dates = set(portfolio_returns_df['일자']).intersection(set(benchmark_returns_df['일자']))
        
        if not common_dates:
            return 0.0
        
        port_df = portfolio_returns_df[portfolio_returns_df['일자'].isin(common_dates)]
        bench_df = benchmark_returns_df[benchmark_returns_df['일자'].isin(common_dates)]
        
        port_df = port_df.sort_values('일자')
        bench_df = bench_df.sort_values('일자')
        
        # 초과 수익률 계산
        port_returns = port_df['daily_return'].values
        bench_returns = bench_df['daily_return'].values
        
        excess_returns = port_returns - bench_returns
        
        # 연율화 초과 수익률
        annual_excess_return = np.mean(excess_returns) * 252
        
        # 추적 오차
        tracking_error = np.std(excess_returns) * np.sqrt(252)
        
        # 정보 비율 계산
        if tracking_error > 0:
            information_ratio = annual_excess_return / tracking_error
        else:
            information_ratio = 0.0
        
        return information_ratio
    
    def plot_performance_comparison(self, title: str = "포트폴리오 성과 비교", figsize: tuple = (12, 8)):
        """포트폴리오와 벤치마크 성과 비교 차트
        
        Args:
            title: 차트 제목
            figsize: 그림 크기
        """
        if self.portfolio_df is None or self.portfolio_df.empty:
            print("포트폴리오 데이터가 없습니다.")
            return
        
        # 포트폴리오 수익률 계산
        portfolio_returns_df = self.calculate_returns(self.portfolio_df)
        
        # 챠트 생성
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, gridspec_kw={'height_ratios': [3, 1]})
        
        # 수익률 차트
        ax1.plot(portfolio_returns_df['일자'], 
               (1 + portfolio_returns_df['cumulative_return']) * 100, 
               'b-', linewidth=2, label='Portfolio')
        
        # 벤치마크가 있는 경우 추가
        if self.benchmark_df is not None and not self.benchmark_df.empty:
            benchmark_returns_df = self.calculate_returns(self.benchmark_df)
            ax1.plot(benchmark_returns_df['일자'], 
                   (1 + benchmark_returns_df['cumulative_return']) * 100, 
                   'r--', linewidth=1.5, label='Benchmark')
        
        ax1.set_title(title, fontsize=16)
        ax1.set_ylabel('Value (Start=100)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='upper left')
        
        # 낙폭 차트
        peak = np.maximum.accumulate(1 + portfolio_returns_df['cumulative_return'])
        drawdown = ((1 + portfolio_returns_df['cumulative_return']) - peak) / peak
        
        ax2.fill_between(portfolio_returns_df['일자'], drawdown, 0, color='red', alpha=0.3)
        ax2.set_ylabel('Drawdown', fontsize=12)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # y축 범위 설정 (최대 낙폭에 여유 추가)
        min_dd = min(drawdown) if len(drawdown) > 0 else 0
        ax2.set_ylim([min(min_dd * 1.1, -0.05), 0.01])
        
        plt.tight_layout()
        plt.show()
        
        # 성과 지표 출력
        analysis_result = self.analyze_performance()
        
        if analysis_result['success']:
            port_metrics = analysis_result['portfolio']['metrics']
            
            print(f"=== 포트폴리오 성과 요약 ===")
            print(f"총 수익률: {port_metrics['total_return']:.2%}")
            print(f"연평균 수익률(CAGR): {port_metrics['cagr']:.2%}")
            print(f"연율화 변동성: {port_metrics['annual_volatility']:.2%}")
            print(f"샤프 비율: {port_metrics['sharpe_ratio']:.2f}")
            print(f"소르티노 비율: {port_metrics['sortino_ratio']:.2f}")
            print(f"최대 낙폭(MDD): {port_metrics['max_drawdown']:.2%}")
            
            if 'benchmark' in analysis_result and 'comparison' in analysis_result:
                bench_metrics = analysis_result['benchmark']['metrics']
                comparison = analysis_result['comparison']
                
                print(f"\n=== 벤치마크 대비 성과 ===")
                print(f"벤치마크 총 수익률: {bench_metrics['total_return']:.2%}")
                print(f"벤치마크 연평균 수익률: {bench_metrics['cagr']:.2%}")
                print(f"알파: {comparison['alpha']:.2%}")
                print(f"초과 수익률: {comparison['excess_return']:.2%}")
                print(f"추적 오차: {comparison['tracking_error']:.2%}")
                print(f"정보 비율: {comparison['information_ratio']:.2f}")

