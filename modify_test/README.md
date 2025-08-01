# 키움 REST API 실전 예제 코드
## 조건식 기반 매수/매도 + 스탑로스 + 트레일링 스탑 간단히 구현
### PyQt5 + QtDesigner / python - multiprocessing
    - Point1: 실시간 등록 최대 100개 -> 주문 체결 + 조건식 2개 -> 실시간 97개 종목 최대 등록 가능
    - Point2: Websocket 실시간 등록 / 해제 관리 (그룹번호 관리, 초당 등록/해제 요청 수 관리)
    - Point3: TR 요청은 최소한으로 진행 (일반 TR 요청은 1초당 1건으로 안전하게)
    - Point4: 일반 TR 요청과 주문 TR 요청 분리해서 진행 (주문도 1초당 1건으로 안전하게)
    - Point5: 실시간 체결/미체결 주문 관리

### 자동매매 시나리오
1. 매수 조건식 검출 -> 입력한 금액 만큼 매수 주문 (지정가, 시장가 선택 가능)
   - 입력한 금액보다 현재가가 커서 주문수량이 0으로 나오는 경우 해당 종목은 매매X
2. 자동 매수 된 종목들 중 아래 조건 만족하면 전량 매도 주문 (지정가, 시장가 선택 가능)
   - 매도 조건식 검출
   - 현재 수익률(%)이 입력된 스탑로스 수익률(%)보다 낮을 경우
   - 트레일링 스탑 발동 이후 트래킹된 고가 대비 현재가의 하락률(%)이 입력된 하락률(%)보다 낮을 경우
     - 현재 수익률(%)이 입력된 트레일링 스탑 발동 수익률(%)보다 큰 경우 트레일링 스탑 발동
3. 지정가 주문이 미체결 될 경우 입력된 시간(초 단위) 만큼 대기 후 시장가 정정 주문
