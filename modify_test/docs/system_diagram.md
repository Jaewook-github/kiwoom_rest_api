# 키움증권 자동매매 시스템 아키텍처 및 다이어그램

## 1. 전체 시스템 아키텍처

```mermaid
graph TB
    subgraph "메인 프로세스"
        GUI[GUI Application<br/>example8-1.py]
        MainUI[PyQt5 Main Window]
        Timer[QTimer 관리자]
        Settings[QSettings 관리]
    end
    
    subgraph "백그라운드 프로세스"
        TRGeneral[일반 TR 프로세스<br/>tr_general_req_func]
        TROrder[주문 TR 프로세스<br/>tr_order_req_func]
        WebSocket[WebSocket 프로세스<br/>run_websocket]
    end
    
    subgraph "데이터 통신"
        Q1[tr_req_queue]
        Q2[tr_result_queue]
        Q3[order_tr_req_queue]
        Q4[websocket_req_queue]
        Q5[websocket_result_queue]
    end
    
    subgraph "외부 시스템"
        KAPI[키움증권 REST API]
        KWS[키움증권 WebSocket]
    end
    
    GUI --> Q1
    GUI --> Q3
    GUI --> Q4
    Q2 --> GUI
    Q5 --> GUI
    
    Q1 --> TRGeneral
    TRGeneral --> Q2
    Q3 --> TROrder
    Q4 --> WebSocket
    WebSocket --> Q5
    
    TRGeneral --> KAPI
    TROrder --> KAPI
    WebSocket --> KWS
```

## 2. 클래스 구조 다이어그램

```mermaid
classDiagram
    class KiwoomAPI {
        +QMainWindow
        +설정값들
        +DataFrame들
        +Queue들
        +Timer들
        +auto_trade_on()
        +auto_trade_off()
        +save_settings()
        +load_settings()
        +receive_tr_result()
        +receive_websocket_result()
        +on_receive_account_info()
        +sell_order()
        +register_realtime_info()
    }
    
    class PandasModel {
        +QAbstractTableModel
        +_data: DataFrame
        +rowCount()
        +columnCount()
        +data()
        +headerData()
    }
    
    class KiwoomTR {
        +token: str
        +login()
        +fn_ka10007(시세표성정보요청)
        +fn_ka10086(일별주가요청)
        +fn_kt00018(계좌평가잔고내역요청)
        +fn_kt10000(주식 매수주문)
        +fn_kt10001(주식 매도주문)
        +fn_kt10002(주식 정정주문)
        +reqeust_all_account_info()
    }
    
    class WebSocketClient {
        +uri: str
        +websocket
        +token: str
        +Queue들
        +connect()
        +send_message()
        +receive_messages()
        +register_realtime_group()
        +register_condition_realtime_result()
    }
    
    KiwoomAPI --> PandasModel : uses
    KiwoomAPI --> KiwoomTR : communicates via Queue
    KiwoomAPI --> WebSocketClient : communicates via Queue
```

## 3. 데이터 흐름 다이어그램

```mermaid
sequenceDiagram
    participant User
    participant GUI
    participant TRProc as TR Process
    participant OrderProc as Order Process
    participant WSProc as WebSocket Process
    participant API as Kiwoom API
    
    User->>GUI: 자동매매 ON
    GUI->>WSProc: 조건검색 실시간 등록
    WSProc->>API: WebSocket 연결
    
    API-->>WSProc: 조건 편입 신호
    WSProc-->>GUI: 편입 종목 정보
    GUI->>TRProc: 종목 기본정보 요청
    TRProc->>API: REST API 호출
    API-->>TRProc: 종목 정보 응답
    TRProc-->>GUI: 종목 정보 전달
    
    GUI->>OrderProc: 매수 주문 요청
    OrderProc->>API: 매수 주문 실행
    API-->>WSProc: 주문 체결 정보
    WSProc-->>GUI: 체결 결과 전달
    
    loop 실시간 모니터링
        API-->>WSProc: 실시간 시세
        WSProc-->>GUI: 시세 업데이트
        GUI->>GUI: 매도 조건 확인
        alt 매도 조건 충족
            GUI->>OrderProc: 매도 주문 요청
            OrderProc->>API: 매도 주문 실행
        end
    end
```

## 4. 프로세스 간 통신 구조

```mermaid
graph LR
    subgraph "Queue 기반 통신"
        GUI[GUI Process]
        
        GUI -.->|tr_req_queue| TRGen[TR General Process]
        TRGen -.->|tr_result_queue| GUI
        
        GUI -.->|order_tr_req_queue| TROrder[TR Order Process]
        
        GUI -.->|websocket_req_queue| WS[WebSocket Process]
        WS -.->|websocket_result_queue| GUI
    end
    
    style GUI fill:#e1f5fe
    style TRGen fill:#f3e5f5
    style TROrder fill:#fff3e0
    style WS fill:#e8f5e8
```

## 5. 주요 함수별 기능 맵

### 5.1 GUI 메인 클래스 (KiwoomAPI)

```mermaid
mindmap
  root((KiwoomAPI))
    초기화
      setupUi()
      load_settings()
      Timer 설정
      Queue 연결
    자동매매 제어
      auto_trade_on()
      auto_trade_off()
      check_valid_time()
    데이터 처리
      receive_tr_result()
      receive_websocket_result()
      on_receive_account_info()
      on_receive_realtime_tick()
    주문 관리
      sell_order()
      check_amend_orders()
      on_receive_order_result()
    UI 관리
      update_pandas_models()
      save_settings()
      format_number()
```

### 5.2 TR 처리 함수들

```mermaid
flowchart TD
    A[TR 요청 수신] --> B{요청 타입 확인}
    
    B -->|계좌조회| C[fn_kt00018]
    B -->|주식기본정보| D[fn_ka10007]
    B -->|매수주문| E[fn_kt10000]
    B -->|매도주문| F[fn_kt10001]
    B -->|정정주문| G[fn_kt10002]
    
    C --> H[계좌 정보 반환]
    D --> I[종목 정보 반환]
    E --> J[주문번호 반환]
    F --> J
    G --> J
    
    H --> K[결과 Queue 전송]
    I --> K
    J --> K
```

### 5.3 WebSocket 처리 구조

```mermaid
graph TB
    WS[WebSocket 연결] --> LOGIN[로그인]
    LOGIN --> REG[실시간 등록]
    
    REG --> LISTEN[메시지 수신 대기]
    
    LISTEN --> REAL{메시지 타입}
    REAL -->|주식체결| TICK[실시간 시세 처리]
    REAL -->|주문체결| ORDER[주문 체결 처리]
    REAL -->|조건검색| COND[조건 편입/편출 처리]
    REAL -->|PING| PING[Ping 응답]
    
    TICK --> QUEUE[결과 Queue 전송]
    ORDER --> QUEUE
    COND --> QUEUE
    PING --> LISTEN
    
    QUEUE --> LISTEN
```

## 6. 데이터 모델 구조

### 6.1 주요 DataFrame 구조

```mermaid
erDiagram
    ACCOUNT_INFO {
        string 종목코드 PK
        string 종목명
        float 현재가
        float 매입가
        int 보유수량
        int 매매가능수량
        float 수익률
    }
    
    REALTIME_TRACKING {
        string 종목코드 PK
        string 종목명
        float 현재가
        float 매입가
        float 수익률
        bool 트레일링발동여부
        float 트레일링발동후고가
        bool 매수주문여부
        bool 매도주문여부
    }
    
    ORDER_INFO {
        string 주문번호 PK
        string 주문접수시간
        string 종목코드
        int 주문수량
        string 매수매도구분
    }
    
    CONDITION_LIST {
        string 조건index PK
        string 조건명
    }
    
    ACCOUNT_INFO ||--o{ REALTIME_TRACKING : "매매대상종목"
    REALTIME_TRACKING ||--o{ ORDER_INFO : "주문내역"
```

## 7. API 통신 구조

### 7.1 REST API 통신

```mermaid
sequenceDiagram
    participant App
    participant KiwoomTR
    participant API as Kiwoom REST API
    
    App->>KiwoomTR: API 요청
    KiwoomTR->>KiwoomTR: 요청 제한 확인
    KiwoomTR->>API: HTTP POST
    Note over KiwoomTR,API: Authorization: Bearer {token}
    API-->>KiwoomTR: JSON 응답
    KiwoomTR->>KiwoomTR: 응답 데이터 파싱
    KiwoomTR-->>App: 처리된 데이터
```

### 7.2 WebSocket 통신

```mermaid
sequenceDiagram
    participant App
    participant WSClient
    participant WS as Kiwoom WebSocket
    
    App->>WSClient: 실시간 등록 요청
    WSClient->>WS: {"trnm": "REG", ...}
    WS-->>WSClient: 등록 완료 응답
    
    loop 실시간 데이터
        WS-->>WSClient: {"trnm": "REAL", ...}
        WSClient->>WSClient: 데이터 파싱
        WSClient-->>App: 처리된 실시간 데이터
    end
```

## 8. 타이머 기반 작업 스케줄링

```mermaid
gantt
    title 타이머 기반 작업 스케줄링
    dateFormat X
    axisFormat %L ms
    
    section 실시간 처리
    WebSocket 결과 수신     :0, 10
    
    section 일반 처리
    TR 결과 수신           :0, 100
    미체결 주문 확인        :0, 1000
    화면 업데이트          :0, 1000
    거래시간 확인          :0, 1000
    
    section 데이터 저장
    Pickle 파일 저장       :0, 5000
```

이 아키텍처는 멀티프로세싱을 통한 안정성과 실시간 처리 성능을 동시에 확보하면서, 체계적인 데이터 관리와 사용자 친화적인 인터페이스를 제공하도록 설계되었습니다.