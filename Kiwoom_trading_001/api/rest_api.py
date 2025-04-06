"""
키움증권 REST API 통신 모듈
"""
import asyncio
import json
from typing import Dict, Any, Optional, List, Union
import requests
import datetime

from ..config import config
from ..utils.logger import logger
from ..utils.decorators import async_retry, async_measure_time

class KiwoomRestAPI:
    """키움증권 REST API 클래스"""

    def __init__(self, access_token: str, is_real: bool = True):
        """
        초기화

        Args:
            access_token: 키움증권 접근 토큰
            is_real: 실전투자 여부 (False면 모의투자)
        """
        self.access_token = access_token
        self.is_real = is_real

        # 호스트 설정 (실전/모의)
        api_config = config.get('api')
        if is_real:
            self.host = api_config.get('real_server', {}).get('rest_host', 'https://api.kiwoom.com')
        else:
            self.host = api_config.get('mock_server', {}).get('rest_host', 'https://mockapi.kiwoom.com')

        # API 요청 설정
        self.timeout = api_config.get('request_timeout', 30)
        self.max_retries = api_config.get('retry_count', 3)

        logger.info(f"KiwoomRestAPI 초기화 - 실전투자: {is_real}, 서버: {self.host}")

    @async_measure_time
    @async_retry(max_retries=3, exceptions=(requests.RequestException,))
    async def request(self, endpoint: str, api_id: str, params: Optional[Dict[str, Any]] = None,
                     method: str = 'POST', cont_yn: str = 'N', next_key: str = '') -> Dict[str, Any]:
        """
        API 요청 전송

        Args:
            endpoint: API 엔드포인트
            api_id: API ID (TR 코드)
            params: 요청 파라미터
            method: HTTP 메소드
            cont_yn: 연속조회 여부
            next_key: 연속조회 키

        Returns:
            응답 데이터
        """
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'authorization': f'Bearer {self.access_token}',
            'cont-yn': cont_yn,
            'next-key': next_key,
            'api-id': api_id,
        }

        url = f"{self.host}{endpoint}"

        # 비동기로 처리하기 위해 이벤트 루프의 run_in_executor 사용
        loop = asyncio.get_running_loop()

        try:
            if method.upper() == 'POST':
                response = await loop.run_in_executor(
                    None,
                    lambda: requests.post(url, headers=headers, json=params or {}, timeout=self.timeout)
                )
            else:
                response = await loop.run_in_executor(
                    None,
                    lambda: requests.get(url, headers=headers, params=params or {}, timeout=self.timeout)
                )

            # 응답 상태 확인
            response.raise_for_status()

            # JSON 응답 반환
            try:
                data = response.json()
                return data
            except json.JSONDecodeError:
                logger.error(f"JSON 파싱 오류: {response.text}")
                return {"error": "JSON parsing error", "status_code": response.status_code}

        except requests.HTTPError as e:
            logger.error(f"HTTP 오류: {e}, 상태 코드: {e.response.status_code if hasattr(e, 'response') else 'N/A'}")
            status_code = e.response.status_code if hasattr(e, 'response') else 0
            error_data = {"error": str(e), "status_code": status_code}

            # 응답 내용이 있으면 추가
            if hasattr(e, 'response') and e.response and e.response.text:
                try:
                    error_data["response"] = e.response.json()
                except:
                    error_data["response"] = e.response.text

            raise requests.HTTPError(json.dumps(error_data))

        except requests.RequestException as e:
            logger.error(f"요청 오류: {e}")
            raise

    async def get_account_balance(self) -> Dict[str, Any]:
        """계좌 잔고 조회"""
        try:
            endpoint = '/api/dostk/acnt'
            api_id = 'ka10070'  # 계좌잔고조회 TR 코드

            data = await self.request(endpoint, api_id)
            logger.info(f"계좌 잔고 조회 성공")
            return data

        except Exception as e:
            logger.exception(f"계좌 잔고 조회 중 오류 발생: {str(e)}")
            return {}

    async def get_stock_price(self, stock_code: str) -> float:
        """종목 현재가 조회"""
        try:
            endpoint = '/api/dostk/mrkcond'
            api_id = 'ka10002'  # 주식현재가조회 TR 코드

            params = {
                'stk_cd': stock_code,
            }

            data = await self.request(endpoint, api_id, params)

            current_price = float(data.get('output', {}).get('prpr', 0))
            logger.debug(f"종목 {stock_code} 현재가: {current_price}")
            return current_price

        except Exception as e:
            logger.exception(f"종목 현재가 조회 중 오류 발생: {str(e)}")
            return 0

    async def get_order_history(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        기간별 주문 내역 조회

        Args:
            start_date: 시작일자 (YYYYMMDD)
            end_date: 종료일자 (YYYYMMDD)

        Returns:
            주문 내역 목록
        """
        try:
            endpoint = '/api/dostk/acnt'
            api_id = 'ka10071'  # 일별주문체결내역요청 TR 코드

            params = {
                'fr_dt': start_date,
                'to_dt': end_date,
            }

            data = await self.request(endpoint, api_id, params)

            orders = data.get('output', [])
            logger.info(f"주문 내역 조회 성공: {len(orders)}건")
            return orders

        except Exception as e:
            logger.exception(f"주문 내역 조회 중 오류 발생: {str(e)}")
            return []

    async def get_daily_chart(self, stock_code: str, days: int = 20) -> List[Dict[str, Any]]:
        """
        일봉 데이터 조회

        Args:
            stock_code: 종목코드
            days: 조회 기간 (일)

        Returns:
            일봉 데이터 목록
        """
        try:
            endpoint = '/api/dostk/chart'
            api_id = 'ka50003'  # 일봉 조회 TR 코드

            # 조회 종료일 (오늘)
            end_date = datetime.now().strftime('%Y%m%d')

            params = {
                'stk_cd': stock_code,
                'end_dt': end_date,
                'term_tp': 'D',  # 일봉
                'term_val': str(days),  # 조회 기간
                'req_cnt': str(days)  # 요청 개수
            }

            data = await self.request(endpoint, api_id, params)

            # 응답 확인
            daily_data = data.get('output', [])
            if daily_data:
                logger.info(f"일봉 데이터 조회 성공: {stock_code}, {len(daily_data)}건")
            else:
                logger.warning(f"일봉 데이터 없음: {stock_code}")

            return daily_data

        except Exception as e:
            logger.exception(f"일봉 데이터 조회 중 오류 발생: {str(e)}")
            return []

    async def get_stock_info(self, stock_code: str) -> Dict[str, Any]:
        """종목 기본 정보 조회"""
        try:
            endpoint = '/api/dostk/mrkcond'
            api_id = 'ka10001'  # 주식기본정보조회 TR 코드

            params = {
                'stk_cd': stock_code,
            }

            data = await self.request(endpoint, api_id, params)
            return data.get('output', {})

        except Exception as e:
            logger.exception(f"종목 정보 조회 중 오류 발생: {str(e)}")
            return {}

    async def buy_stock(self, stock_code: str, quantity: int, price: Optional[float] = None) -> Optional[str]:
        """
        주식 매수 주문

        Args:
            stock_code: 종목코드
            quantity: 주문수량
            price: 주문단가 (None이면 시장가)

        Returns:
            주문번호
        """
        try:
            endpoint = '/api/dostk/ordr'
            api_id = 'kt10000'  # 주식 매수주문 TR 코드

            params = {
                'dmst_stex_tp': 'KRX',  # 국내거래소: KRX
                'stk_cd': stock_code,   # 종목코드
                'ord_qty': str(quantity),  # 주문수량
                'ord_uv': str(price) if price else '',  # 주문단가 (시장가 주문은 빈값)
                'trde_tp': '1' if price else '3',  # 매매구분 (1: 지정가, 3: 시장가)
                'cond_uv': '',  # 조건단가
            }

            data = await self.request(endpoint, api_id, params)

            order_number = data.get('output', {}).get('ord_no', '')
            if order_number:
                logger.info(f"매수 주문 성공 - 종목: {stock_code}, 수량: {quantity}, 주문번호: {order_number}")
                return order_number
            else:
                logger.error(f"매수 주문 실패 - 응답에 주문번호가 없습니다: {data}")
                return None

        except Exception as e:
            logger.exception(f"매수 주문 중 오류 발생: {str(e)}")
            return None

    async def sell_stock(self, stock_code: str, quantity: int, price: Optional[float] = None) -> Optional[str]:
        """
        주식 매도 주문

        Args:
            stock_code: 종목코드
            quantity: 주문수량
            price: 주문단가 (None이면 시장가)

        Returns:
            주문번호
        """
        try:
            endpoint = '/api/dostk/ordr'
            api_id = 'kt10001'  # 주식 매도주문 TR 코드

            params = {
                'dmst_stex_tp': 'KRX',  # 국내거래소: KRX
                'stk_cd': stock_code,   # 종목코드
                'ord_qty': str(quantity),  # 주문수량
                'ord_uv': str(price) if price else '',  # 주문단가 (시장가 주문은 빈값)
                'trde_tp': '1' if price else '3',  # 매매구분 (1: 지정가, 3: 시장가)
                'cond_uv': '',  # 조건단가
            }

            data = await self.request(endpoint, api_id, params)

            order_number = data.get('output', {}).get('ord_no', '')
            if order_number:
                logger.info(f"매도 주문 성공 - 종목: {stock_code}, 수량: {quantity}, 주문번호: {order_number}")
                return order_number
            else:
                logger.error(f"매도 주문 실패 - 응답에 주문번호가 없습니다: {data}")
                return None

        except Exception as e:
            logger.exception(f"매도 주문 중 오류 발생: {str(e)}")
            return None

    async def check_order_status(self, order_number: str) -> Dict[str, Any]:
        """
        주문 체결 확인

        Args:
            order_number: 주문번호

        Returns:
            주문 상태 정보
        """
        try:
            endpoint = '/api/dostk/acnt'
            api_id = 'ka10074'  # 주문체결내역상세요청 TR 코드

            params = {
                'ord_no': order_number,
            }

            data = await self.request(endpoint, api_id, params)

            if 'output' in data:
                status = data['output'].get('ordr_stat', '')
                logger.debug(f"주문 {order_number} 상태: {status}")
                return data['output']
            else:
                logger.warning(f"주문 상태 조회 실패 - 주문번호: {order_number}, 응답: {data}")
                return {}

        except Exception as e:
            logger.exception(f"주문 상태 조회 중 오류 발생: {str(e)}")
            return {}

    async def get_order_history(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        기간별 주문 내역 조회

        Args:
            start_date: 시작일자 (YYYYMMDD)
            end_date: 종료일자 (YYYYMMDD)

        Returns:
            주문 내역 목록
        """
        try:
            endpoint = '/api/dostk/acnt'
            api_id = 'ka10071'  # 일별주문체결내역요청 TR 코드

            params = {
                'fr_dt': start_date,
                'to_dt': end_date,
            }

            data = await self.request(endpoint, api_id, params)

            orders = data.get('output', [])
            logger.info(f"주문 내역 조회 성공: {len(orders)}건")
            return orders

        except Exception as e:
            logger.exception(f"주문 내역 조회 중 오류 발생: {str(e)}")
            return []

    async def cancel_order(self, order_number: str) -> bool:
        """
        주문 취소

        Args:
            order_number: 주문번호

        Returns:
            취소 성공 여부
        """
        try:
            endpoint = '/api/dostk/ordr'
            api_id = 'kt10002'  # 주식 주문취소 TR 코드

            params = {
                'org_ord_no': order_number,  # 원주문번호
            }

            data = await self.request(endpoint, api_id, params)

            success = 'output' in data and data.get('output', {}).get('ord_no', '')

            if success:
                logger.info(f"주문 취소 성공 - 주문번호: {order_number}")
                return True
            else:
                logger.error(f"주문 취소 실패 - 주문번호: {order_number}, 응답: {data}")
                return False

        except Exception as e:
            logger.exception(f"주문 취소 중 오류 발생: {str(e)}")
            return False