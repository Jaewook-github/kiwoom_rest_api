import asyncio
import time
import websockets
import json
from multiprocessing import Queue
from collections import deque

from enhanced_logging import logger, log_websocket, log_trading, log_order, log_error, log_info, log_debug
import pandas as pd

from utils import KiwoomTR
from config import websocket_url


class WebSocketClient:
    def __init__(self, uri='', req_in_queue=None, realtime_out_queue=None):
        self.uri = uri
        self.websocket = None
        self.connected = False
        self.keep_running = True
        kiwoom_tr = KiwoomTR()
        self.token = kiwoom_tr.token
        self.req_in_queue = req_in_queue
        self.realtime_out_queue = realtime_out_queue
        self.stock_code_to_group_num_dict = dict()
        self.group_num = 10
        self.reqeust_list = deque()
        log_websocket("WebSocketClient 초기화 완료")

    # WebSocket 서버에 연결합니다.
    async def connect(self):
        try:
            log_websocket(f"웹소켓 서버 연결 시도: {self.uri}")
            self.websocket = await websockets.connect(self.uri)
            self.connected = True
            log_websocket("웹소켓 서버 연결 성공")

            # 로그인 패킷
            param = {
                'trnm': 'LOGIN',
                'token': self.token
            }

            log_websocket('실시간 시세 서버로 로그인 패킷 전송')
            # 웹소켓 연결 시 로그인 정보 전달
            await self.send_message(message=param)

        except Exception as e:
            log_error(f'웹소켓 연결 에러: {e}', exception=True)
            self.connected = False

    # 서버에 메시지를 보냅니다. 연결이 없다면 자동으로 연결합니다.
    async def send_message(self, message):
        if not self.connected:
            await self.connect()  # 연결이 끊어졌다면 재연결
        if self.connected:
            # message가 문자열이 아니면 JSON으로 직렬화
            if not isinstance(message, str):
                message = json.dumps(message)

            await self.websocket.send(message)
            log_websocket(f'웹소켓 메시지 전송: {message}')

    async def get_group_num(self):
        self.group_num += 1
        return self.group_num

    async def req_condition_name_list(self):
        log_websocket("조건식 리스트 요청")
        await self.send_message({
            'trnm': 'CNSRLST',  # TR명
        })

    async def req_order_info(self):
        await self.send_message({  # 실시간 주문 접수/체결 등록
            'trnm': 'REG',  # 서비스명
            'grp_no': '1',  # 그룹번호
            'refresh': '1',  # 기존등록유지여부
            'data': [{  # 실시간 등록 리스트
                'item': [''],  # 실시간 등록 요소
                'type': ['00'],  # 실시간 항목
            }]
        })
        log_websocket("실시간 주문 접수/체결 등록 완료")

    # 서버에서 오는 메시지를 수신하여 출력합니다.
    async def receive_messages(self):
        await self.req_order_info()
        last_request_unix_time = time.time()

        while self.keep_running:
            try:
                # 요청 큐 처리
                if not self.req_in_queue.empty():
                    req_data = self.req_in_queue.get()
                    log_websocket(f"웹소켓 요청 수신: {req_data}")

                    if req_data['action_id'] == "실시간등록":
                        종목코드 = req_data['종목코드']
                        self.reqeust_list.append([self.register_realtime_group, 종목코드])
                        log_websocket(f"실시간등록 요청 큐에 추가: {종목코드}")

                    elif req_data['action_id'] == "실시간해제":
                        종목코드 = req_data['종목코드']
                        group_num = self.stock_code_to_group_num_dict.get(종목코드, None)
                        if group_num:
                            self.reqeust_list.append([self.remove_realtime_group, group_num])
                            log_websocket(f"실시간해제 요청 큐에 추가: {종목코드} (그룹: {group_num})")

                    elif req_data['action_id'] == "조건검색식리스트":
                        self.reqeust_list.append([self.req_condition_name_list])
                        log_websocket("조건검색식리스트 요청 큐에 추가")

                    elif req_data['action_id'] == "조건검색실시간등록":
                        self.reqeust_list.append([self.register_condition_realtime_result, req_data['조건index']])
                        log_websocket(f"조건검색실시간등록 요청 큐에 추가: {req_data['조건index']}")

                    elif req_data['action_id'] == "조건검색실시간해제":
                        self.reqeust_list.append([self.remove_condition_realtime, req_data['조건index']])
                        log_websocket(f"조건검색실시간해제 요청 큐에 추가: {req_data['조건index']}")

                # 요청 리스트 처리
                if len(self.reqeust_list) > 0:
                    req_func, *args = self.reqeust_list.popleft()
                    now_unix_time = time.time()
                    if now_unix_time - last_request_unix_time < 1:
                        self.reqeust_list.appendleft([req_func, *args])
                    else:
                        log_websocket(f"웹소켓 요청 실행: {req_func.__name__}, args: {args}")
                        last_request_unix_time = time.time()
                        await req_func(*args)

                # 웹소켓 메시지 수신
                response = json.loads(await self.websocket.recv())
                tr_name = response.get('trnm')

                # 메시지 유형별 처리
                if tr_name == 'LOGIN':
                    if response.get('return_code') != 0:
                        log_error(f'웹소켓 로그인 실패: {response.get("return_msg")}')
                        await self.disconnect()
                    else:
                        log_websocket('웹소켓 로그인 성공')

                elif tr_name == 'PING':
                    await self.send_message(response)  # 메시지 유형이 PING일 경우 수신값 그대로 송신
                    log_debug("PING 응답 전송")

                elif tr_name == 'CNSRLST':  # 조건검색식 리스트 수신
                    df = pd.DataFrame(columns=["조건index", "조건명"])
                    condition_count = 0
                    for condition_idx, condition_name in response.get('data', []):
                        df.loc[len(df)] = {"조건index": condition_idx, "조건명": condition_name}
                        condition_count += 1

                    log_websocket(f"조건검색식 리스트 수신: {condition_count}개")
                    self.realtime_out_queue.put(
                        dict(
                            action_id="조건검색식리스트",
                            df=df
                        )
                    )

                elif tr_name == "REAL":
                    for chunk_data_info_map in response.get('data', []):
                        종목코드 = chunk_data_info_map['item'].replace("_AL", "").replace("A", "")

                        if chunk_data_info_map['name'] == "주문체결":
                            tick_info_map = chunk_data_info_map['values']
                            계좌번호 = tick_info_map['9201']
                            주문번호 = tick_info_map['9203']
                            주문상태 = tick_info_map['913']
                            종목명 = tick_info_map['302']
                            주문수량 = int(tick_info_map['900']) if tick_info_map['900'] else None
                            주문가격 = float(tick_info_map['901']) if tick_info_map['901'] else None
                            미체결수량 = int(tick_info_map['902']) if tick_info_map['902'] else None
                            주문구분 = tick_info_map['905'].replace("+", "").replace("-", "")
                            주문및체결시간 = tick_info_map['908']
                            체결가 = float(tick_info_map['910']) if tick_info_map['910'] else None
                            체결량 = int(tick_info_map['911']) if tick_info_map['911'] else None
                            단위체결가 = float(tick_info_map['914']) if tick_info_map['914'] else None
                            단위체결량 = int(tick_info_map['915']) if tick_info_map['915'] else None
                            거부사유 = tick_info_map['919']

                            log_order(
                                f"주문체결 수신 - 종목: {종목명}({종목코드}), "
                                f"주문상태: {주문상태}, 주문구분: {주문구분}, "
                                f"주문번호: {주문번호}, 주문수량: {주문수량}, "
                                f"단위체결가: {단위체결가}, 단위체결량: {단위체결량}"
                            )

                            self.realtime_out_queue.put(
                                dict(
                                    action_id="주문접수및체결",
                                    종목코드=종목코드,
                                    계좌번호=계좌번호,
                                    주문번호=주문번호,
                                    주문상태=주문상태,
                                    주문구분=주문구분,
                                    종목명=종목명,
                                    주문수량=주문수량,
                                    주문가격=주문가격,
                                    미체결수량=미체결수량,
                                    주문및체결시간=주문및체결시간,
                                    체결가=체결가,
                                    체결량=체결량,
                                    단위체결가=단위체결가,
                                    단위체결량=단위체결량,
                                )
                            )

                        elif chunk_data_info_map['name'] == "주식체결":
                            tick_info_map = chunk_data_info_map['values']
                            체결시간 = tick_info_map['20']
                            현재가 = abs(float(tick_info_map['10']))
                            전일대비 = float(tick_info_map['11'])
                            등락율 = float(tick_info_map['12'])
                            체결량 = int(tick_info_map['15'])

                            log_debug(f"실시간체결 - 종목: {종목코드}, 현재가: {현재가:,}, 등락율: {등락율:.2f}%")

                            self.realtime_out_queue.put(
                                dict(
                                    action_id="실시간체결",
                                    종목코드=종목코드,
                                    체결시간=체결시간,
                                    현재가=현재가,
                                    전일대비=전일대비,
                                    등락율=등락율,
                                    체결량=체결량,
                                )
                            )

                        elif chunk_data_info_map['name'] == "조건검색":
                            info_map = chunk_data_info_map['values']
                            조건식idx = info_map['841'].split(' ')[0]
                            종목코드 = info_map['9001'].replace('_AL', '').replace('A', '')
                            편입편출 = info_map['843']  # "I": 편입, "D": 편출

                            log_websocket(f"조건검색 편입편출 - 종목: {종목코드}, 편입편출: {편입편출}, 조건식: {조건식idx}")

                            self.realtime_out_queue.put(
                                dict(
                                    action_id="조건식실시간편입편출",
                                    조건식idx=조건식idx,
                                    종목코드=종목코드,
                                    편입편출=편입편출,
                                )
                            )

                elif tr_name == 'CNSRREQ':  # 조건검색 요청 일반 결과 수신
                    stock_code_list = []
                    code_list = response.get('data', [])
                    if code_list:
                        for per_stock_info_map in code_list:
                            종목코드 = per_stock_info_map['jmcode'].replace("_AL", "").replace("A", "")
                            stock_code_list.append(종목코드)
                        log_websocket(f"조건검색 결과 수신: {len(stock_code_list)}개 종목")
                        log_debug(f"조건검색 종목리스트: {stock_code_list}")
                    else:
                        log_websocket("조건검색 결과: 해당 종목 없음")

                else:
                    log_websocket(f'기타 실시간 메시지 수신: {tr_name}')
                    log_debug(f'실시간 응답 상세: {response}')

            except websockets.ConnectionClosed:
                log_error('웹소켓 연결이 서버에 의해 종료됨')
                self.connected = False
                await self.websocket.close()
            except Exception as e:
                log_error(f'웹소켓 메시지 수신 중 에러: {str(e)}', exception=True)

    async def register_condition_realtime_result(self, condition_idx):
        log_websocket(f"조건식 실시간 등록: {condition_idx}")
        await self.send_message({
            'trnm': 'CNSRREQ',  # 서비스명
            'seq': f'{condition_idx}',  # 조건검색식 일련번호
            'search_type': '1',  # 조회타입 (1: 실시간)
            'stex_tp': 'K',  # 거래소구분
        })

    async def remove_condition_realtime(self, condition_idx):
        log_websocket(f"조건식 실시간 등록 해제: {condition_idx}")
        await self.send_message({
            'trnm': 'CNSRCLR',  # 서비스명
            'seq': f'{condition_idx}',  # 조건검색식 일련번호
        })

    async def register_realtime_group(self, stock_code):
        group_num = await self.get_group_num()
        self.stock_code_to_group_num_dict[stock_code] = group_num

        log_websocket(f"실시간 등록: {stock_code} (그룹: {group_num})")
        await self.send_message({
            'trnm': 'REG',  # 서비스명
            'grp_no': f'{group_num}',  # 그룹번호
            'refresh': '0',  # 기존등록유지여부
            'data': [{  # 실시간 등록 리스트
                'item': [f'{stock_code}_AL'],  # 실시간 등록 요소 (SOR 시세 등록)
                'type': ['0B'],  # 실시간 항목 (주식 체결, 호가 등록)
            }]
        })
        log_websocket(f"실시간 등록 완료: {stock_code}")

    async def remove_realtime_group(self, group_num='1'):
        log_websocket(f"실시간 등록 해제: 그룹 {group_num}")
        await self.send_message({
            'trnm': 'REMOVE',  # 서비스명
            'grp_no': group_num,  # 그룹번호
        })

    # WebSocket 실행
    async def run(self):
        await self.connect()
        await self.receive_messages()

    # WebSocket 연결 종료
    async def disconnect(self):
        self.keep_running = False
        if self.connected and self.websocket:
            await self.websocket.close()
            self.connected = False
            log_websocket('웹소켓 연결 종료')


async def main(req_in_queue, realtime_out_queue):
    # WebSocketClient 전역 변수 선언
    websocket_client = WebSocketClient(websocket_url, req_in_queue, realtime_out_queue)

    # WebSocket 클라이언트를 백그라운드에서 실행합니다.
    receive_task = asyncio.create_task(websocket_client.run())

    # 수신 작업이 종료될 때까지 대기
    await receive_task


def run_websocket(req_in_queue: Queue, realtime_out_queue: Queue):
    time.sleep(1.5)
    log_info("웹소켓 프로세스 시작")
    try:
        asyncio.run(main(req_in_queue, realtime_out_queue))
    except Exception as e:
        log_error(f"웹소켓 프로세스 실행 중 에러: {str(e)}", exception=True)


if __name__ == '__main__':
    req_in_queue = Queue()
    realtime_out_queue = Queue()
    req_in_queue.put(
        dict(
            action_id="실시간등록",
            종목코드="005930"
        )
    )
    run_websocket(req_in_queue, realtime_out_queue)