"""
백테스팅 모듈
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Set, Callable
import pandas as pd
import numpy as np

from ..utils.logger import logger
from ..utils.decorators import async_measure_time
from ..analysis.stock_analyzer import StockAnalyzer


class Backtester:
    """백테스팅 클래스"""

    def __init__(self, stock_analyzer: StockAnalyzer, initial_capital: float = 10000000):
        """
        초기화

        Args:
            stock_analyzer: 종목 분석기 인스턴스
            initial_capital: 초기 자본금
        """
        self.stock_analyzer = stock_analyzer
        self.initial_capital = initial_capital

        # 백테스트 결과
        self.results = {}

        logger.info(f"백테스터 초기화 완료 - 초기 자본금: {initial_capital:,.0f}원")

    @async_measure_time
    async def run_backtest(self,
                           stock_code: str,
                           start_date: str,
                           end_date: str,
                           buy_strategy: Callable[[pd.DataFrame, int], bool],
                           sell_strategy: Callable[[pd.DataFrame, int, Dict[str, Any]], bool],
                           stop_loss_pct: float = -5.0,
                           take_profit_pct: float = 5.0) -> Dict[str, Any]:
        """
        백테스트 실행

        Args:
            stock_code: 종목코드
            start_date: 시작일 (YYYY-MM-DD)
            end_date: 종료일 (YYYY-MM-DD)
            buy_strategy: 매수 전략 함수
            sell_strategy: 매도 전략 함수
            stop_loss_pct: 손절 비율 (%)
            take_profit_pct: 익절 비율 (%)

        Returns:
            백테스트 결과
        """
        try:
            # 일봉 데이터 조회
            # 날짜 범위 계산 (시작일로부터 종료일까지의 일수)
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            days = (end_dt - start_dt).days + 1

            # 충분한 데이터를 위해 시작일 이전 60일 추가
            extended_start_dt = start_dt - timedelta(days=60)
            extended_days = (end_dt - extended_start_dt).days + 1

            # 일봉 데이터 조회
            df = await self.stock_analyzer.get_daily_data(stock_code, extended_days)

            if df.empty:
                logger.error(f"백테스트를 위한 일봉 데이터가 없습니다: {stock_code}")
                return {"error": "일봉 데이터 없음"}

            # 날짜 필터링
            if 'date' in df.columns:
                df = df[(df['date'] >= pd.Timestamp(start_date)) & (df['date'] <= pd.Timestamp(end_date))]

            if df.empty:
                logger.error(f"지정된 기간에 해당하는 데이터가 없습니다: {start_date} ~ {end_date}")
                return {"error": "기간 내 데이터 없음"}

            # 거래 기록 및 계좌 현황 초기화
            trades = []
            portfolio = {
                'cash': self.initial_capital,
                'stocks': 0,
                'position_price': 0,
                'position_date': None
            }

            # 각 일자별로 매매 전략 적용
            for i in range(len(df)):
                current_row = df.iloc[i]
                current_date = current_row['date'] if 'date' in current_row else f"Day {i}"
                current_price = current_row['close'] if 'close' in current_row else 0

                # 보유 여부 확인
                has_position = portfolio['stocks'] > 0

                # 보유 중이라면 손익 확인
                if has_position:
                    position_price = portfolio['position_price']
                    profit_pct = (current_price - position_price) / position_price * 100

                    # 손절/익절 조건 확인
                    if profit_pct <= stop_loss_pct or profit_pct >= take_profit_pct:
                        # 손절/익절에 따른 매도
                        reason = "stop_loss" if profit_pct <= stop_loss_pct else "take_profit"

                        # 매도 실행
                        sell_amount = portfolio['stocks'] * current_price
                        portfolio['cash'] += sell_amount

                        trades.append({
                            'date': current_date,
                            'action': 'sell',
                            'price': current_price,
                            'quantity': portfolio['stocks'],
                            'amount': sell_amount,
                            'reason': reason,
                            'profit_pct': profit_pct
                        })

                        # 포지션 초기화
                        portfolio['stocks'] = 0
                        portfolio['position_price'] = 0
                        portfolio['position_date'] = None

                        logger.debug(
                            f"매도 실행 - 날짜: {current_date}, 가격: {current_price}, 수량: {portfolio['stocks']}, 이유: {reason}")

                        continue

                    # 매도 전략 확인
                    if sell_strategy(df, i, portfolio):
                        # 매도 실행
                        sell_amount = portfolio['stocks'] * current_price
                        portfolio['cash'] += sell_amount

                        trades.append({
                            'date': current_date,
                            'action': 'sell',
                            'price': current_price,
                            'quantity': portfolio['stocks'],
                            'amount': sell_amount,
                            'reason': 'strategy',
                            'profit_pct': profit_pct
                        })

                        # 포지션 초기화
                        portfolio['stocks'] = 0
                        portfolio['position_price'] = 0
                        portfolio['position_date'] = None

                        logger.debug(
                            f"매도 실행 - 날짜: {current_date}, 가격: {current_price}, 수량: {portfolio['stocks']}, 이유: strategy")

                # 보유 중이 아니라면 매수 전략 확인
                else:
                    if buy_strategy(df, i):
                        # 자금의 90%로 매수 (여유자금 남김)
                        available_cash = portfolio['cash'] * 0.9
                        quantity = int(available_cash / current_price)

                        if quantity > 0:
                            # 매수 실행
                            buy_amount = quantity * current_price
                            portfolio['cash'] -= buy_amount
                            portfolio['stocks'] = quantity
                            portfolio['position_price'] = current_price
                            portfolio['position_date'] = current_date

                            trades.append({
                                'date': current_date,
                                'action': 'buy',
                                'price': current_price,
                                'quantity': quantity,
                                'amount': buy_amount,
                                'reason': 'strategy'
                            })

                            logger.debug(f"매수 실행 - 날짜: {current_date}, 가격: {current_price}, 수량: {quantity}")

            # 마지막 날에 보유 포지션 청산
            if portfolio['stocks'] > 0:
                last_price = df.iloc[-1]['close'] if 'close' in df.columns else 0
                last_date = df.iloc[-1]['date'] if 'date' in df.columns else f"Day {len(df) - 1}"

                # 매도 실행
                sell_amount = portfolio['stocks'] * last_price
                portfolio['cash'] += sell_amount

                # 수익률 계산
                profit_pct = (last_price - portfolio['position_price']) / portfolio['position_price'] * 100

                trades.append({
                    'date': last_date,
                    'action': 'sell',
                    'price': last_price,
                    'quantity': portfolio['stocks'],
                    'amount': sell_amount,
                    'reason': 'end_of_period',
                    'profit_pct': profit_pct
                })

                # 포지션 초기화
                portfolio['stocks'] = 0
                portfolio['position_price'] = 0
                portfolio['position_date'] = None

                logger.debug(f"기간 종료 청산 - 날짜: {last_date}, 가격: {last_price}, 수량: {portfolio['stocks']}")

            # 결과 분석
            result = self._analyze_backtest_result(trades, df)

            # 결과 저장
            self.results[f"{stock_code}_{start_date}_{end_date}"] = result

            return result

        except Exception as e:
            logger.exception(f"백테스트 실행 중 오류: {str(e)}")
            return {"error": str(e)}

    def _analyze_backtest_result(self, trades: List[Dict[str, Any]], price_data: pd.DataFrame) -> Dict[str, Any]:
        """
        백테스트 결과 분석

        Args:
            trades: 거래 내역 목록
            price_data: 가격 데이터

        Returns:
            분석 결과
        """
        if not trades:
            return {
                "total_return": 0,
                "total_return_pct": 0,
                "annualized_return": 0,
                "max_drawdown": 0,
                "win_rate": 0,
                "trade_count": 0,
                "avg_holding_period": 0,
                "sharpe_ratio": 0
            }

        try:
            # 거래 데이터프레임 생성
            trades_df = pd.DataFrame(trades)

            # 매수/매도 거래 분리
            buy_trades = trades_df[trades_df['action'] == 'buy']
            sell_trades = trades_df[trades_df['action'] == 'sell']

            # 수익 거래 및 손실 거래 분석
            if 'profit_pct' in sell_trades.columns:
                profit_trades = sell_trades[sell_trades['profit_pct'] > 0]
                loss_trades = sell_trades[sell_trades['profit_pct'] <= 0]

                # 승률 계산
                win_rate = len(profit_trades) / len(sell_trades) * 100 if len(sell_trades) > 0 else 0

                # 평균 수익률 및 손실률
                avg_profit_pct = profit_trades['profit_pct'].mean() if len(profit_trades) > 0 else 0
                avg_loss_pct = loss_trades['profit_pct'].mean() if len(loss_trades) > 0 else 0

                # 전체 수익률
                total_return_pct = sell_trades['profit_pct'].sum()
            else:
                win_rate = 0
                avg_profit_pct = 0
                avg_loss_pct = 0
                total_return_pct = 0

            # 초기 자본 및 최종 자본
            initial_capital = self.initial_capital
            final_capital = initial_capital * (1 + total_return_pct / 100)

            # 총 수익
            total_return = final_capital - initial_capital

            # 보유 기간 분석
            avg_holding_period = 0
            if 'date' in buy_trades.columns and 'date' in sell_trades.columns:
                if len(buy_trades) > 0 and len(sell_trades) > 0:
                    for i in range(min(len(buy_trades), len(sell_trades))):
                        buy_date = buy_trades.iloc[i]['date']
                        sell_date = sell_trades.iloc[i]['date']

                        if isinstance(buy_date, str) and isinstance(sell_date, str):
                            buy_date = pd.to_datetime(buy_date)
                            sell_date = pd.to_datetime(sell_date)

                        if isinstance(buy_date, pd.Timestamp) and isinstance(sell_date, pd.Timestamp):
                            holding_days = (sell_date - buy_date).days
                            avg_holding_period += holding_days

                    avg_holding_period /= min(len(buy_trades), len(sell_trades))

            # 최대 낙폭 (MDD) 계산
            mdd = 0
            if 'close' in price_data.columns:
                price_data['cummax'] = price_data['close'].cummax()
                price_data['drawdown'] = (price_data['close'] - price_data['cummax']) / price_data['cummax'] * 100
                mdd = price_data['drawdown'].min()

            # 연간 수익률 (단순)
            if 'date' in price_data.columns:
                start_date = price_data['date'].min()
                end_date = price_data['date'].max()

                if isinstance(start_date, pd.Timestamp) and isinstance(end_date, pd.Timestamp):
                    years = (end_date - start_date).days / 365
                    if years > 0:
                        annualized_return = ((1 + total_return_pct / 100) ** (1 / years) - 1) * 100
                    else:
                        annualized_return = total_return_pct
                else:
                    annualized_return = total_return_pct
            else:
                annualized_return = total_return_pct

            # 샤프 비율 (간단 계산)
            sharpe_ratio = 0
            if 'close' in price_data.columns:
                daily_returns = price_data['close'].pct_change().dropna()
                if len(daily_returns) > 0:
                    avg_return = daily_returns.mean() * 252  # 연 평균 수익
                    std_return = daily_returns.std() * np.sqrt(252)  # 연 표준편차
                    if std_return > 0:
                        sharpe_ratio = avg_return / std_return

            # 결과 정리
            return {
                "total_return": total_return,
                "total_return_pct": total_return_pct,
                "annualized_return": annualized_return,
                "max_drawdown": mdd,
                "win_rate": win_rate,
                "trade_count": len(sell_trades),
                "avg_profit_pct": avg_profit_pct,
                "avg_loss_pct": avg_loss_pct,
                "avg_holding_period": avg_holding_period,
                "sharpe_ratio": sharpe_ratio,
                "initial_capital": initial_capital,
                "final_capital": final_capital,
                "trades": trades_df.to_dict('records') if len(trades_df) < 100 else f"{len(trades_df)}개 거래 (상세 내역 생략)"
            }

        except Exception as e:
            logger.exception(f"백테스트 결과 분석 중 오류: {str(e)}")
            return {
                "error": str(e),
                "trade_count": len(trades)
            }

    def get_result(self, result_key: str) -> Optional[Dict[str, Any]]:
        """
        백테스트 결과 조회

        Args:
            result_key: 결과 키

        Returns:
            백테스트 결과
        """
        return self.results.get(result_key)

    def get_all_results(self) -> Dict[str, Dict[str, Any]]:
        """
        모든 백테스트 결과 조회

        Returns:
            모든 백테스트 결과
        """
        return self.results

    def reset(self) -> None:
        """결과 초기화"""
        self.results.clear()
        logger.info("백테스트 결과 초기화 완료")

    @async_measure_time
    async def compare_strategies(self,
                                 stock_code: str,
                                 start_date: str,
                                 end_date: str,
                                 strategies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        여러 전략 비교

        Args:
            stock_code: 종목코드
            start_date: 시작일 (YYYY-MM-DD)
            end_date: 종료일 (YYYY-MM-DD)
            strategies: 전략 목록 [{'name': '전략명', 'buy_strategy': 함수, 'sell_strategy': 함수}, ...]

        Returns:
            비교 결과
        """
        if not strategies:
            logger.error("비교할 전략이 없습니다.")
            return {"error": "전략 없음"}

        results = {}

        for strategy in strategies:
            name = strategy.get('name', 'Unknown')
            buy_strategy = strategy.get('buy_strategy')
            sell_strategy = strategy.get('sell_strategy')
            stop_loss = strategy.get('stop_loss_pct', -5.0)
            take_profit = strategy.get('take_profit_pct', 5.0)

            if not buy_strategy or not sell_strategy:
                logger.warning(f"전략 '{name}'에 매수/매도 함수가 없습니다.")
                continue

            logger.info(f"전략 '{name}' 백테스트 실행...")

            # 백테스트 실행
            result = await self.run_backtest(
                stock_code=stock_code,
                start_date=start_date,
                end_date=end_date,
                buy_strategy=buy_strategy,
                sell_strategy=sell_strategy,
                stop_loss_pct=stop_loss,
                take_profit_pct=take_profit
            )

            # 결과 저장
            results[name] = result

        # 결과 비교
        comparison = {
            "stock_code": stock_code,
            "period": f"{start_date} ~ {end_date}",
            "strategies": results,
            "best_strategy": None,
            "best_return": -float('inf')
        }

        # 최고 수익률 전략 찾기
        for name, result in results.items():
            if "error" not in result:
                return_pct = result.get("total_return_pct", 0)
                if return_pct > comparison["best_return"]:
                    comparison["best_return"] = return_pct
                    comparison["best_strategy"] = name

        return comparison