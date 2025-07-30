import asyncio
import time
import websockets
import json
from multiprocessing import Queue
from collections import deque

from loguru import logger
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

	# WebSocket 서버에 연결합니다.
	async def connect(self):
		try:
			self.websocket = await websockets.connect(self.uri)
			self.connected = True
			logger.info("서버와 연결을 시도 중입니다.")

			# 로그인 패킷
			param = {
				'trnm': 'LOGIN',
				'token': self.token
			}

			logger.info('실시간 시세 서버로 로그인 패킷을 전송합니다.')
			# 웹소켓 연결 시 로그인 정보 전달
			await self.send_message(message=param)

		except Exception as e:
			logger.info(f'Connection error: {e}')
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
		logger.info(f'Message sent: {message}')

	async def get_group_num(self):
		self.group_num += 1
		return self.group_num

	async def req_condition_name_list(self):
		logger.info("조건식 리스트 요청!")
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
		logger.debug("실시간 주문 접수/체결 등록!")

	# 서버에서 오는 메시지를 수신하여 출력합니다.
	async def receive_messages(self):
		await self.req_order_info()
		last_request_unix_time = time.time()
		while self.keep_running:
			try:
				# 서버로부터 수신한 메시지를 JSON 형식으로 파싱
				if not self.req_in_queue.empty():
					req_data = self.req_in_queue.get()
					if req_data['action_id'] == "실시간등록":
						종목코드 = req_data['종목코드']
						self.reqeust_list.append([self.register_realtime_group, 종목코드])
					elif req_data['action_id'] == "실시간해제":
						종목코드 = req_data['종목코드']
						group_num = self.stock_code_to_group_num_dict.get(종목코드, None)
						if group_num:
							self.reqeust_list.append([self.remove_realtime_group, group_num])
					elif req_data['action_id'] == "조건검색식리스트":
						self.reqeust_list.append([self.req_condition_name_list])
					elif req_data['action_id'] == "조건검색실시간등록":
						self.reqeust_list.append([self.register_condition_realtime_result, req_data['조건index']])
					elif req_data['action_id'] == "조건검색실시간해제":
						self.reqeust_list.append([self.remove_condition_realtime, req_data['조건index']])
				if len(self.reqeust_list) > 0:
					req_func, *args = self.reqeust_list.popleft()
					now_unix_time = time.time()
					if now_unix_time - last_request_unix_time < 1:
						self.reqeust_list.appendleft([req_func, *args])
					else:
						logger.info(f"req_func: {req_func}, args: {args} 실행!")
						last_request_unix_time = time.time()
						await req_func(*args)

				response = json.loads(await self.websocket.recv())
				tr_name = response.get('trnm')
				# 메시지 유형이 LOGIN일 경우 로그인 시도 결과 체크
				if tr_name == 'LOGIN':
					if response.get('return_code') != 0:
						logger.info('로그인 실패하였습니다. : ', response.get('return_msg'))
						await self.disconnect()
					else:
						logger.info('로그인 성공하였습니다.')
				elif tr_name == 'PING':
					await self.send_message(response)  # 메시지 유형이 PING일 경우 수신값 그대로 송신
				elif tr_name == 'CNSRLST':  # 조건검색식 리스트 수신
					df = pd.DataFrame(columns=["조건index", "조건명"])
					for condition_idx, condition_name in response.get('data', []):
						df.loc[len(df)] = {"조건index": condition_idx, "조건명": condition_name}
					self.realtime_out_queue.put(
						dict(
							action_id="조건검색식리스트",
							df=df
						)
					)
				elif tr_name == "REAL":
					for chunk_data_info_map in response.get('data', []):
						종목코드 = chunk_data_info_map['item'].replace("_AL", "").replace("A", "")
						if chunk_data_info_map['name'] == "주문체결":  # 'name' 또는 'type'으로 구분하여 접근
							tick_info_map = chunk_data_info_map['values']
							계좌번호 = tick_info_map['9201']
							주문번호 = tick_info_map['9203']
							주문상태 = tick_info_map['913']  # 접수, 체결, 확인 (취소 주문의 경우 접수 -> 확인)
							종목명 = tick_info_map['302']
							주문수량 = int(tick_info_map['900']) if tick_info_map['900'] else None
							주문가격 = float(tick_info_map['901']) if tick_info_map['901'] else None
							미체결수량 = int(tick_info_map['902']) if tick_info_map['902'] else None
							주문구분 = tick_info_map['905'].replace("+", "").replace("-", "")  # 매수, 매도, 매수정정, 매도정정, 매수취소, 매도취소
							주문및체결시간 = tick_info_map['908']

							체결가 = float(tick_info_map['910']) if tick_info_map['910'] else None
							체결량 = int(tick_info_map['911']) if tick_info_map['911'] else None
							단위체결가 = float(tick_info_map['914']) if tick_info_map['914'] else None
							단위체결량 = int(tick_info_map['915']) if tick_info_map['915'] else None
							거부사유 = tick_info_map['919']
							거래소구분명 = tick_info_map['2135']
							SOR여부 = tick_info_map['2136']
							logger.info(
								f"종목코드: {종목코드}, "
								f"계좌번호: {계좌번호}, "
								f"주문번호: {주문번호}, "
								f"주문상태: {주문상태}, "
								f"주문구분: {주문구분}, "
								f"종목명: {종목명}, "
								f"주문수량: {주문수량}, "
								f"주문가격: {주문가격}, "
								f"미체결수량: {미체결수량}, "
								f"주문및체결시간: {주문및체결시간}, "
								f"체결가: {체결가}, "
								f"체결량: {체결량}, "
								f"단위체결가: {단위체결가}, "
								f"단위체결량: {단위체결량}, "
								f"거부사유: {거부사유}, "
								f"거래소구분명: {거래소구분명}, "
								f"SOR여부: {SOR여부}"
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
						elif chunk_data_info_map['name'] == "주식체결":  # 'name' 또는 'type'으로 구분하여 접근
							tick_info_map = chunk_data_info_map['values']
							체결시간 = tick_info_map['20']
							현재가 = abs(float(tick_info_map['10']))  # 중간가 주문으로 인해 소수점 현재가 발생할 수 있음
							전일대비 = float(tick_info_map['11'])
							등락율 = float(tick_info_map['12'])
							체결량 = int(tick_info_map['15'])  # +는 매수체결,-는 매도체결
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
						elif chunk_data_info_map['name'] == "조건검색":  # 'name' 또는 'type'으로 구분하여 접근
							info_map = chunk_data_info_map['values']
							조건식idx = info_map['841'].split(' ')[0]
							종목코드 = info_map['9001'].replace('_AL', '').replace('A', '')
							편입편출 = info_map['843']  # "I": 편입, "D": 편출
							logger.info(
								f"종목코드: {종목코드}, "
								f"편입편출: {편입편출}"
							)
							self.realtime_out_queue.put(
								dict(
									action_id="조건식실시간편입편출",
									조건식idx=조건식idx,
									종목코드=종목코드,
									편입편출=편입편출,
								)
							)
				elif tr_name == 'CNSRREQ':  # 조건검색 요청 일반 결과 수신
					logger.info(f'결과: {response}')
					stock_code_list = []
					code_list = response.get('data', [])
					if code_list:  # {'trnm': 'CNSRREQ', 'return_code': 0, 'data': None}인 경우도 있음
						for per_stock_info_map in code_list:
							종목코드 = per_stock_info_map['jmcode'].replace("_AL", "").replace("A", "")
							stock_code_list.append(종목코드)
						logger.info(f"종목코드 리스트: {stock_code_list}")
				else:
					logger.info(f'실시간 시세 서버 응답 수신: {response}')

			except websockets.ConnectionClosed:
				logger.info('Connection closed by the server')
				self.connected = False
				await self.websocket.close()

	async def register_condition_realtime_result(self, condition_idx):
		logger.debug(f"{condition_idx} 실시간 등록")
		await self.send_message({
			'trnm': 'CNSRREQ',  # 서비스명
			'seq': f'{condition_idx}',  # 조건검색식 일련번호
			'search_type': '1',  # 조회타입 (1: 실시간)
			'stex_tp': 'K',  # 거래소구분
		})

	async def remove_condition_realtime(self, condition_idx):
		logger.debug(f"{condition_idx} 실시간 등록 해제")
		await self.send_message({
			'trnm': 'CNSRCLR', # 서비스명
			'seq': f'{condition_idx}',  # 조건검색식 일련번호
		})

	async def register_realtime_group(self, stock_code):
		group_num = await self.get_group_num()
		self.stock_code_to_group_num_dict[stock_code] = group_num
		await self.send_message({
			'trnm': 'REG',  # 서비스명
			'grp_no': f'{group_num}',  # 그룹번호
			'refresh': '0',  # 기존등록유지여부
			'data': [{  # 실시간 등록 리스트
				'item': [f'{stock_code}_AL'],  # 실시간 등록 요소 (SOR 시세 등록)
				'type': ['0B'],  # 실시간 항목 (주식 체결, 호가 등록)
			}]
		})
		logger.info(f"종목코드: {stock_code} 등록 완료! ")

	async def remove_realtime_group(self, group_num='1'):
		logger.info(f"그룹번호: {group_num} 실시간 등록 해지!")
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
			logger.info('Disconnected from WebSocket server')

async def main(req_in_queue, realtime_out_queue):
	# WebSocketClient 전역 변수 선언
	websocket_client = WebSocketClient(websocket_url, req_in_queue, realtime_out_queue)

	# WebSocket 클라이언트를 백그라운드에서 실행합니다.
	receive_task = asyncio.create_task(websocket_client.run())

	# 수신 작업이 종료될 때까지 대기
	await receive_task


def run_websocket(req_in_queue: Queue, realtime_out_queue: Queue):
	time.sleep(1.5)
	asyncio.run(main(req_in_queue, realtime_out_queue))


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
