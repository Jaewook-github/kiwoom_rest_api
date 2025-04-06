# 키움증권 자동매매 시스템

키움증권 API를 이용한 모듈식 자동매매 시스템입니다. 조건검색 기반 매수 및 실시간 익절/손절 자동화를 지원합니다.

## 주요 기능

- 조건검색 기반 종목 선정 및 매수
- 실시간 종목 모니터링 및 익절/손절 자동화
- 다양한 매매 전략 지원 (조건검색, 이동평균 교차 등)
- 웹소켓 연결 자동 복구 및 안정성 강화
- 주문 체결 관리 및 모니터링
- 텔레그램/이메일 알림 지원
- 일일/주간 리포트 생성
- API 서버를 통한 원격 모니터링 및 제어

## 설치 방법

### 필수 패키지 설치

```bash
pip install -r requirements.txt
```

### 환경 변수 설정

```bash
# API 토큰 설정
export KIWOOM_ACCESS_TOKEN="your_access_token"

# 알림 설정 (선택사항)
export TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
export TELEGRAM_CHAT_ID="your_telegram_chat_id"
export EMAIL_SENDER="your_email@gmail.com"
export EMAIL_PASSWORD="your_email_password"
export EMAIL_RECIPIENT="recipient@email.com"
```

## 실행 방법

### 조건검색 기반 전략 실행 (모의투자)

```bash
python main.py --strategy condition
```

### 이동평균 교차 전략 실행 (실전투자)

```bash
python main.py --strategy ma_cross --real
```

### 명령행 인자

- `--token`: 키움증권 접근 토큰 (환경 변수로 설정되어 있지 않은 경우)
- `--real`: 실전투자 모드 (지정하지 않으면 모의투자)
- `--strategy`: 매매 전략 (`condition` 또는 `ma_cross`)

## 프로젝트 구조

```
kiwoom_autotrader/
├── main.py                       # 메인 애플리케이션 진입점
├── config.py                     # 설정 파일
├── utils/                        # 유틸리티 모듈
├── api/                          # API 관련 모듈
├── core/                         # 핵심 모듈
├── strategies/                   # 매매 전략 모듈
├── analysis/                     # 분석 모듈 (향후 확장)
└── notification/                 # 알림 모듈
```

## 설정 파일

`config.json` 파일을 통해 시스템 설정을 변경할 수 있습니다. 기본 설정이 없는 경우 자동으로 생성됩니다.

```json
{
  "system": {
    "log_level": "INFO",
    "log_file": "auto_trading.log",
    "data_dir": "./trading_data"
  },
  "trading": {
    "max_budget_per_stock": 500000,
    "max_stocks": 5,
    "take_profit_pct": 2.0,
    "stop_loss_pct": -2.0
  },
  "market": {
    "start_time": "090000",
    "end_time": "153000"
  }
}
```

## API 서버

시스템에는 간단한 REST API 서버가 포함되어 있어 원격으로 상태 모니터링 및 제어가 가능합니다.

```
# 시스템 상태 조회
GET http://localhost:8080/api/status

# 계좌 정보 조회
GET http://localhost:8080/api/account

# 보유 종목 조회
GET http://localhost:8080/api/holdings

# 수동 매수 요청
POST http://localhost:8080/api/buy
{
  "stock_code": "005930",
  "quantity": 10
}
```

## 향후 개발 계획

- 백테스팅 기능 추가
- 다양한 기술적 분석 전략 추가
- 대시보드 UI 개발
- 데이터 분석 및 시각화 기능 강화

## 참고사항

- 이 시스템은 실제 투자에 활용하기 전에 충분한 테스트가 필요합니다.
- 자동매매 시스템의 특성상 예상치 못한 상황이 발생할 수 있으므로 주의가 필요합니다.
- 키움증권 API 정책이 변경될 경우 시스템이 정상 작동하지 않을 수 있습니다.