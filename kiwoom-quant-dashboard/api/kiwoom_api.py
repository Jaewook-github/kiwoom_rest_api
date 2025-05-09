# api/kiwoom_api.py
import os
import requests
import json
import time
import datetime
import logging
from typing import Dict, List, Any, Optional, Union, Callable
import pandas as pd
import websockets
import asyncio
from dotenv import load_dotenv

# 로깅 설정
logger = logging.getLogger(__name__)

# 환경 변수 로드
load_dotenv()

class KiwoomAPI:
    """키움증권 REST API 클라이언트 클래스
    
    키움증권 Open API+를 통해 시장 데이터 조회, 주문 처리, 계좌 정보 조회 등의 기능을 제공합니다.
    REST API와 웹소켓을 통한 실시간 데이터 구독을 지원합니다.
    """
    
    def __init__(self):
        """API 클라이언트 초기화"""
        self.api_base_url = os.getenv("KIWOOM_API_URL", "https://openapi.kiwoom.com/v1")
        self.api_key = os.getenv("KIWOOM_API_KEY")
        self.api_secret = os.getenv("KIWOOM_API_SECRET")
        self.account_number = os.getenv("KIWOOM_ACCOUNT_NUMBER")
        self.access_token = None
        self.token_expires_at = 0
        self.ws_url = os.getenv("KIWOOM_WS_URL", "wss://openapi.kiwoom.com/ws/v1")
        self.ws_connection = None
        self.realtime_subscriptions = {}
        self.realtime_callbacks = {}
        self.is_connected = False
        
    def _get_headers(self) -> Dict:
        """API 요청 헤더 생성
        
        Returns:
            Dict: 인증 정보가 포함된 헤더
        """
        if self.access_token is None or time.time() > self.token_expires_at:
            self._refresh_token()
            
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def _refresh_token(self) -> None:
        """API 토큰 갱신"""
        auth_url = f"{self.api_base_url}/oauth2/token"
        payload = {
            "grant_type": "client_credentials",
            "appkey": self.api_key,
            "appsecret": self.api_secret
        }
        
        try:
            response = requests.post(auth_url, data=payload)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            # 만료 시간은 현재 시간 + 토큰 유효 시간(초) - 60초(안전 마진)
            self.token_expires_at = time.time() + token_data.get("expires_in", 0) - 60
            
        except requests.exceptions.RequestException as e:
            print(f"토큰 갱신 중 오류 발생: {e}")
            raise
    
    def request(self, method: str, endpoint: str, params: Optional[Dict] = None, 
                data: Optional[Dict] = None) -> Dict:
        """API 요청 수행
        
        Args:
            method: HTTP 메소드 ('GET', 'POST', 'PUT', 'DELETE')
            endpoint: API 엔드포인트 경로
            params: URL 쿼리 파라미터
            data: 요청 본문 데이터
            
        Returns:
            Dict: API 응답 데이터
        """
        url = f"{self.api_base_url}{endpoint}"
        headers = self._get_headers()
        
        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers,
                params=params,
                json=data
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            print(f"API 요청 오류 (HTTP {response.status_code}): {e}")
            print(f"응답 내용: {response.text}")
            raise
            
        except requests.exceptions.RequestException as e:
            print(f"API 요청 중 오류 발생: {e}")
            raise
    
    def get_market_code_list(self, market_type: str = "0") -> Dict:
        """시장별 종목 코드 리스트 조회
        
        Args:
            market_type: 시장 구분 코드 ('0':코스피, '10':코스닥, '3':ELW, '8':ETF, '50':KONEX)
            
        Returns:
            Dict: 종목 코드 리스트
        """
        endpoint = "/market/code_list"
        params = {"market_type": market_type}
        return self.request("GET", endpoint, params=params)
    
    def get_stock_daily_chart(self, code: str, from_date: str, to_date: Optional[str] = None) -> Dict:
        """일별 주가 데이터 조회
        
        Args:
            code: 종목 코드
            from_date: 조회 시작일 (YYYYMMDD)
            to_date: 조회 종료일 (YYYYMMDD, 기본값: 현재 날짜)
            
        Returns:
            Dict: 일별 주가 데이터
        """
        endpoint = "/stock/daily_chart"
        params = {
            "code": code,
            "from_date": from_date
        }
        if to_date:
            params["to_date"] = to_date
            
        return self.request("GET", endpoint, params=params)
    
    def get_current_price(self, codes: Union[str, List[str]]) -> Dict:
        """현재가 조회
        
        Args:
            codes: 종목 코드 또는 종목 코드 리스트
            
        Returns:
            Dict: 현재가 데이터
        """
        endpoint = "/stock/current_price"
        
        if isinstance(codes, list):
            codes_str = ",".join(codes)
        else:
            codes_str = codes
            
        params = {"codes": codes_str}
        return self.request("GET", endpoint, params=params)
    
    def get_financial_statement(self, code: str, year: Optional[str] = None, quarter: Optional[str] = None) -> Dict:
        """재무제표 조회
        
        Args:
            code: 종목 코드
            year: 조회 연도 (YYYY)
            quarter: 조회 분기 ('1', '2', '3', '4')
            
        Returns:
            Dict: 재무제표 데이터
        """
        endpoint = "/stock/financial_statement"
        params = {"code": code}
        
        if year:
            params["year"] = year
        if quarter:
            params["quarter"] = quarter
            
        return self.request("GET", endpoint, params=params)
    
    def get_account_balance(self) -> Dict:
        """계좌 잔고 조회
        
        Returns:
            Dict: 계좌 잔고 정보
        """
        endpoint = "/account/balance"
        return self.request("GET", endpoint)
    
    def get_order_history(self, from_date: str, to_date: Optional[str] = None) -> Dict:
        """주문 내역 조회
        
        Args:
            from_date: 조회 시작일 (YYYYMMDD)
            to_date: 조회 종료일 (YYYYMMDD, 기본값: 현재 날짜)
            
        Returns:
            Dict: 주문 내역
        """
        endpoint = "/account/order_history"
        params = {"from_date": from_date}
        
        if to_date:
            params["to_date"] = to_date
            
        return self.request("GET", endpoint, params=params)
    
    def place_order(self, code: str, order_type: str, quantity: int, price: Optional[int] = None, 
                   order_condition: str = "0", account_number: Optional[str] = None) -> Dict:
        """주식 주문
        
        Args:
            code: 종목 코드
            order_type: 주문 구분 ('1':매도, '2':매수)
            quantity: 주문 수량
            price: 주문 가격 (지정가 주문일 경우)
            order_condition: 주문 조건 ('0':일반, '1':IOC, '2':FOK)
            account_number: 계좌번호 (기본값: 환경 변수에 설정된 계좌)
            
        Returns:
            Dict: 주문 결과
        """
        endpoint = "/stock/order"
        data = {
            "code": code,
            "order_type": order_type,
            "quantity": quantity,
            "account_number": account_number or self.account_number,
            "order_condition": order_condition
        }
        
        if price:
            data["price"] = price
            data["price_type"] = "L"  # 지정가
        else:
            data["price_type"] = "M"  # 시장가
            
        return self.request("POST", endpoint, data=data)
    
    def cancel_order(self, order_number: str) -> Dict:
        """주문 취소
        
        Args:
            order_number: 주문 번호
            
        Returns:
            Dict: 주문 취소 결과
        """
        endpoint = "/stock/order/cancel"
        data = {"order_number": order_number}
        return self.request("POST", endpoint, data=data)
    
    def get_account_info(self) -> Dict:
        """계좌 정보 조회
        
        Returns:
            Dict: 계좌 정보
        """
        endpoint = "/account/info"
        return self.request("GET", endpoint)
    
    def subscribe_realtime(self, code: str, callback: Callable) -> None:
        """실시간 시세 구독
        
        Args:
            code: 종목 코드
            callback: 실시간 데이터 수신 콜백 함수
        """
        if not self.is_connected:
            self.connect_websocket()
        
        self.realtime_subscriptions[code] = callback
        self.ws_connection.send(json.dumps({"type": "subscribe", "code": code}))
    
    def unsubscribe_realtime(self, code: str) -> None:
        """실시간 시세 구독 취소
        
        Args:
            code: 종목 코드
        """
        if code in self.realtime_subscriptions:
            del self.realtime_subscriptions[code]
            self.ws_connection.send(json.dumps({"type": "unsubscribe", "code": code}))
    
    async def connect_websocket(self) -> None:
        """웹소켓 연결 수립"""
        if self.ws_connection and self.is_connected:
            logger.info("이미 웹소켓에 연결되어 있습니다.")
            return
        
        try:
            # 토큰 확인 및 갱신
            if self.access_token is None or time.time() > self.token_expires_at:
                self._refresh_token()
                
            self.ws_connection = await websockets.connect(
                f"{self.ws_url}?token={self.access_token}",
                ping_interval=30,
                ping_timeout=10
            )
            self.is_connected = True
            
            # 웹소켓 메시지 수신 루프 시작
            asyncio.create_task(self._websocket_message_loop())
            logger.info("웹소켓 연결 성공")
            
            # 이전 구독 정보 복원
            for key in self.realtime_subscriptions.keys():
                code, data_type = key.split('_')
                await self._send_subscribe_message(code, data_type)
                
        except Exception as e:
            logger.error(f"웹소켓 연결 실패: {e}")
            self.is_connected = False
            self.ws_connection = None
            raise
    
    async def _websocket_message_loop(self) -> None:
        """웹소켓 메시지 수신 루프"""
        if not self.ws_connection:
            return
            
        try:
            while True:
                message = await self.ws_connection.recv()
                data = json.loads(message)
                
                # 메시지 타입에 따른 처리
                msg_type = data.get("type")
                if msg_type == "heartbeat":
                    # 하트비트 응답
                    await self.ws_connection.send(json.dumps({"type": "heartbeat"}))
                elif msg_type == "data":
                    # 실시간 데이터 처리
                    self._process_realtime_data(data)
                elif msg_type == "error":
                    logger.error(f"웹소켓 오류: {data.get('message')}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.warning("웹소켓 연결 종료")
            self.is_connected = False
            self.ws_connection = None
        except Exception as e:
            logger.error(f"웹소켓 메시지 처리 오류: {e}")
            self.is_connected = False
            self.ws_connection = None
    
    def _process_realtime_data(self, data: Dict) -> None:
        """실시간 데이터 처리
        
        Args:
            data: 수신된 실시간 데이터
        """
        if "code" not in data or "data_type" not in data:
            return
            
        code = data["code"]
        data_type = data["data_type"]
        content = data.get("content", {})
        
        # 콜백 함수 호출
        callback_key = f"{code}_{data_type}"
        if callback_key in self.realtime_callbacks:
            try:
                self.realtime_callbacks[callback_key](content)
            except Exception as e:
                logger.error(f"실시간 데이터 콜백 처리 오류: {e}")
    
    async def _send_subscribe_message(self, code: str, data_type: str) -> None:
        """구독 메시지 전송
        
        Args:
            code: 종목 코드
            data_type: 데이터 타입
        """
        if not self.ws_connection or not self.is_connected:
            return
            
        subscribe_message = {
            "type": "subscribe",
            "code": code,
            "data_type": data_type
        }
        await self.ws_connection.send(json.dumps(subscribe_message))
    
    async def subscribe_realtime(self, code: str, data_type: str, callback: Callable[[Dict], None]) -> bool:
        """실시간 데이터 구독
        
        Args:
            code: 종목 코드
            data_type: 데이터 타입 ('price', 'tick', 'orderbook' 등)
            callback: 데이터 수신 시 호출할 콜백 함수
            
        Returns:
            bool: 구독 성공 여부
        """
        if not self.is_connected:
            await self.connect_websocket()
            
        subscription_key = f"{code}_{data_type}"
        
        # 이미 구독 중인 경우 콜백만 업데이트
        if subscription_key in self.realtime_subscriptions:
            self.realtime_callbacks[subscription_key] = callback
            return True
            
        try:
            # 구독 요청
            await self._send_subscribe_message(code, data_type)
            
            # 구독 정보 저장
            self.realtime_subscriptions[subscription_key] = True
            self.realtime_callbacks[subscription_key] = callback
            logger.info(f"실시간 데이터 구독 성공: {code} - {data_type}")
            return True
            
        except Exception as e:
            logger.error(f"실시간 데이터 구독 실패: {e}")
            return False
    
    async def unsubscribe_realtime(self, code: str, data_type: str) -> bool:
        """실시간 데이터 구독 해제
        
        Args:
            code: 종목 코드
            data_type: 데이터 타입
            
        Returns:
            bool: 구독 해제 성공 여부
        """
        if not self.is_connected:
            return False
            
        subscription_key = f"{code}_{data_type}"
        
        # 구독 중이 아닌 경우
        if subscription_key not in self.realtime_subscriptions:
            return True
            
        try:
            # 구독 해제 요청
            unsubscribe_message = {
                "type": "unsubscribe",
                "code": code,
                "data_type": data_type
            }
            await self.ws_connection.send(json.dumps(unsubscribe_message))
            
            # 구독 정보 삭제
            if subscription_key in self.realtime_subscriptions:
                del self.realtime_subscriptions[subscription_key]
            if subscription_key in self.realtime_callbacks:
                del self.realtime_callbacks[subscription_key]
                
            logger.info(f"실시간 데이터 구독 해제 성공: {code} - {data_type}")
            return True
            
        except Exception as e:
            logger.error(f"실시간 데이터 구독 해제 실패: {e}")
            return False
    
    async def close_websocket(self) -> None:
        """웹소켓 연결 종료"""
        if not self.ws_connection:
            return
            
        try:
            await self.ws_connection.close()
            logger.info("웹소켓 연결 종료")
        except Exception as e:
            logger.error(f"웹소켓 연결 종료 오류: {e}")
        finally:
            self.is_connected = False
            self.ws_connection = None
            self.realtime_subscriptions = {}
            self.realtime_callbacks = {}
    
    def search_stock(self, keyword: str) -> Dict:
        """종목 검색
        
        Args:
            keyword: 검색 키워드
            
        Returns:
            Dict: 검색 결과
        """
        endpoint = "/stock/search"
        params = {"keyword": keyword}
        return self.request("GET", endpoint, params=params)