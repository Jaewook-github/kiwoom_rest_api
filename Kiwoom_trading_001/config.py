"""
키움증권 자동매매 시스템 설정 파일
"""
import os
from typing import Dict, Any, List, Optional
import json

# 기본 설정
DEFAULT_CONFIG = {
    # 시스템 설정
    "system": {
        "log_level": "INFO",
        "log_file": "auto_trading.log",
        "data_dir": "./trading_data",
    },

    # API 설정
    "api": {
        "real_server": {
            "rest_host": "https://api.kiwoom.com",
            "ws_host": "wss://api.kiwoom.com:10000/api/dostk/websocket",
        },
        "mock_server": {
            "rest_host": "https://mockapi.kiwoom.com",
            "ws_host": "wss://mockapi.kiwoom.com:10000/api/dostk/websocket",
        },
        "request_timeout": 30,
        "retry_count": 3,
    },

    # 거래 설정
    "trading": {
        "max_budget_per_stock": 500000,  # 종목당 최대 매수 금액
        "max_stocks": 5,  # 최대 매수 종목 수
        "min_budget_per_stock": 100000,  # 종목당 최소 투자금
        "take_profit_pct": 2.0,  # 익절 기준 (%)
        "stop_loss_pct": -2.0,  # 손절 기준 (%)
        "max_daily_loss_pct": -5.0,  # 당일 최대 손실률 (%)
        "partial_profit_ratio": 0.5,  # 부분 익절 비율
    },

    # 시장 설정
    "market": {
        "start_time": "090000",  # 9시
        "end_time": "153000",  # 15시 30분
        "condition_schedule": {
            "090500": 0,  # 9시 5분에 0번 조건검색 실행
            "103000": 1,  # 10시 30분에 1번 조건검색 실행
            "133000": 2,  # 13시 30분에 2번 조건검색 실행
        },
    },

    # 알림 설정
    "notification": {
        "enable_telegram": False,
        "enable_email": False,
        "critical_alerts": ["trade_error", "connection_lost"],
    },

    # 모니터링 서버 설정
    "monitoring": {
        "enable_api_server": False,
        "host": "127.0.0.1",
        "port": 8080,
        "enable_auth": True,
    }
}


class Config:
    """설정 관리 클래스"""

    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = DEFAULT_CONFIG.copy()
        self._load_config()

    def _load_config(self) -> None:
        """파일에서 설정 로딩"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    self._merge_config(self.config, user_config)
            except Exception as e:
                print(f"설정 파일 로딩 실패: {str(e)}. 기본 설정을 사용합니다.")
        else:
            self._save_config()  # 기본 설정 파일 생성

    def _save_config(self) -> None:
        """설정을 파일에 저장"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"설정 파일 저장 실패: {str(e)}")

    def _merge_config(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        """두 설정 딕셔너리 병합"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def get(self, section: str, key: Optional[str] = None) -> Any:
        """설정값 조회"""
        if key:
            return self.config.get(section, {}).get(key)
        return self.config.get(section, {})

    def set(self, section: str, key: str, value: Any) -> None:
        """설정값 변경"""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        self._save_config()

    def reload(self) -> None:
        """설정 다시 로드"""
        self._load_config()


# 전역 설정 객체 생성
config = Config()