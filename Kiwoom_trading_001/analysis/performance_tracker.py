"""
성과 추적 모듈
"""
import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Set
import pandas as pd
import numpy as np
import asyncio

from config import config
from utils.logger import logger
from utils.helpers import save_json_data, load_json_data, format_money, format_percentage
from utils.helpers import get_current_time_str


class PerformanceTracker:
    """성과 추적 클래스"""

    def __init__(self, trader_instance):
        """
        초기화

        Args:
            trader_instance: 트레이더 인스턴스
        """
        self.trader = trader_instance

        # 데이터 저장 경로
        self.data_dir = config.get('system', 'data_dir', './trading_data')
        self.performance_dir = f"{self.data_dir}/performance"
        os.makedirs(self.performance_dir, exist_ok=True)

        # 성과 데이터
        self.daily_performance = {}
        self.monthly_performance = {}

        logger.info("성과 추적기 초기화 완료")

    async def update_daily_performance(self) -> Dict[str, Any]:
        """
        일일 성과 업데이트

        Returns:
            일일 성과 데이터
        """
        try:
            # 현재 날짜
            today = datetime.now().strftime('%Y%m%d')

            # 계좌 정보 갱신
            account_data = await self.trader._update_account_balance()

            # 계좌 정보가 없으면 빈 객체 반환
            if not account_data:
                logger.error("계좌 정보 조회 실패로 성과 업데이트 중단")
                return {}

            # 포트폴리오 통계 계산
            portfolio_stats = account_data.get('portfolio_stats', {})

            # 현재 보유 종목
            holdings = self.trader.holdings

            # 당일 거래 내역
            orders = self.trader.order_manager.get_today_orders()

            # 일일 성과 데이터 구성
            daily_perf = {
                'date': today,
                'timestamp': get_current_time_str(),
                'account': {
                    'cash': float(account_data.get('cash_amt', 0)),
                    'portfolio_value': portfolio_stats.get('total_value', 0),
                    'total_profit': portfolio_stats.get('total_profit', 0),
                    'profit_rate': portfolio_stats.get('total_profit_rate', 0)
                },
                'holdings_count': len(holdings),
                'trade_count': {
                    'buy': len([o for o in orders.get('executed', []) if o['type'] == 'buy']),
                    'sell': len([o for o in orders.get('executed', []) if o['type'] == 'sell'])
                }
            }

            # 이전 데이터가 있으면 일일 변동 계산
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
            yesterday_perf = self.daily_performance.get(yesterday, {})

            if yesterday_perf and 'account' in yesterday_perf:
                yesterday_account = yesterday_perf['account']
                yesterday_total = yesterday_account.get('cash', 0) + yesterday_account.get('portfolio_value', 0)
                today_total = daily_perf['account']['cash'] + daily_perf['account']['portfolio_value']

                # 일일 수익 및 수익률
                daily_profit = today_total - yesterday_total
                daily_profit_rate = (daily_profit / yesterday_total * 100) if yesterday_total > 0 else 0

                daily_perf['daily_change'] = {
                    'profit': daily_profit,
                    'profit_rate': daily_profit_rate
                }

            # 성과 데이터 저장
            self.daily_performance[today] = daily_perf

            # 파일 저장
            file_path = f"{self.performance_dir}/performance_{today}.json"
            save_json_data(daily_perf, file_path)

            logger.info(f"일일 성과 업데이트 완료 - {today}")

            return daily_perf

        except Exception as e:
            logger.exception(f"일일 성과 업데이트 중 오류: {str(e)}")
            return {}

    async def generate_monthly_performance(self, year_month: Optional[str] = None) -> Dict[str, Any]:
        """
        월간 성과 생성

        Args:
            year_month: 년월 (YYYYMM) - None이면 현재 월

        Returns:
            월간 성과 데이터
        """
        try:
            # 년월 설정
            if year_month is None:
                year_month = datetime.now().strftime('%Y%m')

            year = year_month[:4]
            month = year_month[4:6]

            # 해당 월의 모든 일일 성과 파일 찾기
            monthly_data = []

            # 디렉토리 내 파일들 중 해당 월 파일 찾기
            for filename in os.listdir(self.performance_dir):
                if filename.startswith(f"performance_{year}{month}") and filename.endswith(".json"):
                    file_path = f"{self.performance_dir}/{filename}"
                    daily_data = load_json_data(file_path)
                    if daily_data:
                        monthly_data.append(daily_data)

            # 날짜 순으로 정렬
            monthly_data.sort(key=lambda x: x.get('date', ''))

            if not monthly_data:
                logger.warning(f"{year}년 {month}월 성과 데이터가 없습니다.")
                return {}

            # 월간 성과 분석
            first_day = monthly_data[0]
            last_day = monthly_data[-1]

            # 계좌 정보
            first_account = first_day.get('account', {})
            last_account = last_day.get('account', {})

            # 월초 및 월말 총자산
            first_total = first_account.get('cash', 0) + first_account.get('portfolio_value', 0)
            last_total = last_account.get('cash', 0) + last_account.get('portfolio_value', 0)

            # 월간 수익 및 수익률
            monthly_profit = last_total - first_total
            monthly_profit_rate = (monthly_profit / first_total * 100) if first_total > 0 else 0

            # 월간 누적 거래 건수
            monthly_buy_count = sum(day.get('trade_count', {}).get('buy', 0) for day in monthly_data)
            monthly_sell_count = sum(day.get('trade_count', {}).get('sell', 0) for day in monthly_data)

            # 일별 수익률 추출 (있는 경우)
            daily_rates = []
            for day in monthly_data:
                if 'daily_change' in day and 'profit_rate' in day['daily_change']:
                    daily_rates.append(day['daily_change']['profit_rate'])

            # 최대/최소/평균 일간 수익률
            max_daily_rate = max(daily_rates) if daily_rates else 0
            min_daily_rate = min(daily_rates) if daily_rates else 0
            avg_daily_rate = sum(daily_rates) / len(daily_rates) if daily_rates else 0

            # 월간 성과 구성
            monthly_perf = {
                'year': year,
                'month': month,
                'start_date': first_day.get('date', ''),
                'end_date': last_day.get('date', ''),
                'trading_days': len(monthly_data),
                'monthly_profit': monthly_profit,
                'monthly_profit_rate': monthly_profit_rate,
                'first_day_total': first_total,
                'last_day_total': last_total,
                'max_daily_rate': max_daily_rate,
                'min_daily_rate': min_daily_rate,
                'avg_daily_rate': avg_daily_rate,
                'trade_count': {
                    'buy': monthly_buy_count,
                    'sell': monthly_sell_count,
                    'total': monthly_buy_count + monthly_sell_count
                },
                'last_day_holdings': last_day.get('holdings_count', 0)
            }

            # 월간 성과 데이터 저장
            self.monthly_performance[year_month] = monthly_perf

            # 파일 저장
            file_path = f"{self.performance_dir}/monthly_performance_{year_month}.json"
            save_json_data(monthly_perf, file_path)

            logger.info(f"월간 성과 생성 완료 - {year}년 {month}월")

            return monthly_perf

        except Exception as e:
            logger.exception(f"월간 성과 생성 중 오류: {str(e)}")
            return {}

    def get_daily_performance(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        일일 성과 조회

        Args:
            date: 날짜 (YYYYMMDD) - None이면 오늘

        Returns:
            일일 성과 데이터
        """
        if date is None:
            date = datetime.now().strftime('%Y%m%d')

        # 메모리에 있으면 반환
        if date in self.daily_performance:
            return self.daily_performance[date]

        # 파일에서 로드
        file_path = f"{self.performance_dir}/performance_{date}.json"
        daily_data = load_json_data(file_path)

        # 데이터 있으면 캐시에 저장
        if daily_data:
            self.daily_performance[date] = daily_data

        return daily_data or {}

    def get_monthly_performance(self, year_month: Optional[str] = None) -> Dict[str, Any]:
        """
        월간 성과 조회

        Args:
            year_month: 년월 (YYYYMM) - None이면 현재 월

        Returns:
            월간 성과 데이터
        """
        if year_month is None:
            year_month = datetime.now().strftime('%Y%m')

        # 메모리에 있으면 반환
        if year_month in self.monthly_performance:
            return self.monthly_performance[year_month]

        # 파일에서 로드
        file_path = f"{self.performance_dir}/monthly_performance_{year_month}.json"
        monthly_data = load_json_data(file_path)

        # 데이터 있으면 캐시에 저장
        if monthly_data:
            self.monthly_performance[year_month] = monthly_data

        return monthly_data or {}

    async def analyze_performance_trend(self, months: int = 6) -> Dict[str, Any]:
        """
        성과 추세 분석

        Args:
            months: 분석 기간 (월)

        Returns:
            추세 분석 결과
        """
        try:
            # 현재 날짜
            now = datetime.now()

            # 분석 대상 월 리스트 생성
            month_list = []
            for i in range(months):
                target_date = now - timedelta(days=30 * i)
                month_list.append(target_date.strftime('%Y%m'))

            # 월별 데이터 수집
            monthly_data = []
            for year_month in month_list:
                perf = self.get_monthly_performance(year_month)
                if perf:
                    monthly_data.append(perf)
                else:
                    # 없으면 생성 시도
                    perf = await self.generate_monthly_performance(year_month)
                    if perf:
                        monthly_data.append(perf)

            # 데이터 날짜순 정렬
            monthly_data.sort(key=lambda x: f"{x.get('year', '')}{x.get('month', '')}")

            if not monthly_data:
                logger.warning("분석할 월간 성과 데이터가 없습니다.")
                return {}

            # 수익률 추세
            profit_rates = [data.get('monthly_profit_rate', 0) for data in monthly_data]
            cumulative_profit = 1.0
            cumulative_rates = []

            for rate in profit_rates:
                cumulative_profit *= (1 + rate / 100)
                cumulative_rates.append((cumulative_profit - 1) * 100)

            # 월간 거래량 추세
            trade_counts = [data.get('trade_count', {}).get('total', 0) for data in monthly_data]

            # 평균 일간 수익률 추세
            avg_daily_rates = [data.get('avg_daily_rate', 0) for data in monthly_data]

            # 월별 라벨
            labels = [f"{data.get('year', '')}-{data.get('month', '')}" for data in monthly_data]

            # 추세 분석 결과
            trend_analysis = {
                'period': f"최근 {len(monthly_data)}개월",
                'months': labels,
                'monthly_profit_rates': profit_rates,
                'cumulative_profit_rate': cumulative_rates[-1] if cumulative_rates else 0,
                'cumulative_trend': cumulative_rates,
                'trade_count_trend': trade_counts,
                'avg_daily_rate_trend': avg_daily_rates,
                'latest_month': monthly_data[-1] if monthly_data else {}
            }

            # 파일 저장
            file_path = f"{self.performance_dir}/trend_analysis_{now.strftime('%Y%m%d')}.json"
            save_json_data(trend_analysis, file_path)

            logger.info(f"성과 추세 분석 완료 - 최근 {len(monthly_data)}개월")

            return trend_analysis

        except Exception as e:
            logger.exception(f"성과 추세 분석 중 오류: {str(e)}")
            return {}

    def reset_cache(self) -> None:
        """캐시 초기화"""
        self.daily_performance.clear()
        self.monthly_performance.clear()
        logger.info("성과 데이터 캐시 초기화 완료")

    def get_performance_summary(self) -> Dict[str, Any]:
        """
        성과 요약 조회

        Returns:
            성과 요약 데이터
        """
        try:
            # 오늘 날짜
            today = datetime.now().strftime('%Y%m%d')

            # 이번 달
            current_month = datetime.now().strftime('%Y%m')

            # 일일 성과
            daily_perf = self.get_daily_performance(today)

            # 월간 성과
            monthly_perf = self.get_monthly_performance(current_month)

            # 요약 데이터 구성
            summary = {
                'date': today,
                'daily': {
                    'total_value': daily_perf.get('account', {}).get('portfolio_value', 0) +
                                   daily_perf.get('account', {}).get('cash', 0),
                    'profit_rate': daily_perf.get('daily_change', {}).get('profit_rate', 0),
                    'holdings_count': daily_perf.get('holdings_count', 0),
                    'trade_count': daily_perf.get('trade_count', {}).get('total', 0)
                },
                'monthly': {
                    'profit_rate': monthly_perf.get('monthly_profit_rate', 0),
                    'trading_days': monthly_perf.get('trading_days', 0),
                    'trade_count': monthly_perf.get('trade_count', {}).get('total', 0)
                }
            }

            return summary

        except Exception as e:
            logger.exception(f"성과 요약 조회 중 오류: {str(e)}")
            return {}