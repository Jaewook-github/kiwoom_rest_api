```svg
<svg viewBox="0 0 1400 900" xmlns="http://www.w3.org/2000/svg">
  <!-- 배경 -->
  <rect width="1400" height="900" fill="#fafafa" stroke="#e0e0e0" stroke-width="1"/>
  
  <!-- 타이틀 바 -->
  <rect x="0" y="0" width="1400" height="40" fill="linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)"/>
  <text x="15" y="26" font-family="Arial" font-size="16" fill="white" font-weight="bold">키움증권 자동매매 프로그램 v2.0</text>
  
  <!-- 상태 표시 -->
  <circle cx="1340" cy="20" r="8" fill="#4caf50"/>
  <text x="1310" y="25" font-family="Arial" font-size="10" fill="white">운영중</text>
  
  <!-- 메인 탭 컨테이너 -->
  <g id="main-tabs">
    <!-- 탭 헤더 -->
    <rect x="0" y="40" width="1400" height="45" fill="#f5f5f5" stroke="#e0e0e0" stroke-width="1"/>
    
    <!-- 제어판 탭 (활성) -->
    <rect x="10" y="45" width="120" height="35" fill="white" stroke="#2196f3" stroke-width="2" rx="5"/>
    <text x="45" y="65" font-family="Arial" font-size="12" font-weight="bold" fill="#2196f3">⚙️ 제어판</text>
    
    <!-- 매수설정 탭 -->
    <rect x="140" y="45" width="120" height="35" fill="#f8f9fa" stroke="#ddd" stroke-width="1" rx="5"/>
    <text x="170" y="65" font-family="Arial" font-size="12" fill="#666">💰 매수설정</text>
    
    <!-- 매도설정 탭 -->
    <rect x="270" y="45" width="120" height="35" fill="#f8f9fa" stroke="#ddd" stroke-width="1" rx="5"/>
    <text x="300" y="65" font-family="Arial" font-size="12" fill="#666">📈 매도설정</text>
    
    <!-- 계좌현황 탭 -->
    <rect x="400" y="45" width="120" height="35" fill="#f8f9fa" stroke="#ddd" stroke-width="1" rx="5"/>
    <text x="430" y="65" font-family="Arial" font-size="12" fill="#666">💼 계좌현황</text>
    
    <!-- 매매현황 탭 -->
    <rect x="530" y="45" width="120" height="35" fill="#f8f9fa" stroke="#ddd" stroke-width="1" rx="5"/>
    <text x="560" y="65" font-family="Arial" font-size="12" fill="#666">📊 매매현황</text>
    
    <!-- 매도기록 탭 -->
    <rect x="660" y="45" width="120" height="35" fill="#f8f9fa" stroke="#ddd" stroke-width="1" rx="5"/>
    <text x="690" y="65" font-family="Arial" font-size="12" fill="#666">📋 매도기록</text>
    
    <!-- 로그/알림 탭 -->
    <rect x="790" y="45" width="120" height="35" fill="#f8f9fa" stroke="#ddd" stroke-width="1" rx="5"/>
    <text x="820" y="65" font-family="Arial" font-size="12" fill="#666">📝 로그/알림</text>
  </g>
  
  <!-- 제어판 탭 내용 -->
  <g id="control-tab-content">
    <!-- 메인 제어 영역 -->
    <rect x="20" y="100" width="1360" height="780" fill="white" stroke="#e0e0e0" stroke-width="1" rx="8"/>
    
    <!-- 핵심 제어 패널 -->
    <g id="core-controls">
      <rect x="40" y="120" width="1320" height="80" fill="linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%)" stroke="#2196f3" stroke-width="1" rx="8"/>
      <text x="60" y="140" font-family="Arial" font-size="14" font-weight="bold" fill="#1976d2">🚀 핵심 제어</text>
      
      <!-- 자동매매 상태 -->
      <rect x="60" y="150" width="140" height="40" fill="#4caf50" rx="6" filter="drop-shadow(2px 2px 4px rgba(0,0,0,0.2))"/>
      <text x="105" y="173" font-family="Arial" font-size="12" fill="white" font-weight="bold">자동매매 ON</text>
      
      <rect x="220" y="150" width="140" height="40" fill="#f44336" rx="6" opacity="0.7"/>
      <text x="265" y="173" font-family="Arial" font-size="12" fill="white" font-weight="bold">자동매매 OFF</text>
      
      <rect x="380" y="150" width="120" height="40" fill="#ff9800" rx="6"/>
      <text x="420" y="173" font-family="Arial" font-size="12" fill="white" font-weight="bold">설정 저장</text>
      
      <!-- 실시간 상태 -->
      <rect x="520" y="150" width="200" height="40" fill="#2196f3" rx="6"/>
      <text x="570" y="165" font-family="Arial" font-size="10" fill="white">실시간 등록:</text>
      <text x="575" y="180" font-family="Arial" font-size="14" fill="white" font-weight="bold">15/95 종목</text>
      
      <rect x="740" y="150" width="200" height="40" fill="#673ab7" rx="6"/>
      <text x="790" y="165" font-family="Arial" font-size="10" fill="white">자동매매 종목:</text>
      <text x="810" y="180" font-family="Arial" font-size="14" fill="white" font-weight="bold">3/10 종목</text>
    </g>
    
    <!-- 설정 그리드 -->
    <g id="settings-grid">
      <!-- 거래 시간 설정 -->
      <rect x="40" y="220" width="320" height="120" fill="white" stroke="#e0e0e0" stroke-width="1" rx="6"/>
      <rect x="40" y="220" width="320" height="30" fill="#e8f5e9" rx="6 6 0 0"/>
      <text x="55" y="240" font-family="Arial" font-size="12" font-weight="bold" fill="#2e7d32">⏰ 거래 시간</text>
      
      <text x="55" y="265" font-family="Arial" font-size="11">시작 시간:</text>
      <rect x="120" y="255" width="80" height="25" fill="#f5f5f5" stroke="#ddd" rx="3"/>
      <text x="130" y="270" font-family="Arial" font-size="11">09:00:00</text>
      
      <text x="220" y="270" font-family="Arial" font-size="11">~</text>
      
      <text x="55" y="290" font-family="Arial" font-size="11">종료 시간:</text>
      <rect x="120" y="280" width="80" height="25" fill="#f5f5f5" stroke="#ddd" rx="3"/>
      <text x="130" y="295" font-family="Arial" font-size="11">15:30:00</text>
      
      <text x="55" y="320" font-family="Arial" font-size="10" fill="#666">⚠️ 장 마감 30분 전 자동 정리매매</text>
      
      <!-- 주문 관리 설정 -->
      <rect x="380" y="220" width="320" height="120" fill="white" stroke="#e0e0e0" stroke-width="1" rx="6"/>
      <rect x="380" y="220" width="320" height="30" fill="#fff3e0" rx="6 6 0 0"/>
      <text x="395" y="240" font-family="Arial" font-size="12" font-weight="bold" fill="#f57c00">⚡ 주문 관리</text>
      
      <text x="395" y="265" font-family="Arial" font-size="11">미체결 정정:</text>
      <rect x="480" y="255" width="50" height="25" fill="#f5f5f5" stroke="#ddd" rx="3"/>
      <text x="490" y="270" font-family="Arial" font-size="11">60</text>
      <text x="540" y="270" font-family="Arial" font-size="11">초 후</text>
      
      <text x="395" y="290" font-family="Arial" font-size="11">최대 종목:</text>
      <rect x="480" y="280" width="50" height="25" fill="#f5f5f5" stroke="#ddd" rx="3"/>
      <text x="495" y="295" font-family="Arial" font-size="11">10</text>
      <text x="540" y="295" font-family="Arial" font-size="11">종목</text>
      
      <text x="395" y="320" font-family="Arial" font-size="10" fill="#666">📱 텔레그램 알림: 활성화</text>
      
      <!-- 당일 통계 -->
      <rect x="720" y="220" width="320" height="120" fill="white" stroke="#e0e0e0" stroke-width="1" rx="6"/>
      <rect x="720" y="220" width="320" height="30" fill="#e8eaf6" rx="6 6 0 0"/>
      <text x="735" y="240" font-family="Arial" font-size="12" font-weight="bold" fill="#3f51b5">📊 당일 실적</text>
      
      <text x="735" y="265" font-family="Arial" font-size="11">총 매도:</text>
      <text x="795" y="265" font-family="Arial" font-size="11" font-weight="bold" fill="#4caf50">8건</text>
      <text x="835" y="265" font-family="Arial" font-size="11">승률:</text>
      <text x="875" y="265" font-family="Arial" font-size="11" font-weight="bold" fill="#2196f3">75%</text>
      
      <text x="735" y="290" font-family="Arial" font-size="11">평균수익:</text>
      <text x="810" y="290" font-family="Arial" font-size="11" font-weight="bold" fill="#4caf50">+1.25%</text>
      
      <text x="735" y="315" font-family="Arial" font-size="11">총 수익:</text>
      <text x="785" y="315" font-family="Arial" font-size="11" font-weight="bold" fill="#4caf50">+156,000원</text>
      
      <!-- 알림 설정 -->
      <rect x="1060" y="220" width="300" height="120" fill="white" stroke="#e0e0e0" stroke-width="1" rx="6"/>
      <rect x="1060" y="220" width="300" height="30" fill="#fce4ec" rx="6 6 0 0"/>
      <text x="1075" y="240" font-family="Arial" font-size="12" font-weight="bold" fill="#c2185b">🔔 알림 설정</text>
      
      <text x="1075" y="265" font-family="Arial" font-size="10">☑️ 매수 조건 편입 알림</text>
      <text x="1075" y="280" font-family="Arial" font-size="10">☑️ 매수/매도 체결 알림</text>
      <text x="1075" y="295" font-family="Arial" font-size="10">☑️ 손절/트레일링 발동 알림</text>
      <text x="1075" y="310" font-family="Arial" font-size="10">☑️ 재매수 차단 알림</text>
      <text x="1075" y="325" font-family="Arial" font-size="10">☑️ 일일 실적 요약 알림</text>
    </g>
    
    <!-- 빠른 액션 버튼들 -->
    <g id="quick-actions">
      <rect x="40" y="360" width="1320" height="60" fill="#f8f9fa" stroke="#dee2e6" stroke-width="1" rx="6"/>
      <text x="55" y="380" font-family="Arial" font-size="12" font-weight="bold" fill="#495057">🚀 빠른 액션</text>
      
      <rect x="60" y="390" width="100" height="25" fill="#28a745" rx="4"/>
      <text x="75" y="405" font-family="Arial" font-size="10" fill="white">전체 조건 활성화</text>
      
      <rect x="180" y="390" width="100" height="25" fill="#dc3545" rx="4"/>
      <text x="195" y="405" font-family="Arial" font-size="10" fill="white">전체 조건 비활성화</text>
      
      <rect x="300" y="390" width="100" height="25" fill="#fd7e14" rx="4"/>
      <text x="325" y="405" font-family="Arial" font-size="10" fill="white">전량 매도</text>
      
      <rect x="420" y="390" width="100" height="25" fill="#6f42c1" rx="4"/>
      <text x="445" y="405" font-family="Arial" font-size="10" fill="white">로그 보기</text>
      
      <rect x="540" y="390" width="100" height="25" fill="#20c997" rx="4"/>
      <text x="565" y="405" font-family="Arial" font-size="10" fill="white">백업 생성</text>
      
      <rect x="660" y="390" width="100" height="25" fill="#0dcaf0" rx="4"/>
      <text x="685" y="405" font-family="Arial" font-size="10" fill="white">설정 내보내기</text>
    </g>
    
    <!-- 시스템 상태 -->
    <g id="system-status">
      <rect x="40" y="440" width="1320" height="120" fill="white" stroke="#e0e0e0" stroke-width="1" rx="6"/>
      <rect x="40" y="440" width="1320" height="30" fill="#e1f5fe" rx="6 6 0 0"/>
      <text x="55" y="460" font-family="Arial" font-size="12" font-weight="bold" fill="#0277bd">🖥️ 시스템 상태</text>
      
      <!-- API 연결 상태 -->
      <circle cx="70" cy="485" r="6" fill="#4caf50"/>
      <text x="85" y="490" font-family="Arial" font-size="11">키움 API: 연결됨</text>
      
      <circle cx="200" cy="485" r="6" fill="#4caf50"/>
      <text x="215" y="490" font-family="Arial" font-size="11">웹소켓: 활성</text>
      
      <circle cx="320" cy="485" r="6" fill="#4caf50"/>
      <text x="335" y="490" font-family="Arial" font-size="11">텔레그램: 연결됨</text>
      
      <circle cx="460" cy="485" r="6" fill="#ff9800"/>
      <text x="475" y="490" font-family="Arial" font-size="11">데이터베이스: 동기화중</text>
      
      <!-- 성능 지표 -->
      <text x="70" y="515" font-family="Arial" font-size="11">메모리 사용량:</text>
      <rect x="160" y="505" width="100" height="15" fill="#e0e0e0" rx="3"/>
      <rect x="160" y="505" width="65" height="15" fill="#4caf50" rx="3"/>
      <text x="270" y="515" font-family="Arial" font-size="10">65%</text>
      
      <text x="320" y="515" font-family="Arial" font-size="11">CPU 사용량:</text>
      <rect x="400" y="505" width="100" height="15" fill="#e0e0e0" rx="3"/>
      <rect x="400" y="505" width="25" height="15" fill="#2196f3" rx="3"/>
      <text x="510" y="515" font-family="Arial" font-size="10">25%</text>
      
      <!-- 업타임 -->
      <text x="70" y="540" font-family="Arial" font-size="11">가동 시간: 2시간 34분</text>
      <text x="220" y="540" font-family="Arial" font-size="11">마지막 저장: 방금 전</text>
      <text x="370" y="540" font-family="Arial" font-size="11">버전: v2.0.1</text>
    </g>
    
    <!-- 최근 활동 -->
    <g id="recent-activity">
      <rect x="40" y="580" width="1320" height="290" fill="white" stroke="#e0e0e0" stroke-width="1" rx="6"/>
      <rect x="40" y="580" width="1320" height="30" fill="#f1f8e9" rx="6 6 0 0"/>
      <text x="55" y="600" font-family="Arial" font-size="12" font-weight="bold" fill="#558b2f">📈 최근 활동 로그</text>
      
      <!-- 로그 엔트리들 -->
      <g font-family="monospace" font-size="10">
        <text x="60" y="625" fill="#4caf50">[14:23:45] 💰 매수 조건 편입: 삼성전자(005930) - 돌파조건1</text>
        <text x="60" y="645" fill="#2196f3">[14:23:47] 📋 매수주문 접수: 삼성전자 75,000원 × 2주</text>
        <text x="60" y="665" fill="#4caf50">[14:23:48] ✅ 매수 체결 완료: 삼성전자 75,000원 × 2주</text>
        <text x="60" y="685" fill="#ff9800">[14:25:12] 🔔 트레일링 스탑 발동: SK하이닉스 +2.3%</text>
        <text x="60" y="705" fill="#f44336">[14:28:34] 📉 손절 발동: LG전자 -2.1%</text>
        <text x="60" y="725" fill="#9c27b0">[14:30:15] 🚫 재매수 차단: 현대차(005380) - 당일 매도 종목</text>
        <text x="60" y="745" fill="#4caf50">[14:32:22] 💸 매도 체결 완료: 네이버 +1.8% 수익</text>
        <text x="60" y="765" fill="#607d8b">[14:35:01] 💾 실시간 데이터 저장 완료</text>
        <text x="60" y="785" fill="#795548">[14:37:18] 📱 텔레그램 알림 전송: 일일 실적 요약</text>
        <text x="60" y="805" fill="#3f51b5">[14:40:00] 🔄 조건식 스캔 완료: 활성 5개</text>
        <text x="60" y="825" fill="#009688">[14:42:33] 📊 당일 통계 업데이트: 승률 75%</text>
        <text x="60" y="845" fill="#ff5722">[14:45:00] ⚠️ 장 마감 1시간 전 알림</text>
      </g>
    </g>
  </g>
</svg>
```