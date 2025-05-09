"""
키움증권 REST API 퀀트 대시보드 프로젝트의 분석 모듈
- 백테스팅 엔진
- 성과 분석
- 리스크 분석
"""

# analysis/backtest.py
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union, Callable
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings

# 경고 무시 설정
warnings.filterwarnings("ignore", category=RuntimeWarning)


class BacktestEngine:
    """퀀트 전략 백테스트 엔진"""
    
    def __init__(self, initial_capital: float = 100000000):
        """백테스트 엔진 초기화
        
        Args:
            initial_capital: 초기 자본금 (기본값: 1억원)
        """
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.portfolio = {}  # {종목코드: {수량, 매수가, 현재가, 평가금액}}
        self.cash = initial_capital
        self.trades = []  # 거래 기록
        self.portfolio_values = []  # 포트폴리오 가치 기록
        self.benchmark_values = []  # 벤치마크 가치 기록
        self.dates = []  # 날짜 기록
        
    def reset(self):
        """백테스트 상태 초기화"""
        self.current_capital = self.initial_capital
        self.portfolio = {}
        self.cash = self.initial_capital
        self.trades = []
        self.portfolio_values = []
        self.benchmark_values = []
        self.dates = []
        
    def run_backtest(self, strategy_func: Callable, price_data: Dict[str, pd.DataFrame], 
                     rebalance_freq: str = 'M', start_date: Optional[str] = None, 
                     end_date: Optional[str] = None, benchmark_data: Optional[pd.DataFrame] = None,
                     commission_rate: float = 0.00015, slippage_rate: float = 0.0005) -> Dict[str, Any]:
        """백테스트 실행
        
        Args:
            strategy_func: 전략 함수 (날짜를 입력받아 {종목코드: 비중} 형태의 포트폴리오 반환)
            price_data: 종목별 가격 데이터 딕셔너리 {종목코드: 가격데이터프레임}
            rebalance_freq: 리밸런싱 주기 ('D': 일간, 'W': 주간, 'M': 월간, 'Q': 분기)
            start_date: 백테스트 시작일 (YYYY-MM-DD)
            end_date: 백테스트 종료일 (YYYY-MM-DD)
            benchmark_data: 벤치마크 가격 데이터
            commission_rate: 거래 수수료율 (기본값: 0.015%)
            slippage_rate: 슬리피지율 (기본값: 0.05%)
            
        Returns:
            Dict[str, Any]: 백테스트 결과
        """
        self.reset()
        
        # 전체 데이터를 통합하여 날짜 범위 설정
        all_dates = set()
        for code, df in price_data.items():
            if not df.empty and '일자' in df.columns:
                all_dates.update(df['일자'])
        
        all_dates = sorted(list(all_dates))
        
        if start_date:
            start_dt = pd.to_datetime(start_date)
            all_dates = [d for d in all_dates if d >= start_dt]
            
        if end_date:
            end_dt = pd.to_datetime(end_date)
            all_dates = [d for d in all_dates if d <= end_dt]
        
        # 리밸런싱 날짜 결정
        if rebalance_freq == 'D':
            rebalance_dates = all_dates
        elif rebalance_freq == 'W':
            # 각 주의 첫 거래일
            rebalance_dates = [d for i, d in enumerate(all_dates) if i == 0 or d.weekday() < all_dates[i-1].weekday()]
        elif rebalance_freq == 'M':
            # 각 월의 첫 거래일
            rebalance_dates = [d for i, d in enumerate(all_dates) if i == 0 or d.month != all_dates[i-1].month]
        elif rebalance_freq == 'Q':
            # 각 분기의 첫 거래일
            rebalance_dates = [d for i, d in enumerate(all_dates) if i == 0 or (d.month - 1) // 3 != (all_dates[i-1].month - 1) // 3]
        else:
            rebalance_dates = all_dates
        
        # 매일 포트폴리오 가치 기록 및 리밸런싱 날짜에 리밸런싱 수행
        for current_date in all_dates:
            # 현재 날짜의 가격 정보 수집
            current_prices = {}
            for code, df in price_data.items():
                if not df.empty and '일자' in df.columns and '종가' in df.columns:
                    # 현재 날짜 데이터 찾기
                    price_at_date = df[df['일자'] == current_date]
                    if not price_at_date.empty:
                        current_prices[code] = price_at_date['종가'].iloc[0]
            
            # 포트폴리오 가치 업데이트
            portfolio_value = self.cash
            for code, info in self.portfolio.items():
                if code in current_prices:
                    current_price = current_prices[code]
                    info['현재가'] = current_price
                    info['평가금액'] = info['수량'] * current_price
                    portfolio_value += info['평가금액']
            
            # 벤치마크 가치 업데이트
            benchmark_value = None
            if benchmark_data is not None and not benchmark_data.empty and '일자' in benchmark_data.columns:
                benchmark_at_date = benchmark_data[benchmark_data['일자'] == current_date]
                if not benchmark_at_date.empty and '종가' in benchmark_at_date.columns:
                    benchmark_price = benchmark_at_date['종가'].iloc[0]
                    if len(self.benchmark_values) == 0:
                        benchmark_value = self.initial_capital
                    else:
                        prev_benchmark_price = benchmark_data[benchmark_data['일자'] == self.dates[-1]]['종가'].iloc[0]
                        benchmark_value = self.benchmark_values[-1] * (benchmark_price / prev_benchmark_price)
            
            # 기록 저장
            self.dates.append(current_date)
            self.portfolio_values.append(portfolio_value)
            if benchmark_value is not None:
                self.benchmark_values.append(benchmark_value)
            elif len(self.benchmark_values) > 0:
                self.benchmark_values.append(self.benchmark_values[-1])
            else:
                self.benchmark_values.append(self.initial_capital)
            
            # 리밸런싱 수행
            if current_date in rebalance_dates:
                # 전략 실행하여 새로운 포트폴리오 비중 얻기
                target_weights = strategy_func(current_date)
                
                if target_weights:
                    self._rebalance_portfolio(target_weights, current_prices, current_date, commission_rate, slippage_rate)
        
        # 백테스트 결과 계산
        return self._calculate_performance()
    
    def _rebalance_portfolio(self, target_weights: Dict[str, float], current_prices: Dict[str, float], 
                            current_date: datetime, commission_rate: float, slippage_rate: float):
        """포트폴리오 리밸런싱 수행
        
        Args:
            target_weights: 목표 포트폴리오 비중 {종목코드: 비중}
            current_prices: 현재 가격 {종목코드: 가격}
            current_date: 현재 날짜
            commission_rate: 거래 수수료율
            slippage_rate: 슬리피지율
        """
        # 현재 포트폴리오 가치 계산
        portfolio_value = self.cash
        for code, info in self.portfolio.items():
            if code in current_prices:
                portfolio_value += info['수량'] * current_prices[code]
        
        # 새로운 포트폴리오 구성
        new_portfolio = {}
        for code, weight in target_weights.items():
            if code in current_prices:
                price = current_prices[code]
                target_value = portfolio_value * weight
                target_quantity = int(target_value / price)  # 정수 수량으로 변환
                
                # 거래 비용을 고려한 실제 매수 가능 수량 계산
                max_quantity = int(target_value / (price * (1 + commission_rate + slippage_rate)))
                target_quantity = min(target_quantity, max_quantity)
                
                # 현재 보유 수량과 비교하여 매매 수량 결정
                current_quantity = self.portfolio.get(code, {}).get('수량', 0)
                trade_quantity = target_quantity - current_quantity
                
                if trade_quantity != 0:
                    # 거래 기록 추가
                    trade_price = price * (1 + slippage_rate) if trade_quantity > 0 else price * (1 - slippage_rate)
                    commission = abs(trade_quantity * trade_price * commission_rate)
                    trade_amount = trade_quantity * trade_price + commission
                    
                    self.trades.append({
                        '일자': current_date,
                        '종목코드': code,
                        '거래유형': '매수' if trade_quantity > 0 else '매도',
                        '거래수량': abs(trade_quantity),
                        '거래가격': trade_price,
                        '거래금액': abs(trade_amount),
                        '수수료': commission
                    })
                    
                    # 현금 업데이트
                    self.cash -= trade_amount
                
                if target_quantity > 0:
                    # 포트폴리오 업데이트
                    avg_price = (self.portfolio.get(code, {}).get('매수가', 0) * current_quantity + 
                               trade_price * max(0, trade_quantity)) / max(1, current_quantity + max(0, trade_quantity))
                    
                    new_portfolio[code] = {
                        '수량': target_quantity,
                        '매수가': avg_price,
                        '현재가': price,
                        '평가금액': target_quantity * price
                    }
        
        self.portfolio = new_portfolio
    
    def _calculate_performance(self) -> Dict[str, Any]:
        """백테스트 성과 계산
        
        Returns:
            Dict[str, Any]: 성과 지표
        """
        if not self.portfolio_values or len(self.portfolio_values) < 2:
            return {
                'success': False,
                'message': '백테스트 데이터가 충분하지 않습니다.'
            }
        
        # 일별 수익률 계산
        daily_returns = []
        for i in range(1, len(self.portfolio_values)):
            daily_return = self.portfolio_values[i] / self.portfolio_values[i-1] - 1
            daily_returns.append(daily_return)
        
        daily_returns = np.array(daily_returns)
        
        # 벤치마크 일별 수익률 계산
        benchmark_daily_returns = []
        if self.benchmark_values and len(self.benchmark_values) >= 2:
            for i in range(1, len(self.benchmark_values)):
                daily_return = self.benchmark_values[i] / self.benchmark_values[i-1] - 1
                benchmark_daily_returns.append(daily_return)
        
        benchmark_daily_returns = np.array(benchmark_daily_returns)
        
        # 주요 성과 지표 계산
        total_days = len(self.portfolio_values) - 1
        years = total_days / 252 if total_days >= 252 else total_days / total_days
        
        # 총 수익률
        total_return = self.portfolio_values[-1] / self.portfolio_values[0] - 1
        
        # 연율화 수익률 (CAGR)
        cagr = (1 + total_return) ** (1 / max(years, 0.01)) - 1
        
        # 연율화 변동성
        annual_volatility = np.std(daily_returns) * np.sqrt(252)
        
        # 샤프 비율
        risk_free_rate = 0.02  # 무위험 수익률 (연 2% 가정)
        daily_risk_free = (1 + risk_free_rate) ** (1/252) - 1
        excess_returns = daily_returns - daily_risk_free
        sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252) if np.std(excess_returns) > 0 else 0
        
        # 최대 낙폭 (MDD)
        cumulative_returns = np.cumprod(1 + daily_returns)
        peak = np.maximum.accumulate(cumulative_returns)
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = np.min(drawdown) if len(drawdown) > 0 else 0
        
        # 벤치마크 대비 성과
        benchmark_total_return = None
        benchmark_cagr = None
        benchmark_volatility = None
        benchmark_sharpe = None
        benchmark_mdd = None
        
        if len(benchmark_daily_returns) > 0:
            benchmark_total_return = self.benchmark_values[-1] / self.benchmark_values[0] - 1
            benchmark_cagr = (1 + benchmark_total_return) ** (1 / max(years, 0.01)) - 1
            benchmark_volatility = np.std(benchmark_daily_returns) * np.sqrt(252)
            
            benchmark_excess_returns = benchmark_daily_returns - daily_risk_free
            benchmark_sharpe = (np.mean(benchmark_excess_returns) / np.std(benchmark_excess_returns) * 
                              np.sqrt(252) if np.std(benchmark_excess_returns) > 0 else 0)
            
            benchmark_cumulative = np.cumprod(1 + benchmark_daily_returns)
            benchmark_peak = np.maximum.accumulate(benchmark_cumulative)
            benchmark_drawdown = (benchmark_cumulative - benchmark_peak) / benchmark_peak
            benchmark_mdd = np.min(benchmark_drawdown) if len(benchmark_drawdown) > 0 else 0
        
        # 승률, 손익비 계산
        win_trades = [t for t in self.trades if (t['거래유형'] == '매도' and 
                                              t['거래가격'] > self.portfolio.get(t['종목코드'], {}).get('매수가', 0))]
        lose_trades = [t for t in self.trades if (t['거래유형'] == '매도' and 
                                               t['거래가격'] <= self.portfolio.get(t['종목코드'], {}).get('매수가', 0))]
        
        win_rate = len(win_trades) / max(1, len(win_trades) + len(lose_trades))
        
        avg_win = np.mean([t['거래가격'] / self.portfolio.get(t['종목코드'], {}).get('매수가', 1) - 1 
                         for t in win_trades]) if win_trades else 0
        avg_loss = np.mean([t['거래가격'] / self.portfolio.get(t['종목코드'], {}).get('매수가', 1) - 1 
                          for t in lose_trades]) if lose_trades else 0
        
        profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
        
        # 결과 반환
        result = {
            'success': True,
            'initial_capital': self.initial_capital,
            'final_capital': self.portfolio_values[-1],
            'total_return': total_return,
            'cagr': cagr,
            'annual_volatility': annual_volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'portfolio_values': self.portfolio_values,
            'dates': [d.strftime('%Y-%m-%d') for d in self.dates],
            'trades': self.trades,
            'benchmark': {
                'values': self.benchmark_values,
                'total_return': benchmark_total_return,
                'cagr': benchmark_cagr,
                'volatility': benchmark_volatility,
                'sharpe_ratio': benchmark_sharpe,
                'max_drawdown': benchmark_mdd
            }
        }
        
        return result
    
    def plot_performance(self, title: str = "백테스트 성과", figsize: tuple = (12, 8), 
                        show_benchmark: bool = True, show_drawdown: bool = True):
        """백테스트 성과 차트 출력
        
        Args:
            title: 차트 제목
            figsize: 그림 크기
            show_benchmark: 벤치마크 표시 여부
            show_drawdown: 낙폭 차트 표시 여부
        """
        if not self.portfolio_values or len(self.portfolio_values) < 2:
            print("백테스트 데이터가 충분하지 않습니다.")
            return
        
        # 포트폴리오 및 벤치마크 데이터 준비
        dates = pd.to_datetime(self.dates)
        portfolio_values = np.array(self.portfolio_values)
        portfolio_returns = portfolio_values / portfolio_values[0]
        
        # 낙폭 계산
        portfolio_peak = np.maximum.accumulate(portfolio_returns)
        portfolio_drawdown = (portfolio_returns - portfolio_peak) / portfolio_peak
        
        # 차트 설정
        if show_drawdown:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, gridspec_kw={'height_ratios': [3, 1]})
        else:
            fig, ax1 = plt.subplots(figsize=figsize)
        
        # 수익률 차트
        ax1.plot(dates, portfolio_returns, 'b-', linewidth=2, label='Portfolio')
        
        if show_benchmark and self.benchmark_values and len(self.benchmark_values) == len(self.portfolio_values):
            benchmark_values = np.array(self.benchmark_values)
            benchmark_returns = benchmark_values / benchmark_values[0]
            ax1.plot(dates, benchmark_returns, 'r--', linewidth=1.5, label='Benchmark')
        
        ax1.set_title(title, fontsize=16)
        ax1.set_ylabel('Cumulative Return', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='upper left')
        
        # 낙폭 차트
        if show_drawdown:
            ax2.fill_between(dates, portfolio_drawdown, 0, color='red', alpha=0.3)
            ax2.set_ylabel('Drawdown', fontsize=12)
            ax2.set_xlabel('Date', fontsize=12)
            ax2.grid(True, alpha=0.3)
            
            # y축 범위 설정 (최대 낙폭에 여유 추가)
            min_dd = min(portfolio_drawdown) if len(portfolio_drawdown) > 0 else 0
            ax2.set_ylim([min(min_dd * 1.1, -0.05), 0.01])
        else:
            ax1.set_xlabel('Date', fontsize=12)
        
        plt.tight_layout()
        plt.show()
        
        # 주요 성과 지표 출력
        performance = self._calculate_performance()
        
        print(f"=== 백테스트 성과 요약 ===")
        print(f"기간: {self.dates[0].strftime('%Y-%m-%d')} ~ {self.dates[-1].strftime('%Y-%m-%d')}")
        print(f"총 수익률: {performance['total_return']:.2%}")
        print(f"연평균 수익률(CAGR): {performance['cagr']:.2%}")
        print(f"연율화 변동성: {performance['annual_volatility']:.2%}")
        print(f"샤프 비율: {performance['sharpe_ratio']:.2f}")
        print(f"최대 낙폭(MDD): {performance['max_drawdown']:.2%}")
        print(f"승률: {performance['win_rate']:.2%}")
        print(f"손익비: {performance['profit_factor']:.2f}")
        
        if show_benchmark and 'benchmark' in performance and performance['benchmark']['total_return'] is not None:
            print(f"\n=== 벤치마크 대비 성과 ===")
            print(f"벤치마크 총 수익률: {performance['benchmark']['total_return']:.2%}")
            print(f"벤치마크 연평균 수익률: {performance['benchmark']['cagr']:.2%}")
            print(f"벤치마크 연율화 변동성: {performance['benchmark']['volatility']:.2%}")
            print(f"벤치마크 샤프 비율: {performance['benchmark']['sharpe_ratio']:.2f}")
            print(f"벤치마크 최대 낙폭: {performance['benchmark']['max_drawdown']:.2%}")
            print(f"초과 수익률: {performance['total_return'] - performance['benchmark']['total_return']:.2%}")

