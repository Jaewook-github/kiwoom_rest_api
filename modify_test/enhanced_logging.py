import os
import sys
from datetime import datetime
from loguru import logger
from pathlib import Path


class EnhancedLogger:
    def __init__(self):
        self.setup_logs_directory()
        self.setup_loggers()

    def setup_logs_directory(self):
        """logs 디렉토리 및 하위 디렉토리 생성"""
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)

        # 카테고리별 디렉토리 생성
        categories = ["trading", "errors", "tr_requests", "websocket", "orders", "general"]
        for category in categories:
            (self.logs_dir / category).mkdir(exist_ok=True)

    def setup_loggers(self):
        """각 카테고리별 로거 설정"""
        # 기본 로거 제거
        logger.remove()

        # 날짜 포맷
        today = datetime.now().strftime("%Y%m%d")

        # 1. 콘솔 출력 (모든 로그)
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="DEBUG"
        )

        # 2. 전체 로그 (일반)
        logger.add(
            self.logs_dir / "general" / f"app_{today}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="DEBUG",
            rotation="1 day",
            retention="30 days",
            compression="zip",
            encoding="utf-8"
        )

        # 3. 에러 로그
        logger.add(
            self.logs_dir / "errors" / f"errors_{today}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="ERROR",
            rotation="1 day",
            retention="90 days",
            compression="zip",
            encoding="utf-8"
        )

        # 4. 매매 로그 (필터링)
        def trading_filter(record):
            return "TRADING" in record["extra"] or any(keyword in record["message"].lower() for keyword in
                                                       ["매수", "매도", "주문", "체결", "수익률", "손실", "트레일링", "스탑로스"])

        logger.add(
            self.logs_dir / "trading" / f"trading_{today}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
            filter=trading_filter,
            level="INFO",
            rotation="1 day",
            retention="365 days",  # 매매 로그는 1년 보관
            compression="zip",
            encoding="utf-8"
        )

        # 5. TR 요청 로그 (필터링)
        def tr_filter(record):
            return "TR_REQUEST" in record["extra"] or any(keyword in record["message"].lower() for keyword in
                                                          ["tr", "api", "request", "계좌조회", "주식기본정보"])

        logger.add(
            self.logs_dir / "tr_requests" / f"tr_requests_{today}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
            filter=tr_filter,
            level="DEBUG",
            rotation="1 day",
            retention="30 days",
            compression="zip",
            encoding="utf-8"
        )

        # 6. 웹소켓 로그 (필터링)
        def websocket_filter(record):
            return "WEBSOCKET" in record["extra"] or any(keyword in record["message"].lower() for keyword in
                                                         ["websocket", "실시간", "조건식", "편입", "편출"])

        logger.add(
            self.logs_dir / "websocket" / f"websocket_{today}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
            filter=websocket_filter,
            level="DEBUG",
            rotation="1 day",
            retention="30 days",
            compression="zip",
            encoding="utf-8"
        )

        # 7. 주문 로그 (필터링)
        def order_filter(record):
            return "ORDER" in record["extra"] or any(keyword in record["message"].lower() for keyword in
                                                     ["주문접수", "주문체결", "미체결", "정정", "취소"])

        logger.add(
            self.logs_dir / "orders" / f"orders_{today}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
            filter=order_filter,
            level="INFO",
            rotation="1 day",
            retention="180 days",  # 주문 로그는 6개월 보관
            compression="zip",
            encoding="utf-8"
        )


# 전역 로거 인스턴스 생성
enhanced_logger = EnhancedLogger()


# 편의 함수들
def log_trading(message, level="INFO"):
    """매매 관련 로그"""
    if level.upper() == "ERROR":
        logger.bind(TRADING=True).error(f"[TRADING] {message}")
    elif level.upper() == "WARNING":
        logger.bind(TRADING=True).warning(f"[TRADING] {message}")
    else:
        logger.bind(TRADING=True).info(f"[TRADING] {message}")


def log_tr_request(message, level="DEBUG"):
    """TR 요청 관련 로그"""
    if level.upper() == "ERROR":
        logger.bind(TR_REQUEST=True).error(f"[TR_REQUEST] {message}")
    elif level.upper() == "WARNING":
        logger.bind(TR_REQUEST=True).warning(f"[TR_REQUEST] {message}")
    else:
        logger.bind(TR_REQUEST=True).debug(f"[TR_REQUEST] {message}")


def log_websocket(message, level="DEBUG"):
    """웹소켓 관련 로그"""
    if level.upper() == "ERROR":
        logger.bind(WEBSOCKET=True).error(f"[WEBSOCKET] {message}")
    elif level.upper() == "WARNING":
        logger.bind(WEBSOCKET=True).warning(f"[WEBSOCKET] {message}")
    else:
        logger.bind(WEBSOCKET=True).debug(f"[WEBSOCKET] {message}")


def log_order(message, level="INFO"):
    """주문 관련 로그"""
    if level.upper() == "ERROR":
        logger.bind(ORDER=True).error(f"[ORDER] {message}")
    elif level.upper() == "WARNING":
        logger.bind(ORDER=True).warning(f"[ORDER] {message}")
    else:
        logger.bind(ORDER=True).info(f"[ORDER] {message}")


def log_error(message, exception=None):
    """에러 로그"""
    if exception:
        logger.exception(f"[ERROR] {message}")
    else:
        logger.error(f"[ERROR] {message}")


def log_info(message):
    """일반 정보 로그"""
    logger.info(f"[INFO] {message}")


def log_debug(message):
    """디버그 로그"""
    logger.debug(f"[DEBUG] {message}")