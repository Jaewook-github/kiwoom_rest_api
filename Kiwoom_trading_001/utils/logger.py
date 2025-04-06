"""
로깅 설정 모듈
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
import sys

from config import config


class CustomFormatter(logging.Formatter):
    """컬러 로깅 포맷터"""

    COLORS = {
        'DEBUG': '\033[36m',  # 청록색
        'INFO': '\033[32m',  # 녹색
        'WARNING': '\033[33m',  # 노란색
        'ERROR': '\033[31m',  # 빨간색
        'CRITICAL': '\033[41m',  # 빨간 배경
        'RESET': '\033[0m'  # 리셋
    }

    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_fmt, '%Y-%m-%d %H:%M:%S')

        # 콘솔 출력에만 색상 적용
        if record.levelname in self.COLORS and sys.stderr.isatty():
            colored_levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
            record.levelname = colored_levelname

        return formatter.format(record)


def setup_logger(name='KiwoomAutoTrader', log_dir='logs'):
    """로거 설정"""
    # 로그 디렉토리 생성
    os.makedirs(log_dir, exist_ok=True)

    # 로그 파일명 설정 (오늘 날짜 포함)
    log_file = config.get('system', 'log_file')
    if not log_file:
        today = datetime.now().strftime('%Y%m%d')
        log_file = f"{log_dir}/auto_trading_{today}.log"
    elif not os.path.isabs(log_file):
        log_file = f"{log_dir}/{log_file}"

    # 로그 레벨 설정
    log_level_str = config.get('system', 'log_level')
    log_level = getattr(logging, log_level_str) if log_level_str else logging.INFO

    # 로거 생성
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # 기존 핸들러 제거 (중복 로깅 방지)
    if logger.handlers:
        logger.handlers.clear()

    # 파일 핸들러 추가 (최대 10MB, 10개 백업)
    file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=10)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # 콘솔 핸들러 추가
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)

    return logger


# 전역 로거 생성
logger = setup_logger()