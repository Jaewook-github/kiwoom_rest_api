"""
리포팅 기능 모듈
"""
import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
import pandas as pd
import asyncio

from config import config
from utils.logger import logger
from utils.helpers import get_current_time_str, save_json_data, load_json_data, format_money, format_percentage
from notification.alert_system import AlertSystem


class ReportGenerator:
    """리포트 생성 클래스"""

    def __init__(self, trader_instance, alert_system: Optional[AlertSystem] = None):
        """
        초기화

        Args:
            trader_instance: 트레이더 인스턴스
            alert_system: 알림 시스템 인스턴스
        """
        self.trader = trader_instance
        self.alert_system = alert_system

        # 데이터 저장 경로
        self.data_dir = config.get('system', 'data_dir', './trading_data')
        self.report_dir = f"{self.data_dir}/reports"
        os.makedirs(self.report_dir, exist_ok=True)

        logger.info("리포트 생성기 초기화 완료")

    async def generate_daily_report(self, date_str: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        일일 리포트 생성

        Args:
            date_str: 날짜 (YYYYMMDD) - None이면 오늘

        Returns:
            리포트 데이터
        """
        try:
            # 날짜 설정
            if date_str is None:
                date_str = datetime.now().strftime('%Y%m%d')

            # 리포트 파일 경로
            file_path = f"{self.data_dir}/report_{date_str}.json"

            # 리포트 데이터 로드
            daily_data = load_json_data(file_path)

            if not daily_data:
                logger.warning(f"{date_str} 날짜의 거래 내역이 없습니다.")
                return None

            # 리포트 구성
            report = {
                "date": date_str,
                "generated_at": get_current_time_str(),
                "account_summary": self._generate_account_summary(daily_data),
                "trading_summary": self._generate_trading_summary(daily_data),
                "holdings_summary": self._generate_holdings_summary(daily_data),
                "performance_metrics": self._calculate_performance_metrics(daily_data),
            }

            # 리포트 저장
            report_file_path = f"{self.report_dir}/daily_report_{date_str}.json"
            save_json_data(report, report_file_path)

            logger.info(f"일일 리포트 생성 완료: {report_file_path}")

            # 알림 전송
            if self.alert_system:
                await self._send_report_notification(report)

            return report

        except Exception as e:
            logger.exception(f"일일 리포트 생성 중 오류: {str(e)}")
            return None

    async def generate_weekly_report(self, end_date: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        주간 리포트 생성

        Args:
            end_date: 마지막 날짜 (YYYYMMDD) - None이면 오늘

        Returns:
            리포트 데이터
        """
        try:
            # 날짜 설정
            if end_date is None:
                end_date_obj = datetime.now()
            else:
                end_date_obj = datetime.strptime(end_date, '%Y%m%d')

            # 7일 전 날짜 계산
            start_date_obj = end_date_obj - timedelta(days=6)

            # 날짜 형식 지정
            end_date = end_date_obj.strftime('%Y%m%d')
            start_date = start_date_obj.strftime('%Y%m%d')

            # 주간 데이터 수집
            weekly_data = await self._collect_period_data(start_date, end_date)

            if not weekly_data:
                logger.warning(f"{start_date}부터 {end_date}까지의 거래 내역이 없습니다.")
                return None

            # 리포트 구성
            report = {
                "period": "weekly",
                "start_date": start_date,
                "end_date": end_date,
                "generated_at": get_current_time_str(),
                "account_summary": weekly_data["latest_account"],
                "trading_summary": self._aggregate_trading_data(weekly_data["daily_reports"]),
                "performance_metrics": self._calculate_period_performance(weekly_data),
            }

            # 리포트 저장
            report_file_path = f"{self.report_dir}/weekly_report_{start_date}_to_{end_date}.json"
            save_json_data(report, report_file_path)

            logger.info(f"주간 리포트 생성 완료: {report_file_path}")

            # 알림 전송
            if self.alert_system:
                await self._send_report_notification(report, "weekly")

            return report

        except Exception as e:
            logger.exception(f"주간 리포트 생성 중 오류: {str(e)}")
            return None

    async def _collect_period_data(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        기간별 데이터 수집

        Args:
            start_date: 시작 날짜 (YYYYMMDD)
            end_date: 종료 날짜 (YYYYMMDD)

        Returns:
            수집된 데이터
        """
        # 날짜 객체로 변환
        start_date_obj = datetime.strptime(start_date, '%Y%m%d')
        end_date_obj = datetime.strptime(end_date, '%Y%m%d')

        # 일별 리포트 데이터 수집
        daily_reports = []

        current_date = start_date_obj
        while current_date <= end_date_obj:
            date_str = current_date.strftime('%Y%m%d')
            file_path = f"{self.data_dir}/report_{date_str}.json"

            report_data = load_json_data(file_path)
            if report_data:
                daily_reports.append(report_data)

            # 다음 날짜로 이동
            current_date += timedelta(days=1)

        if not daily_reports:
            return {}

        # 최신 계좌 정보 (마지막 날짜의 데이터)
        latest_account = daily_reports[-1].get('account', {})

        return {
            "daily_reports": daily_reports,
            "latest_account": latest_account
        }

    def _generate_account_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        계좌 요약 정보 생성

        Args:
            data: 일일 데이터

        Returns:
            계좌 요약 정보
        """
        account_info = data.get('account', {})

        return {
            "total_balance": account_info.get('portfolio_value', 0) + account_info.get('cash', 0),
            "portfolio_value": account_info.get('portfolio_value', 0),
            "cash_balance": account_info.get('cash', 0),
            "total_profit": account_info.get('profit', 0),
            "profit_rate": account_info.get('profit_rate', 0)
        }

    def _generate_trading_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        거래 요약 정보 생성

        Args:
            data: 일일 데이터

        Returns:
            거래 요약 정보
        """
        orders = data.get('orders', {})
        executed_orders = orders.get('executed', [])
        buy_orders = [o for o in executed_orders if o.get('type') == 'buy']
        sell_orders = [o for o in executed_orders if o.get('type') == 'sell']

        # 총 거래 금액 계산
        total_buy_amount = sum(o.get('executed_price', 0) * o.get('executed_quantity', 0) for o in buy_orders)
        total_sell_amount = sum(o.get('executed_price', 0) * o.get('executed_quantity', 0) for o in sell_orders)

        return {
            "total_trades": len(executed_orders),
            "buy_count": len(buy_orders),
            "sell_count": len(sell_orders),
            "total_buy_amount": total_buy_amount,
            "total_sell_amount": total_sell_amount,
            "pending_orders": len(orders.get('pending', [])),
        }

    def _generate_holdings_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        보유 종목 요약 정보 생성

        Args:
            data: 일일 데이터

        Returns:
            보유 종목 요약 정보
        """
        holdings = data.get('holdings', {})

        # 종목별 데이터 추출
        holdings_data = []
        for code, info in holdings.items():
            buy_price = info.get('buy_price', 0)
            current_price = info.get('current_price', 0)
            quantity = info.get('quantity', 0)

            # 수익률 계산
            profit_rate = 0
            if buy_price > 0:
                profit_rate = (current_price - buy_price) / buy_price * 100

            holdings_data.append({
                "stock_code": code,
                "name": info.get('name', ''),
                "buy_price": buy_price,
                "current_price": current_price,
                "quantity": quantity,
                "total_value": current_price * quantity,
                "profit_rate": profit_rate,
                "profit_amount": (current_price - buy_price) * quantity
            })

        # 수익률 기준 정렬
        holdings_data.sort(key=lambda x: x['profit_rate'], reverse=True)

        return {
            "count": len(holdings_data),
            "holdings": holdings_data,
            "best_performing": holdings_data[0] if holdings_data else None,
            "worst_performing": holdings_data[-1] if holdings_data else None
        }

    def _calculate_performance_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        성과 지표 계산

        Args:
            data: 일일 데이터

        Returns:
            성과 지표
        """
        # 계좌 정보
        account_info = data.get('account', {})
        portfolio_value = account_info.get('portfolio_value', 0)
        cash = account_info.get('cash', 0)
        total_balance = portfolio_value + cash

        # 거래 정보
        orders = data.get('orders', {})
        executed_orders = orders.get('executed', [])
        buy_orders = [o for o in executed_orders if o.get('type') == 'buy']
        sell_orders = [o for o in executed_orders if o.get('type') == 'sell']

        # 당일 매수/매도 금액
        daily_buy_amount = sum(o.get('executed_price', 0) * o.get('executed_quantity', 0) for o in buy_orders)
        daily_sell_amount = sum(o.get('executed_price', 0) * o.get('executed_quantity', 0) for o in sell_orders)

        # 당일 손익
        daily_profit = account_info.get('profit', 0)

        # 현금 비율
        cash_ratio = (cash / total_balance * 100) if total_balance > 0 else 0

        # 투자 효율
        investment_efficiency = (daily_profit / daily_buy_amount * 100) if daily_buy_amount > 0 else 0

        return {
            "daily_profit": daily_profit,
            "daily_profit_rate": account_info.get('profit_rate', 0),
            "daily_buy_amount": daily_buy_amount,
            "daily_sell_amount": daily_sell_amount,
            "cash_ratio": cash_ratio,
            "investment_efficiency": investment_efficiency
        }

    def _aggregate_trading_data(self, daily_reports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        기간별 거래 데이터 집계

        Args:
            daily_reports: 일일 리포트 목록

        Returns:
            집계된 거래 데이터
        """
        total_buy_count = 0
        total_sell_count = 0
        total_buy_amount = 0
        total_sell_amount = 0

        for report in daily_reports:
            orders = report.get('orders', {})
            executed_orders = orders.get('executed', [])
            buy_orders = [o for o in executed_orders if o.get('type') == 'buy']
            sell_orders = [o for o in executed_orders if o.get('type') == 'sell']

            total_buy_count += len(buy_orders)
            total_sell_count += len(sell_orders)

            total_buy_amount += sum(o.get('executed_price', 0) * o.get('executed_quantity', 0) for o in buy_orders)
            total_sell_amount += sum(o.get('executed_price', 0) * o.get('executed_quantity', 0) for o in sell_orders)

        return {
            "total_trades": total_buy_count + total_sell_count,
            "buy_count": total_buy_count,
            "sell_count": total_sell_count,
            "total_buy_amount": total_buy_amount,
            "total_sell_amount": total_sell_amount,
        }

    def _calculate_period_performance(self, period_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        기간별 성과 계산

        Args:
            period_data: 기간별 데이터

        Returns:
            성과 지표
        """
        daily_reports = period_data.get('daily_reports', [])

        if not daily_reports:
            return {}

        # 시작과 종료 데이터
        start_report = daily_reports[0]
        end_report = daily_reports[-1]

        # 시작 및 종료 계좌 정보
        start_account = start_report.get('account', {})
        end_account = end_report.get('account', {})

        # 시작 및 종료 시점의 총 자산
        start_balance = start_account.get('portfolio_value', 0) + start_account.get('cash', 0)
        end_balance = end_account.get('portfolio_value', 0) + end_account.get('cash', 0)

        # 수익률 계산
        period_profit = end_balance - start_balance
        period_profit_rate = (period_profit / start_balance * 100) if start_balance > 0 else 0

        # 거래 정보
        trading_summary = self._aggregate_trading_data(daily_reports)
        total_buy_amount = trading_summary.get('total_buy_amount', 0)
        total_sell_amount = trading_summary.get('total_sell_amount', 0)

        # 일별 수익률
        daily_profit_rates = []
        for report in daily_reports:
            account_info = report.get('account', {})
            daily_profit_rates.append(account_info.get('profit_rate', 0))

        # 평균 일별 수익률
        avg_daily_profit_rate = sum(daily_profit_rates) / len(daily_profit_rates) if daily_profit_rates else 0

        # 최대 일별 수익률
        max_daily_profit_rate = max(daily_profit_rates) if daily_profit_rates else 0
        min_daily_profit_rate = min(daily_profit_rates) if daily_profit_rates else 0

        # 현금 비율
        cash = end_account.get('cash', 0)
        cash_ratio = (cash / end_balance * 100) if end_balance > 0 else 0

        return {
            "period_profit": period_profit,
            "period_profit_rate": period_profit_rate,
            "avg_daily_profit_rate": avg_daily_profit_rate,
            "max_daily_profit_rate": max_daily_profit_rate,
            "min_daily_profit_rate": min_daily_profit_rate,
            "total_buy_amount": total_buy_amount,
            "total_sell_amount": total_sell_amount,
            "cash_ratio": cash_ratio,
            "days_count": len(daily_reports)
        }

    async def _send_report_notification(self, report: Dict[str, Any], report_type: str = "daily") -> bool:
        """
        리포트 알림 전송

        Args:
            report: 리포트 데이터
            report_type: 리포트 유형

        Returns:
            전송 성공 여부
        """
        if not self.alert_system:
            return False

        try:
            # 리포트 유형에 따른 제목 설정
            if report_type == "daily":
                title = f"일일 거래 리포트 ({report.get('date', '')})"
            elif report_type == "weekly":
                title = f"주간 거래 리포트 ({report.get('start_date', '')} ~ {report.get('end_date', '')})"
            else:
                title = f"거래 리포트"

            # 성과 정보
            performance = report.get('performance_metrics', {})
            account_summary = report.get('account_summary', {})
            trading_summary = report.get('trading_summary', {})

            # 메시지 구성
            message = f"{title}\n\n"

            if report_type == "daily":
                message += f"• 당일 손익: {format_money(performance.get('daily_profit', 0))} ({format_percentage(performance.get('daily_profit_rate', 0))})\n"
                message += f"• 거래 건수: 매수 {trading_summary.get('buy_count', 0)}건, 매도 {trading_summary.get('sell_count', 0)}건\n"
                message += f"• 현금 비율: {format_percentage(performance.get('cash_ratio', 0))}\n"
            else:  # weekly
                message += f"• 기간 손익: {format_money(performance.get('period_profit', 0))} ({format_percentage(performance.get('period_profit_rate', 0))})\n"
                message += f"• 평균 일일 수익률: {format_percentage(performance.get('avg_daily_profit_rate', 0))}\n"
                message += f"• 총 거래 건수: 매수 {trading_summary.get('buy_count', 0)}건, 매도 {trading_summary.get('sell_count', 0)}건\n"

            # 알림 전송
            success = await self.alert_system.send_alert(
                message=message,
                category="report",
                level="info",
                additional_info={
                    "report_type": report_type,
                    "account_summary": account_summary,
                    "performance_metrics": performance
                }
            )

            return success

        except Exception as e:
            logger.exception(f"리포트 알림 전송 중 오류: {str(e)}")
            return False

    async def generate_scheduled_reports(self) -> None:
        """스케줄된 리포트 생성"""
        try:
            # 현재 날짜
            now = datetime.now()
            today_str = now.strftime('%Y%m%d')

            # 일일 리포트 생성
            if now.hour >= 16:  # 장 마감 후 (오후 4시 이후)
                await self.generate_daily_report(today_str)

            # 주간 리포트 생성 (금요일 또는 토요일)
            if now.weekday() in [4, 5]:  # 0=월요일, 4=금요일, 5=토요일
                await self.generate_weekly_report(today_str)

        except Exception as e:
            logger.exception(f"스케줄된 리포트 생성 중 오류: {str(e)}")