# config/settings.py
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# API 설정
API_BASE_URL = os.getenv("KIWOOM_API_URL", "https://openapi.kiwoom.com/v1")
API_KEY = os.getenv("KIWOOM_API_KEY", "")
API_SECRET = os.getenv("KIWOOM_API_SECRET", "")

# 데이터베이스 설정 (옵션)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "kiwoom_quant")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# 웹 서버 설정
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8050"))
DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"

# 캐시 설정
CACHE_DIR = os.getenv("CACHE_DIR", "./cache")
CACHE_EXPIRY = int(os.getenv("CACHE_EXPIRY", "86400"))  # 초 단위 (기본값: 1일)

# 백테스트 설정
BACKTEST_DEFAULT_CAPITAL = float(os.getenv("BACKTEST_DEFAULT_CAPITAL", "100000000"))  # 1억원
BACKTEST_COMMISSION_RATE = float(os.getenv("BACKTEST_COMMISSION_RATE", "0.00015"))  # 0.015%
BACKTEST_SLIPPAGE_RATE = float(os.getenv("BACKTEST_SLIPPAGE_RATE", "0.0005"))  # 0.05%

# 기타 설정
DEFAULT_RISK_FREE_RATE = float(os.getenv("DEFAULT_RISK_FREE_RATE", "0.02"))  # 2%
DEFAULT_CHART_FIGSIZE = (12, 8)
MAX_API_RETRY = int(os.getenv("MAX_API_RETRY", "3"))
API_RETRY_DELAY = float(os.getenv("API_RETRY_DELAY", "1.0"))  # 초 단위

