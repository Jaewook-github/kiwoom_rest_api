# Kiwoom Quant Dashboard

퀀트 투자 전략을 위한 키움증권 API 기반 대시보드 애플리케이션입니다.

## 주요 기능

- 키움증권 API 연동
- 실시간 시장 데이터 모니터링
- 다양한 퀀트 투자 전략 구현
  - 가치 투자 (마법공식, 피오트로스키 F-Score, 그레이엄)
  - 모멘텀 투자 (듀얼 모멘텀, 상대강도)
  - 퀄리티 투자 (퀄리티 팩터, 강환국 퀄리티)
  - 자산배분 (퀀트킹)
- 백테스팅 및 성과 분석
- 대시보드 시각화

## 설치 방법

1. 프로젝트 클론
```bash
git clone https://github.com/yourusername/kiwoom-quant-dashboard.git
cd kiwoom-quant-dashboard
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 의존성 패키지 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
`.env` 파일을 생성하고 필요한 환경 변수를 설정하세요.

5. 애플리케이션 실행
```bash
python run.py
```

## 환경 설정

1. 키움증권 API 설정
- 키움증권 Open API+ 설치
- 실투자 또는 모의투자 계정 로그인

2. 환경 변수 설정
`.env` 파일에 다음 변수들을 설정하세요:
```
KIWOOM_USER_ID=your_id
KIWOOM_USER_PASSWORD=your_password
KIWOOM_CERT_PASSWORD=your_cert_password
```

## 프로젝트 구조

```
kiwoom-quant-dashboard/
├── .env                    # 환경 변수 설정 파일 (API 키 등)
├── README.md               # 프로젝트 설명 문서
├── requirements.txt        # 필요한 패키지 목록
├── run.py                  # 애플리케이션 시작 스크립트
├── config/
│   ├── __init__.py
│   ├── settings.py         # 전역 설정
│   └── logging_config.py   # 로깅 설정
├── api/
│   ├── __init__.py
│   ├── kiwoom_api.py       # 키움증권 API 클라이언트
│   ├── data_provider.py    # 데이터 제공 클래스
│   └── models/             # 데이터 모델 정의
│       ├── __init__.py
│       ├── stock.py
│       ├── market.py
│       ├── account.py
│       └── financial.py
├── data/
│   ├── __init__.py
│   ├── fetcher.py          # 데이터 수집기
│   ├── processor.py        # 데이터 전처리기
│   └── cache.py            # 데이터 캐싱 관리
├── strategies/
│   ├── __init__.py
│   ├── base.py             # 전략 기본 클래스
│   ├── value/              # 가치 투자 전략
│   │   ├── __init__.py
│   │   ├── magic_formula.py   # 마법공식
│   │   ├── piotroski_f.py     # 피오트로스키 F-Score
│   │   └── graham.py          # 그레이엄 전략
│   ├── momentum/           # 모멘텀 투자 전략
│   │   ├── __init__.py
│   │   ├── dual_momentum.py   # 듀얼 모멘텀
│   │   └── relative_strength.py  # 상대강도
│   ├── quality/            # 퀄리티 투자 전략
│   │   ├── __init__.py
│   │   ├── quality_factor.py  # 퀄리티 팩터
│   │   └── kanghk_quality.py  # 강환국 퀄리티 전략
│   ├── asset_allocation/   # 자산배분 전략
│   │   ├── __init__.py
│   │   └── quant_king.py      # 퀀트킹 자산배분
│   └── custom/             # 사용자 정의 전략
│       ├── __init__.py
│       └── user_strategy.py   # 사용자 전략 템플릿
├── analysis/
│   ├── __init__.py
│   ├── backtest.py         # 백테스트 엔진
│   ├── performance.py      # 성과 분석
│   └── risk.py             # 리스크 분석
├── dashboard/
│   ├── __init__.py
│   ├── app.py              # 대시보드 앱
│   ├── callbacks.py        # 콜백 함수
│   ├── layouts/
│   │   ├── __init__.py
│   │   ├── main.py         # 메인 레이아웃
│   │   ├── market.py       # 시장 데이터 레이아웃
│   │   ├── portfolio.py    # 포트폴리오 레이아웃
│   │   ├── strategy.py     # 전략 레이아웃
│   │   └── analysis.py     # 분석 레이아웃
│   └── components/
│       ├── __init__.py
│       ├── charts.py       # 차트 컴포넌트
│       ├── tables.py       # 테이블 컴포넌트
│       └── forms.py        # 입력 폼 컴포넌트
└── utils/
    ├── __init__.py
    ├── date_utils.py       # 날짜 관련 유틸리티
    ├── financial_utils.py  # 재무 관련 유틸리티
    └── visualization.py    # 시각화 유틸리티
```
3. 주요 모듈 설명
3.1. API 모듈 (api/)
키움증권 REST API와의 통신을 담당하는 모듈입니다. API 클라이언트, 데이터 모델, 에러 처리 등을 포함합니다.

kiwoom_api.py: REST API 호출 및 응답 처리
data_provider.py: 각 데이터 유형별 API 호출 래퍼 함수 제공
models/: 주식, 시장, 계좌, 재무제표 등 데이터 모델 정의

3.2. 데이터 모듈 (data/)
데이터 수집, 전처리, 저장, 캐싱을 담당하는 모듈입니다.

fetcher.py: API를 통한 데이터 수집
processor.py: 수집된 데이터 전처리
cache.py: 데이터 캐싱을 통한 API 호출 최적화

3.3. 전략 모듈 (strategies/)
다양한 퀀트 투자 전략을 구현한 모듈입니다.

base.py: 모든 전략의 기본 클래스 정의
value/: 가치투자 전략 (마법공식, 피오트로스키 F-Score 등)
momentum/: 모멘텀 투자 전략 (듀얼 모멘텀, 상대 강도 등)
quality/: 퀄리티 투자 전략 (강환국 퀄리티 전략 등)
asset_allocation/: 자산배분 전략 (퀀트킹 등)
custom/: 사용자 정의 전략을 추가할 수 있는 영역

3.4. 분석 모듈 (analysis/)
백테스트, 성과 분석, 리스크 분석을 담당하는 모듈입니다.

backtest.py: 과거 데이터를 사용한 전략 백테스팅
performance.py: 성과 지표 계산 (샤프 비율, 최대 낙폭 등)
risk.py: 리스크 지표 계산 (변동성, 베타 등)

3.5. 대시보드 모듈 (dashboard/)
웹 기반 대시보드 UI를 담당하는 모듈입니다.

app.py: Dash 애플리케이션 초기화 및 실행
callbacks.py: 대시보드 인터랙션 콜백 함수
layouts/: 각 페이지별 레이아웃 정의
components/: 재사용 가능한 UI 컴포넌트

3.6. 유틸리티 모듈 (utils/)
프로젝트 전반에서 사용되는 유틸리티 함수를 제공하는 모듈입니다.

date_utils.py: 날짜 관련 유틸리티
financial_utils.py: 재무 관련 유틸리티
visualization.py: 시각화 유틸리티

4. 주요 퀀트 투자 전략
4.1. 마법공식 (Magic Formula)
조엘 그린블라트의 마법공식은 두 가지 지표를 결합한 전략입니다:

영업이익률(EBIT/EV): 기업가치 대비 영업이익이 높은 종목
자본수익률(ROC): 투자자본 대비 영업이익이 높은 종목

두 지표에 대한 순위를 합산하여 최종 순위가 높은 종목을 선정합니다.
4.2. 강환국 퀄리티 전략
강환국의 퀀트 투자 전략은 다음 지표들을 결합합니다:

PER (주가수익비율) - 낮을수록 유리
PBR (주가순자산비율) - 낮을수록 유리
ROE (자기자본이익률) - 높을수록 유리
GP/A (총자산 대비 매출총이익) - 높을수록 유리

각 지표에 대한 순위를 합산하여 최종 순위가 높은 종목을 선정합니다.
4.3. 퀀트킹 자산배분 전략
퀀트킹의 자산배분 전략은 시장 상황에 따라 주식, 채권, 금, 현금의 비중을 조절하는 전략입니다. 주요 지표로 모멘텀, 추세, 변동성 등을 활용합니다.
4.4. 기타 구현 예정 전략

피오트로스키 F-Score
듀얼 모멘텀
그레이엄 가치투자
상대 강도 전략 (RSI)
및 기타 사용자 정의 전략

5. 사용 방법
5.1. 설치 및 설정
bash# 저장소 클론
git clone https://github.com/your-username/kiwoom-quant-dashboard.git
cd kiwoom-quant-dashboard

# 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows의 경우: venv\Scripts\activate

# 필요한 패키지 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 API 키 등 설정
5.2. 대시보드 실행
bashpython run.py
대시보드가 실행되면 웹 브라우저에서 http://localhost:8050으로 접속할 수 있습니다.
5.3. 사용자 정의 전략 추가
strategies/custom/user_strategy.py 파일을 템플릿으로 사용하여 자신만의 전략을 추가할 수 있습니다. 전략 클래스는 strategies/base.py의 StrategyBase 클래스를 상속받아야 합니다.
6. 확장 및 개선 계획

기계학습 기반 예측 모델 통합
실시간 알림 시스템
자동매매 기능
추가 퀀트 전략 구현
모바일 지원

7. 참고 자료

키움증권 REST API 개발 가이드
조엘 그린블라트 "주식시장을 이기는 작은 책"
강환국 "할 수 있다! 퀀트 투자"
퀀트킹 관련 자료
## 라이선스

MIT License
