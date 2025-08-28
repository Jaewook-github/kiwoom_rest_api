is_paper_trading = True  # 모의투자 여부: False 또는 True
api_key = ""  # API KEY
api_secret_key = ""  # API SECRET KEY

host = "https://mockapi.kiwoom.com" if is_paper_trading else "https://api.kiwoom.com"
websocket_url = "wss://mockapi.kiwoom.com:10000/api/dostk/websocket" if is_paper_trading else "wss://api.kiwoom.com:10000/api/dostk/websocket"

# 로깅 설정
LOGGING_CONFIG = {
    "enable_trading_logs": True,      # 매매 로그 활성화
    "enable_tr_logs": True,           # TR 요청 로그 활성화
    "enable_websocket_logs": True,    # 웹소켓 로그 활성화
    "enable_order_logs": True,        # 주문 로그 활성화
    "enable_error_logs": True,        # 에러 로그 활성화
    "log_retention_days": {
        "general": 30,
        "trading": 365,
        "tr_requests": 30,
        "websocket": 30,
        "orders": 180,
        "errors": 90
    }
}

# 텔레그램 알림 설정
TELEGRAM_CONFIG = {
    "enabled": True,  # 텔레그램 알림 활성화
    "bot_token": "",  # 봇 토큰 (BotFather에서 발급)
    "chat_id": "",  # 채팅 ID (개인 또는 그룹)

    # 알림 활성화 설정
    "alert_levels": {
        "buy_condition": True,  # 매수 조건 편입 알림
        "buy_order": True,  # 매수 주문 접수 알림
        "buy_filled": True,  # 매수 체결 완료 알림
        "sell_condition": True,  # 매도 조건 발동 알림
        "sell_order": True,  # 매도 주문 접수 알림
        "sell_filled": True,  # 매도 체결 완료 알림
        "stop_loss": True,  # 손절 발동 알림
        "trailing_stop": True,  # 트레일링 스탑 알림
        "errors": True,  # 에러 알림
        "daily_summary": True,  # 일일 요약 알림
        "test": True  # 테스트 메시지
    },

    # 알림 조건 설정
    "alert_conditions": {
        "min_amount": 0,  # 최소 거래금액 (이상만 알림)
        "min_profit_rate": None,  # 최소 수익률 (이상만 알림, None=모든 거래)
        "exclude_stocks": [],  # 알림 제외할 종목코드 리스트
        "include_stocks": [],  # 알림 포함할 종목코드만 (빈 리스트=모든 종목)
        "market_hours_only": False,  # 장시간에만 알림 (True/False)
        "max_alerts_per_hour": 50  # 시간당 최대 알림 수
    },

    # 알림 시간 설정
    "time_settings": {
        "start_time": "08:30",  # 알림 시작 시간
        "end_time": "16:00",  # 알림 종료 시간
        "weekend_alerts": False,  # 주말 알림 여부
        "holiday_alerts": False  # 공휴일 알림 여부
    },

    # 메시지 설정
    "message_settings": {
        "use_emoji": True,  # 이모지 사용 여부
        "compact_mode": False,  # 간단 모드 (짧은 메시지)
        "include_condition_name": True,  # 조건식 이름 포함
        "include_profit_calc": True,  # 손익 계산 포함
        "grouping_enabled": True,  # 메시지 그룹화
        "grouping_interval": 60  # 그룹화 간격 (초)
    }

}
