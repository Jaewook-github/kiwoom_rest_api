# config/logging_config.py
import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_dir: str = './logs', log_level: int = logging.INFO):
    """로깅 설정
    
    Args:
        log_dir: 로그 저장 디렉토리
        log_level: 로그 레벨 (logging.DEBUG, logging.INFO, ...)
    """
    # 로그 디렉토리 생성
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 로거 설정
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # 기존 핸들러 제거
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 파일 핸들러 (로그 파일 저장)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'kiwoom_quant.log'),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(log_level)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    
    # 콘솔 핸들러 (터미널 출력)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    return logger