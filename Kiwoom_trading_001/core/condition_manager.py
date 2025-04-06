"""
조건검색 관리 모듈
"""
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable, Coroutine
import json

from ..config import config
from ..utils.logger import logger
from ..utils.helpers import calculate_wait_seconds, get_current_time_str
from ..api.websocket_api import KiwoomWebSocketAPI


class ConditionManager:
    """조건검색 관리 클래스"""

    def __init__(self, websocket_api: KiwoomWebSocketAPI):
        """
        초기화

        Args:
            websocket_api: WebSocket API 인스턴스
        """
        self.ws_api = websocket_api

        # 조건검색식 정보
        self.condition_list = []
        self.current_condition = None

        # 조건검색 스케줄
        self.schedule = config.get('market', 'condition_schedule') or {}

        # 조건검색 결과 저장
        self.latest_results = {}  # 조건별 최근 검색 결과
        self.realtime_results = {}  # 실시간 편입/이탈 종목

        # 조건검색 결과 콜백
        self.result_callback = None
        self.realtime_callback = None

        # 실행 중인 태스크
        self.scheduler_task = None

        logger.info("ConditionManager 초기화 완료")

    async def initialize(self) -> bool:
        """
        조건검색 관리자 초기화

        Returns:
            초기화 성공 여부
        """
        try:
            # 웹소켓 연결
            if not self.ws_api.connected:
                connected = await self.ws_api.connect()
                if not connected:
                    logger.error("웹소켓 연결 실패")
                    return False

            # 조건검색식 목록 조회
            conditions = await self.ws_api.get_condition_list()

            if conditions:
                self.condition_list = conditions
                logger.info(f"조건검색식 {len(conditions)}개 로드 완료")

                # 메시지 핸들러 등록
                self.ws_api.register_handler('CNSR', self._handle_condition_result)
                self.ws_api.register_handler('CNSRCUR', self._handle_realtime_condition)

                # 웹소켓 메시지 루프 시작
                if not hasattr(self, 'message_task') or self.message_task.done():
                    self.message_task = asyncio.create_task(self.ws_api.message_loop())

                return True
            else:
                logger.error("조건검색식 목록 로드 실패")
                return False

        except Exception as e:
            logger.exception(f"조건검색 관리자 초기화 중 오류: {str(e)}")
            return False

    def start_scheduler(self) -> None:
        """조건검색 스케줄러 시작"""
        if not self.scheduler_task or self.scheduler_task.done():
            self.scheduler_task = asyncio.create_task(self._run_scheduler())
            logger.info("조건검색 스케줄러 시작")

    def stop_scheduler(self) -> None:
        """조건검색 스케줄러 중지"""
        if self.scheduler_task and not self.scheduler_task.done():
            self.scheduler_task.cancel()
            logger.info("조건검색 스케줄러 중지")

    async def _run_scheduler(self) -> None:
        """조건검색 스케줄 실행"""
        try:
            while True:
                current_time = datetime.now().strftime("%H%M%S")

                # 다음 스케줄 찾기
                schedule_times = sorted(self.schedule.keys())
                next_times = [t for t in schedule_times if t > current_time]

                if next_times:
                    # 다음 실행 시간까지 대기
                    next_time = next_times[0]
                    condition_index = self.schedule[next_time]

                    wait_seconds = calculate_wait_seconds(current_time, next_time)
                    logger.info(f"다음 조건검색 예정: {next_time}, 조건: {condition_index}, {wait_seconds}초 후")

                    await asyncio.sleep(min(wait_seconds, 300))  # 최대 5분 대기

                    # 정확한 시간 확인
                    if datetime.now().strftime("%H%M%S") >= next_time:
                        # 조건 실행
                        await self.run_condition(condition_index)
                else:
                    # 다음 날까지 대기
                    logger.info("오늘 예정된 조건검색이 모두 완료되었습니다.")
                    await asyncio.sleep(600)  # 10분마다 확인

        except asyncio.CancelledError:
            logger.info("조건검색 스케줄러 태스크 취소됨")
        except Exception as e:
            logger.exception(f"조건검색 스케줄러 실행 중 오류: {str(e)}")

    async def run_condition(self, condition_index: int) -> bool:
        """
        조건검색 실행

        Args:
            condition_index: 조건검색식 인덱스

        Returns:
            실행 성공 여부
        """
        try:
            if not self.condition_list:
                logger.error("조건검색식 목록이 없습니다.")
                return False

            if condition_index < 0 or condition_index >= len(self.condition_list):
                logger.error(f"잘못된 조건검색 인덱스: {condition_index}")
                return False

            # 조건검색식 선택
            self.current_condition = self.condition_list[condition_index]
            condition_id = self.current_condition.get('cond_id')
            condition_name = self.current_condition.get('cond_nm')

            logger.info(f"조건검색 시작: {condition_name} (ID: {condition_id})")

            # 조건검색 실행
            success = await self.ws_api.start_condition_search(condition_id, use_realtime=True)

            if success:
                logger.info(f"조건검색 요청 성공: {condition_name}")
            else:
                logger.error(f"조건검색 요청 실패: {condition_name}")

            return success

        except Exception as e:
            logger.exception(f"조건검색 실행 중 오류: {str(e)}")
            return False

    async def _handle_condition_result(self, data: Dict[str, Any]) -> None:
        """
        조건검색 결과 처리 핸들러

        Args:
            data: 조건검색 결과 데이터
        """
        try:
            if data.get('return_code') != '0':
                logger.error(f"조건검색 결과 오류: {data.get('return_msg')}")
                return

            stock_codes = data.get('data', [])
            condition_id = self.current_condition.get('cond_id') if self.current_condition else 'unknown'
            condition_name = self.current_condition.get('cond_nm') if self.current_condition else 'unknown'

            logger.info(f"조건검색 결과 수신: {condition_name}, {len(stock_codes)}개 종목")

            # 결과 저장
            result_info = {
                'condition_id': condition_id,
                'condition_name': condition_name,
                'time': get_current_time_str(),
                'stock_codes': stock_codes
            }
            self.latest_results[condition_id] = result_info

            # 결과 콜백 호출
            if self.result_callback:
                try:
                    await self.result_callback(result_info)
                except Exception as callback_error:
                    logger.exception(f"조건검색 결과 콜백 실행 중 오류: {str(callback_error)}")

            # 검색 결과 종목 실시간 시세 등록
            if stock_codes:
                await self.ws_api.register_realtime_price(stock_codes)

        except Exception as e:
            logger.exception(f"조건검색 결과 처리 중 오류: {str(e)}")

    async def _handle_realtime_condition(self, data: Dict[str, Any]) -> None:
        """
        실시간 조건검색 결과 처리 핸들러

        Args:
            data: 실시간 조건검색 데이터
        """
        try:
            stock_code = data.get('code')
            status = data.get('status')  # '0': 이탈, '1': 편입
            condition_id = data.get('cond_id')

            if not stock_code or not condition_id:
                return

            # 조건검색식 이름 찾기
            condition_name = 'unknown'
            for cond in self.condition_list:
                if cond.get('cond_id') == condition_id:
                    condition_name = cond.get('cond_nm')
                    break

            # 편입/이탈 처리
            if status == '1':  # 편입
                logger.info(f"실시간 조건 편입: {stock_code}, 조건: {condition_name}")

                # 결과 저장
                if condition_id not in self.realtime_results:
                    self.realtime_results[condition_id] = {'in': [], 'out': []}
                self.realtime_results[condition_id]['in'].append(stock_code)

                # 실시간 시세 등록
                await self.ws_api.register_realtime_price([stock_code])

            elif status == '0':  # 이탈
                logger.info(f"실시간 조건 이탈: {stock_code}, 조건: {condition_name}")

                # 결과 저장
                if condition_id not in self.realtime_results:
                    self.realtime_results[condition_id] = {'in': [], 'out': []}
                self.realtime_results[condition_id]['out'].append(stock_code)

            # 콜백 호출
            if self.realtime_callback:
                realtime_info = {
                    'stock_code': stock_code,
                    'condition_id': condition_id,
                    'condition_name': condition_name,
                    'status': 'in' if status == '1' else 'out',
                    'time': get_current_time_str()
                }
                try:
                    await self.realtime_callback(realtime_info)
                except Exception as callback_error:
                    logger.exception(f"실시간 조건검색 콜백 실행 중 오류: {str(callback_error)}")

        except Exception as e:
            logger.exception(f"실시간 조건검색 결과 처리 중 오류: {str(e)}")

    def set_result_callback(self, callback: Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]) -> None:
        """
        조건검색 결과 콜백 설정

        Args:
            callback: 콜백 함수
        """
        self.result_callback = callback
        logger.debug("조건검색 결과 콜백 설정됨")

    def set_realtime_callback(self, callback: Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]) -> None:
        """
        실시간 조건검색 결과 콜백 설정

        Args:
            callback: 콜백 함수
        """
        self.realtime_callback = callback
        logger.debug("실시간 조건검색 결과 콜백 설정됨")

    def get_condition_by_index(self, index: int) -> Optional[Dict[str, Any]]:
        """
        인덱스로 조건검색식 조회

        Args:
            index: 조건검색식 인덱스

        Returns:
            조건검색식 정보
        """
        if not self.condition_list or index < 0 or index >= len(self.condition_list):
            return None
        return self.condition_list[index]

    def get_condition_by_id(self, condition_id: str) -> Optional[Dict[str, Any]]:
        """
        ID로 조건검색식 조회

        Args:
            condition_id: 조건검색식 ID

        Returns:
            조건검색식 정보
        """
        for condition in self.condition_list:
            if condition.get('cond_id') == condition_id:
                return condition
        return None

    def get_condition_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        이름으로 조건검색식 조회

        Args:
            name: 조건검색식 이름

        Returns:
            조건검색식 정보
        """
        for condition in self.condition_list:
            if condition.get('cond_nm') == name:
                return condition
        return None

    def get_latest_results(self, condition_id: Optional[str] = None) -> Any:
        """
        최근 조건검색 결과 조회

        Args:
            condition_id: 조건검색식 ID (None이면 모든 결과)

        Returns:
            조건검색 결과
        """
        if condition_id:
            return self.latest_results.get(condition_id)
        return self.latest_results

    def reset(self) -> None:
        """조건검색 관리자 초기화"""
        # 실행 중인 태스크 취소
        self.stop_scheduler()

        # 데이터 초기화
        self.current_condition = None
        self.latest_results.clear()
        self.realtime_results.clear()

        logger.info("조건검색 관리자 초기화 완료")