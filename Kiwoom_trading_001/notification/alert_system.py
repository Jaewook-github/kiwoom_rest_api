"""
알림 시스템 모듈
"""
import asyncio
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional, Dict, Any, Union
import json
import requests

from ..config import config
from ..utils.logger import logger
from ..utils.helpers import get_current_time_str


class AlertSystem:
    """알림 시스템 클래스"""

    def __init__(self):
        """초기화"""
        # 알림 설정
        notification_config = config.get('notification')

        # 텔레그램 설정
        self.enable_telegram = notification_config.get('enable_telegram', False)
        self.telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")

        # 이메일 설정
        self.enable_email = notification_config.get('enable_email', False)
        self.email_sender = os.environ.get("EMAIL_SENDER")
        self.email_password = os.environ.get("EMAIL_PASSWORD")
        self.email_recipient = os.environ.get("EMAIL_RECIPIENT")
        self.email_smtp_server = os.environ.get("EMAIL_SMTP_SERVER", "smtp.gmail.com")
        self.email_smtp_port = int(os.environ.get("EMAIL_SMTP_PORT", "587"))

        # 중요 알림 카테고리
        self.critical_alerts = notification_config.get('critical_alerts', [])

        # 초기화 검사
        self._check_initialization()

        logger.info("알림 시스템 초기화 완료")

    def _check_initialization(self) -> None:
        """초기화 상태 확인"""
        if self.enable_telegram:
            if not self.telegram_token or not self.telegram_chat_id:
                logger.warning("텔레그램 설정이 불완전합니다. 환경 변수 TELEGRAM_BOT_TOKEN과 TELEGRAM_CHAT_ID를 확인하세요.")
                self.enable_telegram = False
            else:
                logger.info("텔레그램 알림 활성화")

        if self.enable_email:
            if not self.email_sender or not self.email_password or not self.email_recipient:
                logger.warning("이메일 설정이 불완전합니다. 관련 환경 변수를 확인하세요.")
                self.enable_email = False
            else:
                logger.info("이메일 알림 활성화")

    async def send_alert(self, message: str, category: str = "general", level: str = "info",
                         additional_info: Optional[Dict[str, Any]] = None,
                         channels: Optional[List[str]] = None) -> bool:
        """
        알림 전송

        Args:
            message: 알림 메시지
            category: 알림 카테고리
            level: 알림 레벨 (info, warning, error)
            additional_info: 추가 정보
            channels: 알림 채널 목록 (지정되지 않으면 모든 활성 채널)

        Returns:
            전송 성공 여부
        """
        # 알림 레벨에 따른 로깅
        if level == "info":
            logger.info(f"알림 [{category}]: {message}")
        elif level == "warning":
            logger.warning(f"알림 [{category}]: {message}")
        elif level == "error":
            logger.error(f"알림 [{category}]: {message}")

        # 알림 데이터 구성
        alert_data = {
            "message": message,
            "category": category,
            "level": level,
            "time": get_current_time_str(),
            "additional_info": additional_info or {}
        }

        # 알림 채널 결정
        if not channels:
            channels = []
            if self.enable_telegram:
                channels.append("telegram")
            if self.enable_email:
                # 이메일은 중요 알림만 전송
                if category in self.critical_alerts or level == "error":
                    channels.append("email")

        # 각 채널로 알림 전송
        success = True
        for channel in channels:
            if channel == "telegram" and self.enable_telegram:
                success = success and await self._send_telegram(alert_data)
            elif channel == "email" and self.enable_email:
                success = success and await self._send_email(alert_data)

        return success

    async def _send_telegram(self, alert_data: Dict[str, Any]) -> bool:
        """
        텔레그램으로 알림 전송

        Args:
            alert_data: 알림 데이터

        Returns:
            전송 성공 여부
        """
        try:
            # 알림 메시지 구성
            level = alert_data["level"]
            category = alert_data["category"]
            message = alert_data["message"]
            time = alert_data["time"]

            level_emoji = "ℹ️" if level == "info" else "⚠️" if level == "warning" else "🚨"

            formatted_message = (
                f"{level_emoji} *{category.upper()}*\n"
                f"{message}\n\n"
                f"🕒 {time}"
            )

            # 추가 정보가 있으면 포함
            additional_info = alert_data.get("additional_info")
            if additional_info:
                formatted_message += f"\n\n📋 추가 정보:\n```\n{json.dumps(additional_info, indent=2, ensure_ascii=False)}\n```"

            # 텔레그램 API 요청
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                "chat_id": self.telegram_chat_id,
                "text": formatted_message,
                "parse_mode": "Markdown"
            }

            # 비동기로 처리하기 위해 이벤트 루프의 run_in_executor 사용
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None,
                lambda: requests.post(url, json=payload, timeout=10)
            )

            if response.status_code == 200:
                logger.debug("텔레그램 알림 전송 성공")
                return True
            else:
                logger.error(f"텔레그램 알림 전송 실패: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.exception(f"텔레그램 알림 전송 중 오류: {str(e)}")
            return False

    async def _send_email(self, alert_data: Dict[str, Any]) -> bool:
        """
        이메일로 알림 전송

        Args:
            alert_data: 알림 데이터

        Returns:
            전송 성공 여부
        """
        try:
            # 알림 메시지 구성
            level = alert_data["level"]
            category = alert_data["category"]
            message = alert_data["message"]
            time = alert_data["time"]

            # 이메일 제목
            level_prefix = "[정보]" if level == "info" else "[경고]" if level == "warning" else "[오류]"
            subject = f"{level_prefix} {category.upper()} - 자동매매 알림"

            # 이메일 본문 (HTML)
            level_color = "#3498db" if level == "info" else "#f39c12" if level == "warning" else "#e74c3c"
            html_body = f"""
            <html>
              <body style="font-family: Arial, sans-serif; padding: 20px;">
                <div style="background-color: #f8f9fa; border-radius: 5px; padding: 20px; max-width: 600px;">
                  <h2 style="color: {level_color};">{level_prefix} {category.upper()}</h2>
                  <p style="font-size: 16px; line-height: 1.5;">{message}</p>
                  <p style="color: #7f8c8d; font-size: 14px;">발생 시간: {time}</p>
            """

            # 추가 정보가 있으면 포함
            additional_info = alert_data.get("additional_info")
            if additional_info:
                html_body += """
                  <div style="background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin-top: 20px;">
                    <h3 style="margin-top: 0;">추가 정보</h3>
                    <pre style="white-space: pre-wrap; font-family: monospace; margin: 0;">{}</pre>
                  </div>
                """.format(json.dumps(additional_info, indent=2, ensure_ascii=False))

            html_body += """
                </div>
              </body>
            </html>
            """

            # 메시지 생성
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.email_sender
            msg["To"] = self.email_recipient

            # HTML 부분 추가
            html_part = MIMEText(html_body, "html")
            msg.attach(html_part)

            # 이메일 전송 (비동기로 처리)
            return await self._send_email_async(msg)

        except Exception as e:
            logger.exception(f"이메일 알림 전송 중 오류: {str(e)}")
            return False

    async def _send_email_async(self, msg: MIMEMultipart) -> bool:
        """
        비동기 이메일 전송

        Args:
            msg: MIME 메시지

        Returns:
            전송 성공 여부
        """
        loop = asyncio.get_running_loop()

        # 이메일 전송 함수
        def send_mail():
            try:
                with smtplib.SMTP(self.email_smtp_server, self.email_smtp_port) as server:
                    server.starttls()
                    server.login(self.email_sender, self.email_password)
                    server.send_message(msg)
                return True
            except Exception as e:
                logger.exception(f"이메일 전송 중 오류: {str(e)}")
                return False

        # 비동기 실행
        try:
            result = await loop.run_in_executor(None, send_mail)
            if result:
                logger.debug("이메일 알림 전송 성공")
            else:
                logger.error("이메일 알림 전송 실패")
            return result
        except Exception as e:
            logger.exception(f"이메일 전송 비동기 처리 중 오류: {str(e)}")
            return False

    async def send_trade_alert(self, order_type: str, stock_code: str, quantity: int,
                               price: float, reason: str = None) -> bool:
        """
        거래 알림 전송

        Args:
            order_type: 거래 유형 (buy, sell)
            stock_code: 종목코드
            quantity: 수량
            price: 가격
            reason: 거래 이유

        Returns:
            전송 성공 여부
        """
        # 거래 유형에 따른 메시지 설정
        if order_type == "buy":
            message = f"[매수] {stock_code} - {quantity}주 @ {price:,.0f}원"
            category = "trade_buy"
        else:  # sell
            message = f"[매도] {stock_code} - {quantity}주 @ {price:,.0f}원"
            category = "trade_sell"

        # 거래 이유가 있으면 추가
        if reason:
            message += f" ({reason})"

        # 추가 정보
        additional_info = {
            "stock_code": stock_code,
            "quantity": quantity,
            "price": price,
            "total_amount": quantity * price,
            "reason": reason
        }

        # 알림 전송
        return await self.send_alert(message, category, "info", additional_info)

    async def send_system_alert(self, message: str, level: str = "info",
                                additional_info: Optional[Dict[str, Any]] = None) -> bool:
        """
        시스템 알림 전송

        Args:
            message: 알림 메시지
            level: 알림 레벨 (info, warning, error)
            additional_info: 추가 정보

        Returns:
            전송 성공 여부
        """
        return await self.send_alert(message, "system", level, additional_info)

    async def send_error_alert(self, error_message: str,
                               additional_info: Optional[Dict[str, Any]] = None) -> bool:
        """
        오류 알림 전송

        Args:
            error_message: 오류 메시지
            additional_info: 추가 정보

        Returns:
            전송 성공 여부
        """
        return await self.send_alert(error_message, "error", "error", additional_info)