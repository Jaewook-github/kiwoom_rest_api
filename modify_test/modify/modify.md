# 키움증권 자동매매 시스템 UI 미리보기

## 🏠 메인 창 구조

### 창 제목 및 기본 정보
- **창 제목**: "키움증권 자동매매 시스템 v2.2 (유연한 매도조건)"
- **창 크기**: 1500 x 1000 픽셀
- **스타일**: Fusion 테마로 모던한 디자인

---

## 📋 메뉴바

### 파일(F) 메뉴
- **설정 저장(S)** - `Ctrl+S`
- *(구분선)*
- **종료(X)** - `Ctrl+Q`

### 도구(T) 메뉴
- **데이터 초기화(R)**

---

## 📊 상태바 (하단)

```
[상태: 연결완료] | [자동매매: 실행중] | [매도: 자동매도] | [활성 조건식: 3/5] | [실시간: 45/95] |                    [15:23:45]
```

**상태 표시 요소들:**
- 🔗 **연결 상태**: 대기중(주황) / 완료(녹색) / 실패(빨강)
- 🤖 **자동매매 상태**: 중지(빨강) / 실행중(녹색)
- 📈 **매도 방식**: 자동매도(파랑) / 조건식+자동(주황)
- 📊 **활성 조건식**: 현재/전체 개수
- 📡 **실시간 등록**: 현재/최대(95) 종목수
- 🕐 **현재 시간**: 실시간 업데이트

---

## 🗂️ 탭 구성

## 1️⃣ 자동매매 탭

### 🎮 컨트롤 패널 (상단)

#### 좌측: 자동매매 제어
```
┌─ 자동매매 제어 ─────────────────────┐
│ [자동매매 시작]  [자동매매 중지]      │
│                                      │
│ ┌─ 📊 조건식 관리 ─────────────────┐ │
│ │ 📋 조건식별 매매시간 설정         │ │
│ │ [⏰ 쉬운 시간 설정]               │ │
│ │ ⏰ 시간 설정: 전체 통일(09:00~15:30) │
│ │                                   │ │
│ │ ┌─ 🔵 매수 조건식 (최소 3개) ───┐ │ │
│ │ │ ☐ 📈 상승추세 조건식          │ │ │
│ │ │ ☑ 📈 거래량 급증 조건식       │ │ │
│ │ │ ☑ 📈 기술적 돌파 조건식       │ │ │
│ │ │ ☑ 📈 하락추세 조건식          │ │ │
│ │ └─────────────────────────────┘ │ │
│ │                                   │ │
│ │ ┌─ 🔴 매도 조건식 설정 ─────────┐ │ │
│ │ │ ● 🤖 자동 매도만 사용         │ │ │
│ │ │ ○ ⚙️ 조건식 매도 + 자동 매도  │ │ │
│ │ │                               │ │ │
│ │ │ [매도 조건식 리스트]          │ │ │
│ │ │ (비활성화 상태)               │ │ │
│ │ └─────────────────────────────┘ │ │
│ │                                   │ │
│ │ 📋 선택: 매수 3개, 매도: 🤖 자동매도 │ │
│ └───────────────────────────────┘ │
└──────────────────────────────────┘
```

#### 중앙: 매수/매도 설정
```
┌─ 매수/매도 설정 ──────────────────┐
│ ┌─ 매수 설정 ─────────────────┐  │
│ │ 매수 금액: [200,000]        │  │
│ │ 매수 방식: ● 시장가 ○ 지정가 │  │
│ │ 지정가 틱: [0] 틱           │  │
│ └─────────────────────────────┘  │
│                                  │
│ ┌─ 매도 설정 ─────────────────┐  │
│ │ 매도 방식: ● 시장가 ○ 지정가 │  │
│ │ 지정가 틱: [0] 틱           │  │
│ └─────────────────────────────┘  │
└──────────────────────────────────┘
```

#### 우측: 리스크 관리
```
┌─ 리스크 관리 (자동매도) ──────────┐
│ 💡 자동매도는 항상 활성화됩니다    │
│                                  │
│ ☑ 스탑로스 사용  [-2.0] %        │
│                                  │
│ ☑ 트레일링 스탑 사용             │
│   발동 수익률: [2.0] %           │
│   청산 하락률: [-1.0] %          │
│                                  │
│ 최대 보유종목: [10]              │
│ 정정주문 시간: [60] 초           │
│                                  │
│         [설정 저장]              │
└──────────────────────────────────┘
```

### 📊 데이터 테이블 영역 (하단)

#### 실시간 트래킹 테이블
```
┌─ 실시간 트래킹 ─────────────────────────────────────────────────────────────┐
│ 종목명     │ 현재가  │ 매입가  │ 수익률(%) │ 트레일링발동 │ 매수주문 │ 진입조건식   │
├───────────┼────────┼────────┼─────────┼────────────┼────────┼────────────┤
│ 삼성전자    │ 82,500 │ 80,000 │   +3.12  │    True    │  True  │ 상승추세    │
│ SK하이닉스  │125,000 │128,000 │   -2.34  │   False    │  True  │ 거래량급증  │
│ NAVER      │215,000 │210,000 │   +2.38  │    True    │  True  │ 기술적돌파  │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 주문 정보 테이블
```
┌─ 주문 정보 ───────────────────────────────────────────────────────────────┐
│ 주문접수시간 │ 종목코드 │ 주문수량 │ 매수매도구분 │ 발생조건식                │
├─────────────┼─────────┼─────────┼────────────┼─────────────────────────┤
│ 14:25:30    │ 005930  │   100   │    매수     │ 상승추세 조건식          │
│ 14:30:15    │ 000660  │    50   │    매도     │ 스탑로스(-2.1%)         │
│ 14:35:45    │ 035420  │    75   │    매수     │ 거래량 급증 조건식       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2️⃣ 계좌 정보 탭

### 계좌 보유 현황 테이블
```
┌─ 계좌 보유 현황 ─────────────────────────────────────────────────────────┐
│ 종목명     │ 현재가    │ 매입가    │ 보유수량 │ 매매가능수량 │ 수익률(%)  │
├───────────┼──────────┼──────────┼─────────┼────────────┼──────────┤
│ 삼성전자    │  82,500  │  80,000  │   100   │     100    │  +3.12   │
│ SK하이닉스  │ 125,000  │ 128,000  │    50   │      50    │  -2.34   │
│ NAVER      │ 215,000  │ 210,000  │    30   │      30    │  +2.38   │
│ 카카오      │  98,500  │ 100,000  │    25   │      25    │  -1.50   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3️⃣ 설정 탭

### API 설정
```
┌─ API 설정 ────────────────────────────┐
│ API Key:    [********************]   │
│ API Secret: [********************]   │
│ API URL:    [https://mockapi.ki...]  │
└───────────────────────────────────────┘
```

---

## 4️⃣ 로그 탭

### 로그 출력 영역
```
┌─ 로그 출력 ─────────────────────────────────────────────────────────────┐
│ [15:20:30] 자동매매 시작 - 매수조건 3개, 매도: 자동매도만                │
│ [15:20:35] 매수 신호: 005930 (조건식: 상승추세 조건식)                  │
│ [15:20:40] 매수 주문: 005930 100주 시장가 (진입: 상승추세 조건식)       │
│ [15:20:45] 주문 접수: 005930 매수                                      │
│ [15:20:50] 주문 체결: 005930 매수                                      │
│ [15:25:10] 트레일링 스탑 발동: 005930 수익률 2.12%                     │
│ [15:30:25] 매도 주문: 000660 50주 시장가 - 스탑로스 (-2.34%)          │
│                                                                        │
│ [로그 지우기]  [로그 저장]                                             │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🎨 UI 디자인 특징

### 색상 체계
- **배경색**: `#f5f5f5` (연한 회색)
- **기본 텍스트**: 검정색
- **성공/매수**: `#4CAF50` (녹색)
- **위험/매도**: `#f44336` (빨간색)
- **정보/선택**: `#2196F3` (파란색)
- **경고**: `#FF9800` (주황색)
- **수익**: 빨간색, **손실**: 파란색

### 스타일링 특징
- **모던한 디자인**: 둥근 모서리, 그라데이션 효과
- **아이콘 활용**: 이모지를 적극 활용한 직관적 UI
- **그룹박스**: 섹션별로 명확한 구분
- **반응형 요소**: 호버 효과, 클릭 애니메이션
- **시각적 계층**: 글꼴 크기와 굵기로 정보 우선순위 표현

---

## 🎯 주요 UI 컴포넌트

### FlexibleSellConditionWidget (핵심 위젯)
```
📊 조건식 관리
├── 🔵 매수 조건식 (다중 선택)
├── 🔴 매도 조건식 설정
│   ├── 🤖 자동 매도만 사용 (라디오버튼)
│   └── ⚙️ 조건식 매도 + 자동 매도 (라디오버튼)
├── ⏰ 쉬운 시간 설정 버튼
├── 📋 선택 상태 표시
└── ✅ 선택 검증 기능
```

### EasyTimeSettingDialog (시간 설정 팝업)
```
📅 조건식 매매시간 설정 (쉬운 버전)
├── 🌍 전체 적용 탭
│   ├── ⚡ 빠른 설정 버튼들
│   ├── 🕘 시작/종료 시간 설정
│   └── 🔄 모든 조건식에 적용
└── ⚙️ 개별 설정 탭
    └── 조건식별 개별 시간 설정
```

### StatusWidget (상태 표시)
```
[연결상태] | [자동매매상태] | [매도방식] | [활성조건식] | [실시간등록] | [시간]
```

---

## 📱 사용자 경험 (UX) 요소

### 직관적 안내
- 💡 **도움말 버튼**: 각 섹션별 상세 가이드
- 🔍 **미리보기 기능**: 설정 확인 가능
- ⚠️ **검증 메시지**: 잘못된 설정 시 친절한 안내
- ✅ **성공 알림**: 설정 완료 시 확인 메시지

### 시각적 피드백
- **색상 변화**: 상태에 따른 동적 색상 변경
- **아이콘 표시**: 체크박스, 라디오버튼의 시각적 표현
- **진행 상태**: 실시간 데이터 업데이트 표시
- **호버 효과**: 버튼에 마우스 올릴 때 색상 변화

### 접근성
- **키보드 단축키**: Ctrl+S (저장), Ctrl+Q (종료)
- **탭 네비게이션**: 논리적 탭 순서
- **명확한 레이블**: 모든 입력 요소에 설명
- **상태 표시**: 현재 상태를 명확히 표시

---

## 🔧 기능별 UI 상세

### 자동매매 시작/중지
- **시작 버튼**: 녹색, "자동매매 시작"
- **중지 버튼**: 빨간색, "자동매매 중지"
- **상태 변화**: 버튼 활성화/비활성화로 현재 상태 표시

### 조건식 선택
- **매수 조건식**: 파란색 테두리, 다중 선택 가능
- **매도 조건식**: 빨간색 테두리, 조건부 활성화
- **선택 카운터**: 하단에 실시간 선택 개수 표시

### 시간 설정
- **전체 적용**: 간편한 일괄 설정
- **개별 설정**: 세밀한 조건식별 설정
- **빠른 설정**: 자주 사용하는 시간대 원클릭 설정

이 UI 구성은 사용자가 복잡한 자동매매 시스템을 직관적이고 안전하게 조작할 수 있도록 설계되었습니다.


# 키움증권 자동매매 시스템 UI 미리보기 (SVG)

## 🖥️ 전체 메인 창 구조

<svg width="1000" height="700" xmlns="http://www.w3.org/2000/svg">
  <!-- 메인 창 -->
  <rect x="10" y="10" width="980" height="680" fill="#f5f5f5" stroke="#ccc" stroke-width="2" rx="8"/>
  
  <!-- 타이틀 바 -->
  <rect x="10" y="10" width="980" height="40" fill="#2196F3" rx="8 8 0 0"/>
  <text x="30" y="32" fill="white" font-family="Arial" font-size="14" font-weight="bold">
    키움증권 자동매매 시스템 v2.2 (유연한 매도조건)
  </text>
  
  <!-- 창 컨트롤 버튼 -->
  <circle cx="950" cy="30" r="8" fill="#ff5f57"/>
  <circle cx="970" cy="30" r="8" fill="#ffbd2e"/>
  <circle cx="930" cy="30" r="8" fill="#28ca42"/>
  
  <!-- 메뉴바 -->
  <rect x="10" y="50" width="980" height="25" fill="#e9e9e9" stroke="#ccc"/>
  <text x="25" y="67" font-family="Arial" font-size="12">파일(F)</text>
  <text x="85" y="67" font-family="Arial" font-size="12">도구(T)</text>
  
  <!-- 탭 영역 -->
  <rect x="20" y="85" width="960" height="35" fill="#ffffff" stroke="#e0e0e0"/>
  
  <!-- 탭 버튼들 -->
  <rect x="25" y="90" width="100" height="25" fill="#2196F3" rx="4 4 0 0"/>
  <text x="65" y="107" fill="white" font-family="Arial" font-size="11" text-anchor="middle">자동매매</text>
  
  <rect x="125" y="90" width="100" height="25" fill="#e9e9e9" stroke="#ccc" rx="4 4 0 0"/>
  <text x="175" y="107" fill="#666" font-family="Arial" font-size="11" text-anchor="middle">계좌 정보</text>
  
  <rect x="225" y="90" width="100" height="25" fill="#e9e9e9" stroke="#ccc" rx="4 4 0 0"/>
  <text x="275" y="107" fill="#666" font-family="Arial" font-size="11" text-anchor="middle">설정</text>
  
  <rect x="325" y="90" width="100" height="25" fill="#e9e9e9" stroke="#ccc" rx="4 4 0 0"/>
  <text x="375" y="107" fill="#666" font-family="Arial" font-size="11" text-anchor="middle">로그</text>
  
  <!-- 컨텐츠 영역 -->
  <rect x="20" y="120" width="960" height="520" fill="#ffffff" stroke="#e0e0e0"/>
  
  <!-- 상태바 -->
  <rect x="10" y="650" width="980" height="30" fill="#f0f0f0" stroke="#ccc"/>
  <text x="25" y="668" font-family="Arial" font-size="11" fill="#4CAF50">상태: 연결완료</text>
  <text x="150" y="668" font-family="Arial" font-size="11">|</text>
  <text x="170" y="668" font-family="Arial" font-size="11" fill="#4CAF50">자동매매: 실행중</text>
  <text x="300" y="668" font-family="Arial" font-size="11">|</text>
  <text x="320" y="668" font-family="Arial" font-size="11" fill="#2196F3">매도: 자동매도</text>
  <text x="450" y="668" font-family="Arial" font-size="11">|</text>
  <text x="470" y="668" font-family="Arial" font-size="11">활성 조건식: 3/5</text>
  <text x="580" y="668" font-family="Arial" font-size="11">|</text>
  <text x="600" y="668" font-family="Arial" font-size="11">실시간: 45/95</text>
  <text x="850" y="668" font-family="Arial" font-size="11" fill="#666">15:23:45</text>
</svg>

---

## 🎮 자동매매 탭 - 컨트롤 패널

<svg width="1000" height="400" xmlns="http://www.w3.org/2000/svg">
  <!-- 전체 컨트롤 패널 -->
  <rect x="10" y="10" width="980" height="380" fill="#ffffff" stroke="#e0e0e0" stroke-width="1" rx="8"/>
  
  <!-- 좌측: 자동매매 제어 영역 -->
  <rect x="20" y="20" width="300" height="360" fill="#f8fff8" stroke="#4CAF50" stroke-width="2" rx="8"/>
  <text x="30" y="40" font-family="Arial" font-size="14" font-weight="bold" fill="#4CAF50">🎮 자동매매 제어</text>
  
  <!-- 자동매매 버튼들 -->
  <rect x="30" y="50" width="120" height="35" fill="#4CAF50" rx="6"/>
  <text x="90" y="72" fill="white" font-family="Arial" font-size="12" text-anchor="middle" font-weight="bold">자동매매 시작</text>
  
  <rect x="160" y="50" width="120" height="35" fill="#f44336" rx="6"/>
  <text x="220" y="72" fill="white" font-family="Arial" font-size="12" text-anchor="middle" font-weight="bold">자동매매 중지</text>
  
  <!-- 조건식 관리 영역 -->
  <rect x="30" y="100" width="270" height="270" fill="#ffffff" stroke="#2196F3" stroke-width="2" rx="6"/>
  <text x="40" y="120" font-family="Arial" font-size="12" font-weight="bold" fill="#2196F3">📊 조건식 관리</text>
  
  <!-- 시간 설정 버튼 -->
  <rect x="150" y="105" width="120" height="25" fill="#FF9800" rx="4"/>
  <text x="210" y="122" fill="white" font-family="Arial" font-size="10" text-anchor="middle">⏰ 쉬운 시간 설정</text>
  
  <!-- 매수 조건식 영역 -->
  <rect x="40" y="140" width="250" height="100" fill="#e8f5e8" stroke="#4CAF50" rx="4"/>
  <text x="50" y="155" font-family="Arial" font-size="11" font-weight="bold" fill="#4CAF50">🔵 매수 조건식 (최소 3개)</text>
  
  <!-- 체크박스들 -->
  <rect x="50" y="165" width="12" height="12" fill="#4CAF50" rx="2"/>
  <text x="70" y="175" font-family="Arial" font-size="10">📈 상승추세 조건식</text>
  
  <rect x="50" y="185" width="12" height="12" fill="#4CAF50" rx="2"/>
  <text x="70" y="195" font-family="Arial" font-size="10">📈 거래량 급증 조건식</text>
  
  <rect x="50" y="205" width="12" height="12" fill="#4CAF50" rx="2"/>
  <text x="70" y="215" font-family="Arial" font-size="10">📈 기술적 돌파 조건식</text>
  
  <!-- 매도 조건식 영역 -->
  <rect x="40" y="250" width="250" height="110" fill="#fff8f8" stroke="#FF5722" rx="4"/>
  <text x="50" y="265" font-family="Arial" font-size="11" font-weight="bold" fill="#FF5722">🔴 매도 조건식 설정</text>
  
  <!-- 라디오 버튼들 -->
  <circle cx="56" cy="280" r="6" fill="#2196F3"/>
  <text x="70" y="285" font-family="Arial" font-size="10" fill="#2196F3">🤖 자동 매도만 사용</text>
  
  <circle cx="56" cy="300" r="6" fill="none" stroke="#FF9800" stroke-width="2"/>
  <text x="70" y="305" font-family="Arial" font-size="10" fill="#FF9800">⚙️ 조건식 매도 + 자동 매도</text>
  
  <!-- 선택 상태 표시 -->
  <rect x="40" y="320" width="250" height="25" fill="#e3f2fd" stroke="#2196F3" rx="4"/>
  <text x="50" y="337" font-family="Arial" font-size="10" fill="#2196F3">📋 선택: 매수 3개, 매도: 🤖 자동매도</text>
  
  <!-- 중앙: 매수/매도 설정 -->
  <rect x="340" y="20" width="300" height="360" fill="#ffffff" stroke="#cccccc" stroke-width="2" rx="8"/>
  <text x="350" y="40" font-family="Arial" font-size="14" font-weight="bold">⚙️ 매수/매도 설정</text>
  
  <!-- 매수 설정 -->
  <rect x="350" y="50" width="280" height="150" fill="#f0f8ff" stroke="#2196F3" rx="6"/>
  <text x="360" y="70" font-family="Arial" font-size="12" font-weight="bold" fill="#2196F3">💰 매수 설정</text>
  
  <text x="360" y="90" font-family="Arial" font-size="10">매수 금액:</text>
  <rect x="430" y="80" width="120" height="20" fill="white" stroke="#ccc" rx="3"/>
  <text x="490" y="93" font-family="Arial" font-size="10" text-anchor="middle">200,000</text>
  
  <text x="360" y="115" font-family="Arial" font-size="10">매수 방식:</text>
  <circle cx="430" cy="112" r="5" fill="#2196F3"/>
  <text x="445" y="116" font-family="Arial" font-size="9">시장가</text>
  <circle cx="500" cy="112" r="5" fill="none" stroke="#ccc" stroke-width="1"/>
  <text x="515" y="116" font-family="Arial" font-size="9">지정가</text>
  
  <text x="360" y="140" font-family="Arial" font-size="10">지정가 틱:</text>
  <rect x="430" y="130" width="60" height="20" fill="white" stroke="#ccc" rx="3"/>
  <text x="460" y="143" font-family="Arial" font-size="10" text-anchor="middle">0</text>
  
  <!-- 매도 설정 -->
  <rect x="350" y="210" width="280" height="120" fill="#fff0f0" stroke="#f44336" rx="6"/>
  <text x="360" y="230" font-family="Arial" font-size="12" font-weight="bold" fill="#f44336">📉 매도 설정</text>
  
  <text x="360" y="250" font-family="Arial" font-size="10">매도 방식:</text>
  <circle cx="430" cy="247" r="5" fill="#f44336"/>
  <text x="445" y="251" font-family="Arial" font-size="9">시장가</text>
  <circle cx="500" cy="247" r="5" fill="none" stroke="#ccc" stroke-width="1"/>
  <text x="515" y="251" font-family="Arial" font-size="9">지정가</text>
  
  <text x="360" y="275" font-family="Arial" font-size="10">지정가 틱:</text>
  <rect x="430" y="265" width="60" height="20" fill="white" stroke="#ccc" rx="3"/>
  <text x="460" y="278" font-family="Arial" font-size="10" text-anchor="middle">0</text>
  
  <!-- 우측: 리스크 관리 -->
  <rect x="660" y="20" width="320" height="360" fill="#f8fff8" stroke="#4CAF50" stroke-width="2" rx="8"/>
  <text x="670" y="40" font-family="Arial" font-size="14" font-weight="bold" fill="#4CAF50">🛡️ 리스크 관리 (자동매도)</text>
  
  <!-- 안내 메시지 -->
  <rect x="670" y="50" width="300" height="25" fill="#e3f2fd" stroke="#2196F3" rx="4"/>
  <text x="680" y="67" font-family="Arial" font-size="10" fill="#2196F3">💡 자동매도는 항상 활성화됩니다</text>
  
  <!-- 스탑로스 설정 -->
  <rect x="680" y="85" width="12" height="12" fill="#4CAF50" rx="2"/>
  <text x="700" y="95" font-family="Arial" font-size="10">스탑로스 사용</text>
  <rect x="820" y="82" width="60" height="18" fill="white" stroke="#ccc" rx="3"/>
  <text x="850" y="94" font-family="Arial" font-size="9" text-anchor="middle">-2.0 %</text>
  
  <!-- 트레일링 스탑 설정 -->
  <rect x="680" y="110" width="12" height="12" fill="#4CAF50" rx="2"/>
  <text x="700" y="120" font-family="Arial" font-size="10">트레일링 스탑 사용</text>
  
  <text x="690" y="140" font-family="Arial" font-size="9">발동 수익률:</text>
  <rect x="780" y="133" width="60" height="18" fill="white" stroke="#ccc" rx="3"/>
  <text x="810" y="145" font-family="Arial" font-size="9" text-anchor="middle">2.0 %</text>
  
  <text x="690" y="160" font-family="Arial" font-size="9">청산 하락률:</text>
  <rect x="780" y="153" width="60" height="18" fill="white" stroke="#ccc" rx="3"/>
  <text x="810" y="165" font-family="Arial" font-size="9" text-anchor="middle">-1.0 %</text>
  
  <!-- 기타 설정 -->
  <text x="680" y="190" font-family="Arial" font-size="10">최대 보유종목:</text>
  <rect x="820" y="183" width="60" height="18" fill="white" stroke="#ccc" rx="3"/>
  <text x="850" y="195" font-family="Arial" font-size="9" text-anchor="middle">10</text>
  
  <text x="680" y="210" font-family="Arial" font-size="10">정정주문 시간:</text>
  <rect x="820" y="203" width="60" height="18" fill="white" stroke="#ccc" rx="3"/>
  <text x="850" y="215" font-family="Arial" font-size="9" text-anchor="middle">60 초</text>
  
  <!-- 설정 저장 버튼 -->
  <rect x="720" y="250" width="120" height="30" fill="#2196F3" rx="6"/>
  <text x="780" y="270" fill="white" font-family="Arial" font-size="11" text-anchor="middle" font-weight="bold">설정 저장</text>
</svg>

---

## 📊 데이터 테이블 영역

<svg width="1000" height="350" xmlns="http://www.w3.org/2000/svg">
  <!-- 실시간 트래킹 테이블 -->
  <rect x="10" y="10" width="980" height="200" fill="#ffffff" stroke="#4CAF50" stroke-width="2" rx="8"/>
  <text x="20" y="30" font-family="Arial" font-size="14" font-weight="bold" fill="#4CAF50">📈 실시간 트래킹</text>
  
  <!-- 테이블 헤더 -->
  <rect x="20" y="40" width="960" height="25" fill="#f0f8ff" stroke="#2196F3"/>
  <text x="30" y="57" font-family="Arial" font-size="10" font-weight="bold">종목명</text>
  <text x="120" y="57" font-family="Arial" font-size="10" font-weight="bold">현재가</text>
  <text x="200" y="57" font-family="Arial" font-size="10" font-weight="bold">매입가</text>
  <text x="280" y="57" font-family="Arial" font-size="10" font-weight="bold">수익률(%)</text>
  <text x="380" y="57" font-family="Arial" font-size="10" font-weight="bold">트레일링발동</text>
  <text x="500" y="57" font-family="Arial" font-size="10" font-weight="bold">매수주문</text>
  <text x="600" y="57" font-family="Arial" font-size="10" font-weight="bold">매도주문</text>
  <text x="700" y="57" font-family="Arial" font-size="10" font-weight="bold">진입조건식</text>
  
  <!-- 테이블 행들 -->
  <rect x="20" y="65" width="960" height="20" fill="#ffffff" stroke="#e0e0e0"/>
  <text x="30" y="79" font-family="Arial" font-size="9">삼성전자</text>
  <text x="120" y="79" font-family="Arial" font-size="9">82,500</text>
  <text x="200" y="79" font-family="Arial" font-size="9">80,000</text>
  <text x="280" y="79" font-family="Arial" font-size="9" fill="#f44336">+3.12</text>
  <text x="390" y="79" font-family="Arial" font-size="9" fill="#4CAF50">True</text>
  <text x="510" y="79" font-family="Arial" font-size="9" fill="#4CAF50">True</text>
  <text x="610" y="79" font-family="Arial" font-size="9">False</text>
  <text x="710" y="79" font-family="Arial" font-size="9">상승추세</text>
  
  <rect x="20" y="85" width="960" height="20" fill="#f9f9f9" stroke="#e0e0e0"/>
  <text x="30" y="99" font-family="Arial" font-size="9">SK하이닉스</text>
  <text x="120" y="99" font-family="Arial" font-size="9">125,000</text>
  <text x="200" y="99" font-family="Arial" font-size="9">128,000</text>
  <text x="280" y="99" font-family="Arial" font-size="9" fill="#2196F3">-2.34</text>
  <text x="390" y="99" font-family="Arial" font-size="9">False</text>
  <text x="510" y="99" font-family="Arial" font-size="9" fill="#4CAF50">True</text>
  <text x="610" y="99" font-family="Arial" font-size="9">False</text>
  <text x="710" y="99" font-family="Arial" font-size="9">거래량급증</text>
  
  <rect x="20" y="105" width="960" height="20" fill="#ffffff" stroke="#e0e0e0"/>
  <text x="30" y="119" font-family="Arial" font-size="9">NAVER</text>
  <text x="120" y="119" font-family="Arial" font-size="9">215,000</text>
  <text x="200" y="119" font-family="Arial" font-size="9">210,000</text>
  <text x="280" y="119" font-family="Arial" font-size="9" fill="#f44336">+2.38</text>
  <text x="390" y="119" font-family="Arial" font-size="9" fill="#4CAF50">True</text>
  <text x="510" y="119" font-family="Arial" font-size="9" fill="#4CAF50">True</text>
  <text x="610" y="119" font-family="Arial" font-size="9">False</text>
  <text x="710" y="119" font-family="Arial" font-size="9">기술적돌파</text>
  
  <!-- 주문 정보 테이블 -->
  <rect x="10" y="230" width="980" height="110" fill="#ffffff" stroke="#FF5722" stroke-width="2" rx="8"/>
  <text x="20" y="250" font-family="Arial" font-size="14" font-weight="bold" fill="#FF5722">📋 주문 정보</text>
  
  <!-- 테이블 헤더 -->
  <rect x="20" y="260" width="960" height="25" fill="#fff0f0" stroke="#FF5722"/>
  <text x="30" y="277" font-family="Arial" font-size="10" font-weight="bold">주문접수시간</text>
  <text x="150" y="277" font-family="Arial" font-size="10" font-weight="bold">종목코드</text>
  <text x="250" y="277" font-family="Arial" font-size="10" font-weight="bold">주문수량</text>
  <text x="350" y="277" font-family="Arial" font-size="10" font-weight="bold">매수매도구분</text>
  <text x="500" y="277" font-family="Arial" font-size="10" font-weight="bold">발생조건식</text>
  
  <!-- 주문 정보 행들 -->
  <rect x="20" y="285" width="960" height="18" fill="#ffffff" stroke="#e0e0e0"/>
  <text x="30" y="297" font-family="Arial" font-size="9">14:25:30</text>
  <text x="150" y="297" font-family="Arial" font-size="9">005930</text>
  <text x="260" y="297" font-family="Arial" font-size="9">100</text>
  <text x="360" y="297" font-family="Arial" font-size="9" fill="#4CAF50">매수</text>
  <text x="510" y="297" font-family="Arial" font-size="9">상승추세 조건식</text>
  
  <rect x="20" y="303" width="960" height="18" fill="#f9f9f9" stroke="#e0e0e0"/>
  <text x="30" y="315" font-family="Arial" font-size="9">14:30:15</text>
  <text x="150" y="315" font-family="Arial" font-size="9">000660</text>
  <text x="260" y="315" font-family="Arial" font-size="9">50</text>
  <text x="360" y="315" font-family="Arial" font-size="9" fill="#f44336">매도</text>
  <text x="510" y="315" font-family="Arial" font-size="9">스탑로스(-2.1%)</text>
</svg>

---

## ⏰ 쉬운 시간 설정 다이얼로그

<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
  <!-- 다이얼로그 창 -->
  <rect x="10" y="10" width="780" height="580" fill="#ffffff" stroke="#2196F3" stroke-width="3" rx="12"/>
  
  <!-- 타이틀 바 -->
  <rect x="10" y="10" width="780" height="50" fill="#2196F3" rx="12 12 0 0"/>
  <text x="30" y="40" fill="white" font-family="Arial" font-size="16" font-weight="bold">📅 조건식 매매시간 설정 (쉬운 버전)</text>
  
  <!-- 도움말 버튼 -->
  <rect x="680" y="20" width="80" height="30" fill="#FF9800" rx="6"/>
  <text x="720" y="40" fill="white" font-family="Arial" font-size="12" text-anchor="middle">❓ 도움말</text>
  
  <!-- 안내 메시지 -->
  <rect x="20" y="70" width="760" height="60" fill="#f0f8ff" stroke="#e3f2fd" stroke-width="2" rx="8"/>
  <text x="30" y="90" font-family="Arial" font-size="12" font-weight="bold" fill="#2196F3">💡 간단 설정 가이드:</text>
  <text x="30" y="110" font-family="Arial" font-size="11">• 전체 적용: 모든 조건식에 동일한 시간 적용</text>
  <text x="30" y="125" font-family="Arial" font-size="11">• 개별 설정: 조건식마다 다른 시간 설정</text>
  
  <!-- 탭 영역 -->
  <rect x="20" y="140" width="760" height="30" fill="#f5f5f5" stroke="#e0e0e0"/>
  
  <!-- 전체 적용 탭 (활성) -->
  <rect x="25" y="145" width="120" height="25" fill="#ffffff" stroke="#2196F3" stroke-width="3" rx="6 6 0 0"/>
  <text x="85" y="162" fill="#2196F3" font-family="Arial" font-size="12" text-anchor="middle" font-weight="bold">🌍 전체 적용</text>
  
  <!-- 개별 설정 탭 -->
  <rect x="145" y="145" width="120" height="25" fill="#f5f5f5" stroke="#cccccc" rx="6 6 0 0"/>
  <text x="205" y="162" fill="#666" font-family="Arial" font-size="12" text-anchor="middle">⚙️ 개별 설정</text>
  
  <!-- 전체 적용 탭 내용 -->
  <rect x="20" y="170" width="760" height="320" fill="#ffffff" stroke="#e0e0e0"/>
  
  <!-- 전체 설정 그룹 -->
  <rect x="40" y="190" width="720" height="280" fill="#f8fff8" stroke="#4CAF50" stroke-width="2" rx="8"/>
  <text x="50" y="210" font-family="Arial" font-size="14" font-weight="bold" fill="#4CAF50">🌍 모든 조건식에 동일한 시간 적용</text>
  
  <!-- 전체 활성화 체크박스 -->
  <rect x="60" y="225" width="15" height="15" fill="#4CAF50" rx="3"/>
  <text x="85" y="238" font-family="Arial" font-size="12" font-weight="bold" fill="#2E7D32">✅ 전체 조건식 시간 제한 활성화</text>
  
  <!-- 시간 설정 영역 -->
  <rect x="60" y="250" width="640" height="80" fill="#ffffff" stroke="#e0e0e0" rx="6"/>
  
  <!-- 시작 시간 -->
  <text x="80" y="275" font-family="Arial" font-size="12" font-weight="bold" fill="#1976D2">🕘 시작 시간:</text>
  <rect x="180" y="260" width="80" height="25" fill="#e3f2fd" stroke="#2196F3" stroke-width="2" rx="6"/>
  <text x="220" y="277" font-family="Arial" font-size="12" text-anchor="middle" font-weight="bold">09:00</text>
  
  <!-- 종료 시간 -->
  <text x="300" y="275" font-family="Arial" font-size="12" font-weight="bold" fill="#D32F2F">🕕 종료 시간:</text>
  <rect x="400" y="260" width="80" height="25" fill="#ffebee" stroke="#f44336" stroke-width="2" rx="6"/>
  <text x="440" y="277" font-family="Arial" font-size="12" text-anchor="middle" font-weight="bold">15:30</text>
  
  <!-- 빠른 설정 버튼들 -->
  <text x="80" y="310" font-family="Arial" font-size="11" font-weight="bold">⚡ 빠른 설정:</text>
  
  <rect x="180" y="295" width="70" height="25" fill="#E1F5FE" stroke="#0288D1" rx="4"/>
  <text x="215" y="311" font-family="Arial" font-size="10" text-anchor="middle" font-weight="bold">전체 시간</text>
  
  <rect x="260" y="295" width="70" height="25" fill="#E1F5FE" stroke="#0288D1" rx="4"/>
  <text x="295" y="311" font-family="Arial" font-size="10" text-anchor="middle" font-weight="bold">오전만</text>
  
  <rect x="340" y="295" width="70" height="25" fill="#E1F5FE" stroke="#0288D1" rx="4"/>
  <text x="375" y="311" font-family="Arial" font-size="10" text-anchor="middle" font-weight="bold">오후만</text>
  
  <rect x="420" y="295" width="70" height="25" fill="#E1F5FE" stroke="#0288D1" rx="4"/>
  <text x="455" y="311" font-family="Arial" font-size="10" text-anchor="middle" font-weight="bold">점심 제외</text>
  
  <!-- 전체 적용 버튼 -->
  <rect x="250" y="340" width="200" height="35" fill="#4CAF50" rx="6"/>
  <text x="350" y="363" fill="white" font-family="Arial" font-size="14" text-anchor="middle" font-weight="bold">🔄 모든 조건식에 적용</text>
  
  <!-- 하단 버튼들 -->
  <rect x="50" y="510" width="100" height="30" fill="#9C27B0" rx="6"/>
  <text x="100" y="530" fill="white" font-family="Arial" font-size="11" text-anchor="middle" font-weight="bold">👁️ 미리보기</text>
  
  <rect x="160" y="510" width="80" height="30" fill="#795548" rx="6"/>
  <text x="200" y="530" fill="white" font-family="Arial" font-size="11" text-anchor="middle" font-weight="bold">🔄 초기화</text>
  
  <!-- 확인/취소 버튼 -->
  <rect x="580" y="510" width="80" height="30" fill="#4CAF50" rx="6"/>
  <text x="620" y="530" fill="white" font-family="Arial" font-size="11" text-anchor="middle" font-weight="bold">확인</text>
  
  <rect x="670" y="510" width="80" height="30" fill="#f44336" rx="6"/>
  <text x="710" y="530" fill="white" font-family="Arial" font-size="11" text-anchor="middle" font-weight="bold">취소</text>
</svg>

---

## 📱 계좌 정보 탭

<svg width="1000" height="300" xmlns="http://www.w3.org/2000/svg">
  <!-- 계좌 정보 테이블 -->
  <rect x="10" y="10" width="980" height="280" fill="#ffffff" stroke="#2196F3" stroke-width="2" rx="8"/>
  <text x="20" y="35" font-family="Arial" font-size="16" font-weight="bold" fill="#2196F3">💼 계좌 보유 현황</text>
  
  <!-- 테이블 헤더 -->
  <rect x="20" y="50" width="960" height="30" fill="#e3f2fd" stroke="#2196F3"/>
  <text x="30" y="70" font-family="Arial" font-size="12" font-weight="bold">종목명</text>
  <text x="150" y="70" font-family="Arial" font-size="12" font-weight="bold">현재가</text>
  <text x="250" y="70" font-family="Arial" font-size="12" font-weight="bold">매입가</text>
  <text x="350" y="70" font-family="Arial" font-size="12" font-weight="bold">보유수량</text>
  <text x="450" y="70" font-family="Arial" font-size="12" font-weight="bold">매매가능수량</text>
  <text x="580" y="70" font-family="Arial" font-size="12" font-weight="bold">수익률(%)</text>
  <text x="700" y="70" font-family="Arial" font-size="12" font-weight="bold">평가손익</text>
  <text x="820" y="70" font-family="Arial" font-size="12" font-weight="bold">평가금액</text>
  
  <!-- 데이터 행들 -->
  <rect x="20" y="80" width="960" height="25" fill="#ffffff" stroke="#e0e0e0"/>
  <text x="30" y="98" font-family="Arial" font-size="11">삼성전자</text>
  <text x="150" y="98" font-family="Arial" font-size="11">82,500</text>
  <text x="250" y="98" font-family="Arial" font-size="11">80,000</text>
  <text x="360" y="98" font-family="Arial" font-size="11">100</text>
  <text x="470" y="98" font-family="Arial" font-size="11">100</text>
  <text x="590" y="98" font-family="Arial" font-size="11" fill="#f44336">+3.12</text>
  <text x="710" y="98" font-family="Arial" font-size="11" fill="#f44336">+250,000</text>
  <text x="830" y="98" font-family="Arial" font-size="11">8,250,000</text>
  
  <rect x="20" y="105" width="960" height="25" fill="#f9f9f9" stroke="#e0e0e0"/>
  <text x="30" y="123" font-family="Arial" font-size="11">SK하이닉스</text>
  <text x="150" y="123" font-family="Arial" font-size="11">125,000</text>
  <text x="250" y="123" font-family="Arial" font-size="11">128,000</text>
  <text x="360" y="123" font-family="Arial" font-size="11">50</text>
  <text x="470" y="123" font-family="Arial" font-size="11">50</text>
  <text x="590" y="123" font-family="Arial" font-size="11" fill="#2196F3">-2.34</text>
  <text x="710" y="123" font-family="Arial" font-size="11" fill="#2196F3">-150,000</text>
  <text x="830" y="123" font-family="Arial" font-size="11">6,250,000</text>
  
  <rect x="20" y="130" width="960" height="25" fill="#ffffff" stroke="#e0e0e0"/>
  <text x="30" y="148" font-family="Arial" font-size="11">NAVER</text>
  <text x="150" y="148" font-family="Arial" font-size="11">215,000</text>
  <text x="250" y="148" font-family="Arial" font-size="11">210,000</text>
  <text x="360" y="148" font-family="Arial" font-size="11">30</text>
  <text x="470" y="148" font-family="Arial" font-size="11">30</text>
  <text x="590" y="148" font-family="Arial" font-size="11" fill="#f44336">+2.38</text>
  <text x="710" y="148" font-family="Arial" font-size="11" fill="#f44336">+150,000</text>
  <text x="830" y="148" font-family="Arial" font-size="11">6,450,000</text>
  
  <!-- 계좌 요약 정보 -->
  <rect x="20" y="170" width="960" height="60" fill="#f0f8ff" stroke="#2196F3" rx="6"/>
  <text x="30" y="190" font-family="Arial" font-size="12" font-weight="bold" fill="#2196F3">📊 계좌 요약</text>
  
  <text x="30" y="210" font-family="Arial" font-size="11">총매입금액: 20,800,000원</text>
  <text x="200" y="210" font-family="Arial" font-size="11">총평가금액: 20,950,000원</text>
  <text x="370" y="210" font-family="Arial" font-size="11" fill="#f44336">총평가손익: +250,000원</text>
  <text x="550" y="210" font-family="Arial" font-size="11" fill="#f44336">총수익률: +1.20%</text>
  <text x="700" y="210" font-family="Arial" font-size="11">추정예탁자산: 25,500,000원</text>
</svg>

---

## 📋 로그 탭

<svg width="1000" height="400" xmlns="http://www.w3.org/2000/svg">
  <!-- 로그 영역 -->
  <rect x="10" y="10" width="980" height="350" fill="#ffffff" stroke="#666666" stroke-width="2" rx="8"/>
  <text x="20" y="35" font-family="Arial" font-size="16" font-weight="bold" fill="#666">📄 시스템 로그</text>
  
  <!-- 로그 출력 영역 -->
  <rect x="20" y="50" width="960" height="280" fill="#000000" rx="6"/>
  
  <!-- 로그 텍스트들 -->
  <text x="30" y="75" font-family="Consolas" font-size="10" fill="#00ff00">[15:20:30] 자동매매 시작 - 매수조건 3개, 매도: 자동매도만</text>
  <text x="30" y="95" font-family="Consolas" font-size="10" fill="#ffffff">[15:20:35] 매수 신호: 005930 (조건식: 상승추세 조건식)</text>
  <text x="30" y="115" font-family="Consolas" font-size="10" fill="#ffffff">[15:20:40] 매수 주문: 005930 100주 시장가 (진입: 상승추세 조건식)</text>
  <text x="30" y="135" font-family="Consolas" font-size="10" fill="#00ffff">[15:20:45] 주문 접수: 005930 매수</text>
  <text x="30" y="155" font-family="Consolas" font-size="10" fill="#00ffff">[15:20:50] 주문 체결: 005930 매수</text>
  <text x="30" y="175" font-family="Consolas" font-size="10" fill="#ffff00">[15:25:10] 트레일링 스탑 발동: 005930 수익률 2.12%</text>
  <text x="30" y="195" font-family="Consolas" font-size="10" fill="#ff6600">[15:30:25] 매도 주문: 000660 50주 시장가 - 스탑로스 (-2.34%)</text>
  <text x="30" y="215" font-family="Consolas" font-size="10" fill="#ffffff">[15:30:30] 주문 접수: 000660 매도</text>
  <text x="30" y="235" font-family="Consolas" font-size="10" fill="#00ffff">[15:30:35] 주문 체결: 000660 매도</text>
  <text x="30" y="255" font-family="Consolas" font-size="10" fill="#ffffff">[15:35:10] 실시간 트래킹 업데이트: 3개 종목 모니터링 중</text>
  <text x="30" y="275" font-family="Consolas" font-size="10" fill="#ffffff">[15:40:15] 계좌 정보 업데이트 완료</text>
  <text x="30" y="295" font-family="Consolas" font-size="10" fill="#00ff00">[15:45:20] 시스템 정상 운영 중...</text>
  
  <!-- 스크롤바 표시 -->
  <rect x="970" y="50" width="10" height="280" fill="#e0e0e0" rx="5"/>
  <rect x="971" y="200" width="8" height="50" fill="#888888" rx="4"/>
  
  <!-- 하단 컨트롤 버튼들 -->
  <rect x="20" y="350" width="100" height="30" fill="#795548" rx="6"/>
  <text x="70" y="370" fill="white" font-family="Arial" font-size="11" text-anchor="middle" font-weight="bold">로그 지우기</text>
  
  <rect x="130" y="350" width="100" height="30" fill="#2196F3" rx="6"/>
  <text x="180" y="370" fill="white" font-family="Arial" font-size="11" text-anchor="middle" font-weight="bold">로그 저장</text>
  
  <text x="850" y="370" font-family="Arial" font-size="10" fill="#666">실시간 업데이트 중...</text>
</svg>

---

## 🎨 UI 컬러 팔레트

<svg width="800" height="200" xmlns="http://www.w3.org/2000/svg">
  <!-- 색상 팔레트 제목 -->
  <text x="20" y="25" font-family="Arial" font-size="16" font-weight="bold">🎨 UI 색상 체계</text>
  
  <!-- 성공/안전 색상 -->
  <rect x="20" y="40" width="60" height="30" fill="#4CAF50" rx="4"/>
  <text x="50" y="60" fill="white" font-family="Arial" font-size="10" text-anchor="middle" font-weight="bold">SUCCESS</text>
  <text x="50" y="80" font-family="Arial" font-size="8" text-anchor="middle">#4CAF50</text>
  <text x="50" y="90" font-family="Arial" font-size="8" text-anchor="middle">매수/성공</text>
  
  <!-- 위험/경고 색상 -->
  <rect x="100" y="40" width="60" height="30" fill="#f44336" rx="4"/>
  <text x="130" y="60" fill="white" font-family="Arial" font-size="10" text-anchor="middle" font-weight="bold">DANGER</text>
  <text x="130" y="80" font-family="Arial" font-size="8" text-anchor="middle">#f44336</text>
  <text x="130" y="90" font-family="Arial" font-size="8" text-anchor="middle">매도/위험</text>
  
  <!-- 정보/선택 색상 -->
  <rect x="180" y="40" width="60" height="30" fill="#2196F3" rx="4"/>
  <text x="210" y="60" fill="white" font-family="Arial" font-size="10" text-anchor="middle" font-weight="bold">INFO</text>
  <text x="210" y="80" font-family="Arial" font-size="8" text-anchor="middle">#2196F3</text>
  <text x="210" y="90" font-family="Arial" font-size="8" text-anchor="middle">정보/선택</text>
  
  <!-- 경고 색상 -->
  <rect x="260" y="40" width="60" height="30" fill="#FF9800" rx="4"/>
  <text x="290" y="60" fill="white" font-family="Arial" font-size="10" text-anchor="middle" font-weight="bold">WARNING</text>
  <text x="290" y="80" font-family="Arial" font-size="8" text-anchor="middle">#FF9800</text>
  <text x="290" y="90" font-family="Arial" font-size="8" text-anchor="middle">경고/주의</text>
  
  <!-- 보조 색상 -->
  <rect x="340" y="40" width="60" height="30" fill="#9C27B0" rx="4"/>
  <text x="370" y="60" fill="white" font-family="Arial" font-size="10" text-anchor="middle" font-weight="bold">ACCENT</text>
  <text x="370" y="80" font-family="Arial" font-size="8" text-anchor="middle">#9C27B0</text>
  <text x="370" y="90" font-family="Arial" font-size="8" text-anchor="middle">액센트</text>
  
  <!-- 배경 색상들 -->
  <text x="20" y="120" font-family="Arial" font-size="14" font-weight="bold">배경 색상</text>
  
  <rect x="20" y="130" width="50" height="25" fill="#f5f5f5" stroke="#ccc" rx="3"/>
  <text x="45" y="147" font-family="Arial" font-size="8" text-anchor="middle">#f5f5f5</text>
  <text x="45" y="158" font-family="Arial" font-size="7" text-anchor="middle">메인 배경</text>
  
  <rect x="80" y="130" width="50" height="25" fill="#ffffff" stroke="#ccc" rx="3"/>
  <text x="105" y="147" font-family="Arial" font-size="8" text-anchor="middle">#ffffff</text>
  <text x="105" y="158" font-family="Arial" font-size="7" text-anchor="middle">카드 배경</text>
  
  <rect x="140" y="130" width="50" height="25" fill="#f0f8ff" stroke="#ccc" rx="3"/>
  <text x="165" y="147" font-family="Arial" font-size="8" text-anchor="middle">#f0f8ff</text>
  <text x="165" y="158" font-family="Arial" font-size="7" text-anchor="middle">정보 배경</text>
  
  <rect x="200" y="130" width="50" height="25" fill="#f8fff8" stroke="#ccc" rx="3"/>
  <text x="225" y="147" font-family="Arial" font-size="8" text-anchor="middle">#f8fff8</text>
  <text x="225" y="158" font-family="Arial" font-size="7" text-anchor="middle">성공 배경</text>
  
  <rect x="260" y="130" width="50" height="25" fill="#fff8f8" stroke="#ccc" rx="3"/>
  <text x="285" y="147" font-family="Arial" font-size="8" text-anchor="middle">#fff8f8</text>
  <text x="285" y="158" font-family="Arial" font-size="7" text-anchor="middle">경고 배경</text>
</svg>

---

## 📐 UI 구조 요약

이 키움증권 자동매매 시스템은 다음과 같은 특징을 가진 PyQt5 기반의 데스크톱 애플리케이션입니다:

### 🏗️ 구조적 특징
- **4탭 구조**: 자동매매, 계좌정보, 설정, 로그
- **모듈형 위젯**: FlexibleSellConditionWidget, EasyTimeSettingDialog 등
- **실시간 상태 표시**: 하단 상태바로 시스템 상태 모니터링

### 🎨 디자인 특징  
- **모던한 스타일**: 둥근 모서리, 그라데이션, 그림자 효과
- **직관적 아이콘**: 이모지 활용으로 시각적 인식성 향상
- **색상 코딩**: 기능별/상태별 일관된 색상 체계
- **반응형 요소**: 호버 효과, 상태 변화 애니메이션

### 🔧 기능적 특징
- **유연한 매도 설정**: 자동매도 vs 조건식+자동매도 선택
- **시간 관리**: 조건식별 세밀한 시간 설정 가능
- **실시간 모니터링**: 테이블을 통한 실시간 데이터 표시
- **상태 추적**: 각 단계별 상세한 로그 및 상태 표시

이 UI는 복잡한 금융 자동매매 시스템을 사용자가 직관적이고 안전하게 조작할 수 있도록 설계되었습니다.