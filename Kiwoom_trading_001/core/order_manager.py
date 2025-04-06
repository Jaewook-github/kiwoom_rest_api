"""
주문 관리 모듈
"""
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple, Set
import json

from ..config import config
from ..utils.logger import logger
from ..utils.helpers import get_current_time_str
from ..api.rest_api import KiwoomRestAPI


class OrderManager:
    """주문 관리 클래스"""

    def __init__(self, rest_api: KiwoomRestAPI):
        """
        초기화

        Args:
            rest_api: REST API 인스턴스
        """
        self.rest_api = rest_api

        # 주문 저장소
        self.pending_orders = {}  # 미체결 주문 정보
        self.executed_orders = {}  # 체결된 주문 정보
        self.canceled_orders = {}  # 취소된 주문 정보

        # 중복 주문 방지를 위한 플래그
        self.selling_stocks = set()  # 매도 중인 종목 코드
        self.buying_stocks = set()  # 매수 중인 종목 코드

        # 주문 타임아웃 설정 (초 단위)
        self.order_timeout = 300  # 기본 5분

        # 검사 주기 (초 단위)
        self.check_interval = 60  # 1분마다 점검

        # 실행 중인 태스크
        self.monitor_task = None

        logger.info("OrderManager 초기화 완료")

    def start_monitoring(self) -> None:
        """주문 모니터링 시작"""
        if self.monitor_task is None or self.monitor_task.done():
            self.monitor_task = asyncio.create_task(self._monitor_orders())
            logger.info("주문 모니터링 시작")

    def stop_monitoring(self) -> None:
        """주문 모니터링 중지"""
        if self.monitor_task and not self.monitor_task.done():
            self.monitor_task.cancel()
            logger.info("주문 모니터링 중지")

    async def _monitor_orders(self) -> None:
        """주문 상태 모니터링 및 처리"""
        try:
            while True:
                # 미체결 주문 상태 확인
                await self._check_pending_orders()

                # 오래된 주문 정리
                self._cleanup_old_orders()

                # 지정 시간 대기
                await asyncio.sleep(self.check_interval)

        except asyncio.CancelledError:
            logger.info("주문 모니터링 작업 취소됨")
        except Exception as e:
            logger.exception(f"주문 모니터링 중 오류: {str(e)}")

    async def _check_pending_orders(self) -> None:
        """미체결 주문 상태 확인"""
        if not self.pending_orders:
            return

        # 미체결 주문 목록 복사 (반복 중 변경될 수 있으므로)
        order_ids = list(self.pending_orders.keys())

        for order_id in order_ids:
            if order_id not in self.pending_orders:
                continue  # 이미 처리된 주문

            order_info = self.pending_orders[order_id]

            # 타임아웃 확인
            order_time = datetime.strptime(order_info['time'], '%Y%m%d%H%M%S')
            elapsed = (datetime.now() - order_time).total_seconds()

            if elapsed > self.order_timeout:
                logger.warning(f"주문 {order_id} 처리 시간 초과 - 경과: {elapsed:.0f}초, 종목: {order_info['stock_code']}")

                # 오래된 주문 자동 취소 (선택적으로 활성화)
                # await self.cancel_order(order_id)
                # continue

            # 주문 상태 확인
            order_status = await self.rest_api.check_order_status(order_id)

            # 주문 상태에 따른 처리
            if order_status:
                status_code = order_status.get('ordr_stat', '')

                # 체결 완료
                if status_code == '1':  # 주문 체결 코드 (API 문서 참조 필요)
                    logger.info(f"주문 체결 완료 - 주문번호: {order_id}, 종목: {order_info['stock_code']}")

                    # 매수/매도 상태 플래그 제거
                    stock_code = order_info['stock_code']
                    if order_info['type'] == 'buy':
                        self.buying_stocks.discard(stock_code)
                    elif order_info['type'] == 'sell':
                        self.selling_stocks.discard(stock_code)

                    # 체결 정보 저장
                    order_info['status'] = 'executed'
                    order_info['executed_time'] = get_current_time_str()
                    order_info['executed_price'] = float(order_status.get('cntr_pric', 0))
                    order_info['executed_quantity'] = int(order_status.get('cntr_qty', 0))

                    # 체결 주문으로 이동
                    self.executed_orders[order_id] = order_info
                    del self.pending_orders[order_id]

                # 주문 취소됨
                elif status_code == '2':  # 주문 취소 코드
                    logger.info(f"주문 취소됨 - 주문번호: {order_id}, 종목: {order_info['stock_code']}")

                    # 매수/매도 상태 플래그 제거
                    stock_code = order_info['stock_code']
                    if order_info['type'] == 'buy':
                        self.buying_stocks.discard(stock_code)
                    elif order_info['type'] == 'sell':
                        self.selling_stocks.discard(stock_code)

                    # 취소 정보 저장
                    order_info['status'] = 'canceled'
                    order_info['canceled_time'] = get_current_time_str()

                    # 취소 주문으로 이동
                    self.canceled_orders[order_id] = order_info
                    del self.pending_orders[order_id]

    def _cleanup_old_orders(self) -> None:
        """오래된 주문 정보 정리"""
        current_time = datetime.now()
        day_seconds = 24 * 60 * 60  # 24시간

        # 하루 이상 지난 체결/취소 주문 정리
        for order_dict in [self.executed_orders, self.canceled_orders]:
            for order_id, order_info in list(order_dict.items()):
                order_time = datetime.strptime(order_info['time'], '%Y%m%d%H%M%S')
                if (current_time - order_time).total_seconds() > day_seconds:
                    del order_dict[order_id]

    async def place_buy_order(self, stock_code: str, quantity: int, price: Optional[float] = None) -> Optional[str]:
        """
        매수 주문 처리

        Args:
            stock_code: 종목코드
            quantity: 매수 수량
            price: 매수 가격 (None이면 시장가)

        Returns:
            주문번호
        """
        # 중복 매수 주문 방지
        if stock_code in self.buying_stocks:
            logger.warning(f"종목 {stock_code}는 이미 매수 중입니다.")
            return None

        try:
            # 매수 주문
            order_number = await self.rest_api.buy_stock(stock_code, quantity, price)

            if order_number:
                # 매수 중 플래그 설정
                self.buying_stocks.add(stock_code)

                # 주문 정보 저장
                order_info = {
                    'stock_code': stock_code,
                    'quantity': quantity,
                    'price': price,
                    'type': 'buy',
                    'status': 'pending',
                    'time': get_current_time_str()
                }
                self.pending_orders[order_number] = order_info

                logger.info(f"매수 주문 등록 - 종목: {stock_code}, 수량: {quantity}, 주문번호: {order_number}")
                return order_number
            else:
                logger.error(f"매수 주문 실패 - 종목: {stock_code}, 수량: {quantity}")
                return None

        except Exception as e:
            logger.exception(f"매수 주문 처리 중 오류: {str(e)}")
            return None

    async def place_sell_order(self, stock_code: str, quantity: int, price: Optional[float] = None) -> Optional[str]:
        """
        매도 주문 처리

        Args:
            stock_code: 종목코드
            quantity: 매도 수량
            price: 매도 가격 (None이면 시장가)

        Returns:
            주문번호
        """
        # 중복 매도 주문 방지
        if stock_code in self.selling_stocks:
            logger.warning(f"종목 {stock_code}는 이미 매도 중입니다.")
            return None

        try:
            # 매도 주문
            order_number = await self.rest_api.sell_stock(stock_code, quantity, price)

            if order_number:
                # 매도 중 플래그 설정
                self.selling_stocks.add(stock_code)

                # 주문 정보 저장
                order_info = {
                    'stock_code': stock_code,
                    'quantity': quantity,
                    'price': price,
                    'type': 'sell',
                    'status': 'pending',
                    'time': get_current_time_str()
                }
                self.pending_orders[order_number] = order_info

                logger.info(f"매도 주문 등록 - 종목: {stock_code}, 수량: {quantity}, 주문번호: {order_number}")
                return order_number
            else:
                logger.error(f"매도 주문 실패 - 종목: {stock_code}, 수량: {quantity}")
                return None

        except Exception as e:
            logger.exception(f"매도 주문 처리 중 오류: {str(e)}")
            return None

    async def cancel_order(self, order_id: str) -> bool:
        """
        주문 취소

        Args:
            order_id: 주문번호

        Returns:
            취소 성공 여부
        """
        if order_id not in self.pending_orders:
            logger.warning(f"취소할 주문이 없습니다: {order_id}")
            return False

        try:
            # 주문 취소
            result = await self.rest_api.cancel_order(order_id)

            if result:
                logger.info(f"주문 취소 요청 성공: {order_id}")
                return True
            else:
                logger.error(f"주문 취소 요청 실패: {order_id}")
                return False

        except Exception as e:
            logger.exception(f"주문 취소 처리 중 오류: {str(e)}")
            return False

    def get_order_info(self, order_id: str) -> Optional[Dict[str, Any]]:
        """
        주문 정보 조회

        Args:
            order_id: 주문번호

        Returns:
            주문 정보
        """
        # 미체결/체결/취소 주문에서 순서대로 확인
        if order_id in self.pending_orders:
            return self.pending_orders[order_id]
        elif order_id in self.executed_orders:
            return self.executed_orders[order_id]
        elif order_id in self.canceled_orders:
            return self.canceled_orders[order_id]
        else:
            return None

    def get_pending_orders(self) -> List[Dict[str, Any]]:
        """미체결 주문 목록 조회"""
        return list(self.pending_orders.values())

    def get_executed_orders(self) -> List[Dict[str, Any]]:
        """체결 주문 목록 조회"""
        return list(self.executed_orders.values())

    def is_buying(self, stock_code: str) -> bool:
        """매수 중인지 확인"""
        return stock_code in self.buying_stocks

    def is_selling(self, stock_code: str) -> bool:
        """매도 중인지 확인"""
        return stock_code in self.selling_stocks

    def get_today_orders(self) -> Dict[str, List[Dict[str, Any]]]:
        """오늘 주문 내역 조회"""
        today = datetime.now().strftime('%Y%m%d')

        # 오늘 날짜로 시작하는 주문만 필터링
        pending = [order for order in self.pending_orders.values() if order['time'].startswith(today)]
        executed = [order for order in self.executed_orders.values() if order['time'].startswith(today)]
        canceled = [order for order in self.canceled_orders.values() if order['time'].startswith(today)]

        return {
            'pending': pending,
            'executed': executed,
            'canceled': canceled
        }

    def reset(self) -> None:
        """주문 관리자 초기화"""
        # 실행 중인 태스크 중지
        self.stop_monitoring()

        # 데이터 초기화
        self.pending_orders.clear()
        self.executed_orders.clear()
        self.canceled_orders.clear()
        self.buying_stocks.clear()
        self.selling_stocks.clear()

        logger.info("주문 관리자 초기화 완료")