"""
키움증권 WebSocket API 통신 모듈
"""
import asyncio
import json
from typing import Dict, Any, Optional, List, Callable, Coroutine
import websockets
from websockets.exceptions import ConnectionClosed

from config import config
from utils.logger import logger
from utils.decorators import async_measure_time
from utils.helpers import execute_with_timeout


class KiwoomWebSocketAPI:
    """키움증권 WebSocket API 클래스"""

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
            self.host = api_config.get('real_server', {}).get('ws_host',
                                                              'wss://api.kiwoom.com:10000/api/dostk/websocket')
        else:
            self.host = api_config.get('mock_server', {}).get('ws_host',
                                                              'wss://mockapi.kiwoom.com:10000/api/dostk/websocket')

        # 웹소켓 클라이언트
        self.client = None
        self.connected = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 10
        self.reconnect_delay = 2  # 초 단위, 지수 백오프로 증가

        # 응답 핸들러 등록
        self.message_handlers = {}
        self.default_handler = None

        # 연결 상태 모니터링
        self.last_activity = 0
        self.ping_interval = 30  # 30초마다 핑
        self.ping_task = None

        logger.info(f"KiwoomWebSocketAPI 초기화 - 실전투자: {is_real}, 서버: {self.host}")

    @async_measure_time
    async def connect(self) -> bool:
        """
        웹소켓 연결 및 로그인

        Returns:
            연결 성공 여부
        """
        if self.connected and self.client:
            logger.debug("이미 웹소켓에 연결되어 있습니다.")
            return True

        try:
            # 웹소켓 연결
            self.client = await websockets.connect(
                self.host,
                ping_interval=None,  # 자체 ping 처리를 위해 비활성화
                ping_timeout=None,
                close_timeout=10,
                max_size=10 * 1024 * 1024  # 최대 메시지 크기 (10MB)
            )

            # 로그인 패킷 전송
            login_message = {
                'trnm': 'LOGIN',
                'token': self.access_token
            }
            await self.client.send(json.dumps(login_message))

            # 로그인 응답 수신
            response = json.loads(await self.client.recv())

            if response.get('trnm') == 'LOGIN':
                if response.get('return_code') != '0':
                    logger.error(f"웹소켓 로그인 실패: {response.get('return_msg')}")
                    await self.close()
                    return False
                else:
                    logger.info("웹소켓 로그인 성공")
                    self.connected = True
                    self.reconnect_attempts = 0

                    # PING 모니터링 시작
                    if self.ping_task is None or self.ping_task.done():
                        self.ping_task = asyncio.create_task(self._ping_monitor())

                    return True
            else:
                logger.error(f"웹소켓 로그인 응답 오류: {response}")
                await self.close()
                return False

        except Exception as e:
            logger.exception(f"웹소켓 연결 중 오류 발생: {str(e)}")
            if self.client:
                await self.close()
            return False

    async def close(self) -> None:
        """웹소켓 연결 종료"""
        if self.ping_task and not self.ping_task.done():
            self.ping_task.cancel()

        if self.client:
            try:
                await self.client.close()
            except Exception as e:
                logger.error(f"웹소켓 종료 중 오류: {str(e)}")
            finally:
                self.client = None
                self.connected = False

    async def reconnect(self) -> bool:
        """웹소켓 재연결"""
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            logger.error(f"최대 재연결 시도 횟수 초과: {self.reconnect_attempts}")
            return False

        self.reconnect_attempts += 1
        delay = self.reconnect_delay * (2 ** (self.reconnect_attempts - 1))  # 지수 백오프
        delay = min(delay, 60)  # 최대 60초

        logger.warning(f"웹소켓 재연결 시도 ({self.reconnect_attempts}/{self.max_reconnect_attempts}) - {delay}초 후")

        await asyncio.sleep(delay)
        return await self.connect()

    async def _ping_monitor(self) -> None:
        """PING 모니터링 및 전송 루프"""
        try:
            while self.connected and self.client:
                await asyncio.sleep(self.ping_interval)

                if not self.connected or not self.client:
                    break

                try:
                    # PING 메시지 전송
                    ping_message = {
                        'trnm': 'PING'
                    }
                    await self.client.send(json.dumps(ping_message))
                    logger.debug("PING 메시지 전송")

                except Exception as e:
                    logger.error(f"PING 전송 중 오류: {str(e)}")
                    # 연결 문제가 있을 수 있으므로 재연결 시도
                    self.connected = False
                    asyncio.create_task(self.reconnect())
                    break

        except asyncio.CancelledError:
            logger.debug("PING 모니터링 태스크 취소됨")
        except Exception as e:
            logger.exception(f"PING 모니터링 중 오류: {str(e)}")

    async def _send_message(self, message: Dict[str, Any]) -> bool:
        """
        메시지 전송

        Args:
            message: 전송할 메시지

        Returns:
            전송 성공 여부
        """
        if not self.connected or not self.client:
            logger.error("웹소켓이 연결되지 않았습니다.")
            return False

        try:
            await self.client.send(json.dumps(message))
            return True
        except Exception as e:
            logger.error(f"메시지 전송 중 오류: {str(e)}")
            # 연결 문제가 있을 수 있으므로 재연결 시도
            self.connected = False
            asyncio.create_task(self.reconnect())
            return False

    def register_handler(self, message_type: str,
                         handler: Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]) -> None:
        """
        메시지 핸들러 등록

        Args:
            message_type: 메시지 유형 (trnm 필드 값)
            handler: 핸들러 함수
        """
        self.message_handlers[message_type] = handler
        logger.debug(f"메시지 핸들러 등록: {message_type}")

    def set_default_handler(self, handler: Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]) -> None:
        """
        기본 메시지 핸들러 설정

        Args:
            handler: 핸들러 함수
        """
        self.default_handler = handler

    async def message_loop(self) -> None:
        """
        메시지 수신 루프
        """
        if not self.connected or not self.client:
            logger.error("웹소켓이 연결되지 않았습니다.")
            return

        try:
            while self.connected and self.client:
                try:
                    # 메시지 수신
                    message = await self.client.recv()
                    data = json.loads(message)

                    # 메시지 유형 확인
                    trnm = data.get('trnm', '')

                    # PING 응답은 그대로 전송
                    if trnm == 'PING':
                        await self._send_message(data)
                        continue

                    # 핸들러 호출
                    if trnm in self.message_handlers:
                        asyncio.create_task(self.message_handlers[trnm](data))
                    elif self.default_handler:
                        asyncio.create_task(self.default_handler(data))
                    else:
                        logger.debug(f"미처리 메시지: {trnm}")

                except ConnectionClosed:
                    logger.warning("웹소켓 연결이 종료되었습니다.")
                    self.connected = False

                    # 재연결 시도
                    if await self.reconnect():
                        logger.info("웹소켓 재연결 성공")
                    else:
                        logger.error("웹소켓 재연결 실패, 메시지 루프 종료")
                        break

                except json.JSONDecodeError as e:
                    logger.error(f"JSON 파싱 오류: {str(e)}, 메시지: {message[:100]}...")

                except Exception as e:
                    logger.exception(f"메시지 처리 중 오류: {str(e)}")

        except asyncio.CancelledError:
            logger.debug("메시지 루프 태스크 취소됨")
            await self.close()

        except Exception as e:
            logger.exception(f"메시지 루프 중 오류: {str(e)}")
            await self.close()

    async def get_condition_list(self) -> List[Dict[str, Any]]:
        """
        조건검색식 목록 조회

        Returns:
            조건검색식 목록
        """
        if not self.connected:
            if not await self.connect():
                logger.error("웹소켓 연결 실패")
                return []

        try:
            # 응답을 기다리기 위한 Future 객체
            response_future = asyncio.Future()

            # 임시 핸들러 등록
            async def condition_list_handler(data: Dict[str, Any]) -> None:
                if not response_future.done():
                    if data.get('return_code') == '0':
                        conditions = data.get('data', [])
                        response_future.set_result(conditions)
                    else:
                        response_future.set_result([])

            # 기존 핸들러 백업 및 임시 핸들러 등록
            original_handler = self.message_handlers.get('CNSRLST')
            self.register_handler('CNSRLST', condition_list_handler)

            # 조건검색식 목록 요청
            condition_req = {
                'trnm': 'CNSRLST'
            }

            if not await self._send_message(condition_req):
                logger.error("조건검색식 목록 요청 전송 실패")
                # 원래 핸들러 복원
                if original_handler:
                    self.register_handler('CNSRLST', original_handler)
                return []

            # 응답 대기 (30초 타임아웃)
            try:
                conditions = await execute_with_timeout(response_future, 30.0)
                logger.info(f"조건검색식 목록 조회 성공: {len(conditions)}개")

                # 조건검색식 목록 출력
                for i, condition in enumerate(conditions):
                    logger.info(f"조건검색식 {i + 1}: {condition.get('cond_nm')} (ID: {condition.get('cond_id')})")

                return conditions
            except TimeoutError:
                logger.error("조건검색식 목록 조회 타임아웃")
                if not response_future.done():
                    response_future.cancel()
                return []
            finally:
                # 원래 핸들러 복원
                if original_handler:
                    self.register_handler('CNSRLST', original_handler)

        except Exception as e:
            logger.exception(f"조건검색식 목록 조회 중 오류 발생: {str(e)}")
            return []

    async def start_condition_search(self, condition_id: str, use_realtime: bool = True) -> bool:
        """
        조건검색 시작

        Args:
            condition_id: 조건검색식 ID
            use_realtime: 실시간 사용 여부

        Returns:
            요청 성공 여부
        """
        if not self.connected:
            if not await self.connect():
                logger.error("웹소켓 연결 실패")
                return False

        try:
            # 조건검색 요청
            search_req = {
                'trnm': 'CNSR',
                'cond_id': condition_id,
                'mrkt_tp': '001',  # 001: 코스피
                'mrkt_tp2': '101',  # 101: 코스닥
                'real_typ': '1' if use_realtime else '0'  # 0: 실시간 미사용, 1: 실시간 사용
            }

            result = await self._send_message(search_req)
            if result:
                logger.info(f"조건검색 요청 전송 성공: {condition_id}")
            else:
                logger.error(f"조건검색 요청 전송 실패: {condition_id}")

            return result

        except Exception as e:
            logger.exception(f"조건검색 시작 중 오류 발생: {str(e)}")
            return False

    async def register_realtime_price(self, stock_codes: List[str]) -> bool:
        """
        실시간 시세 등록

        Args:
            stock_codes: 종목코드 목록

        Returns:
            등록 성공 여부
        """
        if not stock_codes:
            logger.warning("등록할 종목 코드가 없습니다.")
            return False

        if not self.connected:
            if not await self.connect():
                logger.error("웹소켓 연결 실패")
                return False

        try:
            # 실시간 시세 등록 요청
            register_req = {
                'trnm': 'REG',
                'grp_no': '1',
                'refresh': '1',
                'data': [{
                    'item': stock_codes,
                    'type': ['01']  # 01: 현재가, 등락율, 시가, 고가, 저가
                }]
            }

            result = await self._send_message(register_req)
            if result:
                logger.info(f"{len(stock_codes)}개 종목 실시간 시세 등록 성공")
            else:
                logger.error(f"실시간 시세 등록 실패")

            return result

        except Exception as e:
            logger.exception(f"실시간 시세 등록 중 오류 발생: {str(e)}")
            return False

    async def unregister_realtime_price(self, stock_codes: List[str]) -> bool:
        """
        실시간 시세 해제

        Args:
            stock_codes: 종목코드 목록

        Returns:
            해제 성공 여부
        """
        if not stock_codes:
            return True

        if not self.connected:
            return False

        try:
            # 실시간 시세 등록 해제 요청
            unregister_req = {
                'trnm': 'UNREG',
                'grp_no': '1',
                'data': [{
                    'item': stock_codes,
                    'type': ['01']
                }]
            }

            result = await self._send_message(unregister_req)
            if result:
                logger.info(f"{len(stock_codes)}개 종목 실시간 시세 등록 해제")

            return result

        except Exception as e:
            logger.exception(f"실시간 시세 해제 중 오류 발생: {str(e)}")
            return False