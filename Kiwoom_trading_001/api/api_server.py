"""
자동매매 모니터링 및 제어 API 서버
"""
import asyncio
import json
from typing import Dict, Any, Optional
from aiohttp import web
import os

from config import config
from utils.logger import logger


class TradingAPIServer:
    """자동매매 모니터링 및 제어 API 서버"""

    def __init__(self, trader_instance, host="127.0.0.1", port=8080):
        """
        초기화

        Args:
            trader_instance: 트레이더 인스턴스
            host: 호스트 주소
            port: 포트 번호
        """
        self.trader = trader_instance

        # 서버 설정
        monitoring_config = config.get('monitoring')
        self.host = monitoring_config.get('host', host)
        self.port = monitoring_config.get('port', port)
        self.enable_auth = monitoring_config.get('enable_auth', True)

        # API 키 설정
        self.api_key = os.environ.get("TRADING_API_KEY") or monitoring_config.get('api_key', "default_key")

        # 서버 애플리케이션
        self.app = web.Application()
        self.setup_routes()

        # 실행 태스크
        self.server_task = None

        logger.info(f"API 서버 초기화 - 호스트: {self.host}, 포트: {self.port}")

    def setup_routes(self):
        """라우트 설정"""
        # 상태 조회
        self.app.router.add_get("/api/status", self.get_status)

        # 계좌 정보
        self.app.router.add_get("/api/account", self.get_account)

        # 보유 종목
        self.app.router.add_get("/api/holdings", self.get_holdings)
        self.app.router.add_get("/api/holdings/{stock_code}", self.get_holding)

        # 주문 내역
        self.app.router.add_get("/api/orders", self.get_orders)
        self.app.router.add_get("/api/orders/{order_id}", self.get_order)

        # 조건검색
        self.app.router.add_get("/api/conditions", self.get_conditions)
        self.app.router.add_post("/api/conditions/{condition_id}/run", self.run_condition)

        # 매매 제어
        self.app.router.add_post("/api/buy", self.handle_buy)
        self.app.router.add_post("/api/sell", self.handle_sell)
        self.app.router.add_post("/api/cancel/{order_id}", self.cancel_order)

        # 시스템 제어
        self.app.router.add_post("/api/start", self.start_trading)
        self.app.router.add_post("/api/stop", self.stop_trading)

    async def start(self):
        """서버 시작"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        logger.info(f"API 서버 시작 - http://{self.host}:{self.port}")

    async def stop(self):
        """서버 중지"""
        if self.server_task and not self.server_task.done():
            self.server_task.cancel()
            try:
                await self.server_task
            except asyncio.CancelledError:
                pass
        logger.info("API 서버 중지")

    def start_server(self):
        """비동기 서버 시작"""
        if not self.server_task or self.server_task.done():
            self.server_task = asyncio.create_task(self.start())

    async def validate_auth(self, request):
        """인증 확인"""
        if not self.enable_auth:
            return True

        api_key = request.headers.get("X-API-Key")
        if not api_key or api_key != self.api_key:
            return False
        return True

    # 에러 응답 헬퍼
    def error_response(self, message, status=400):
        """에러 응답 생성"""
        return web.json_response({"error": message}, status=status)

    # 인증 필수 데코레이터 (클로저 사용)
    def auth_required(handler):
        """인증 필수 데코레이터"""

        async def wrapper(self, request):
            """인증 확인 후 핸들러 실행"""
            if not await self.validate_auth(request):
                return self.error_response("Unauthorized", 401)
            return await handler(self, request)

        return wrapper

    # ---------- API 엔드포인트 핸들러 ----------#

    @auth_required
    async def get_status(self, request):
        """시스템 상태 조회"""
        status = {
            "running": self.trader.is_running,
            "initialized": self.trader.is_initialized,
            "strategy": self.trader.strategy.name if self.trader.strategy else None,
            "holdings_count": len(self.trader.holdings),
            "pending_orders": len(self.trader.order_manager.pending_orders)
        }

        return web.json_response(status)

    @auth_required
    async def get_account(self, request):
        """계좌 정보 조회"""
        # 계좌 정보 갱신 요청
        if request.query.get('refresh') == '1':
            await self.trader._update_account_info()

        # 계좌 정보 반환
        return web.json_response(self.trader.account_info)

    @auth_required
    async def get_holdings(self, request):
        """보유 종목 목록 조회"""
        return web.json_response(self.trader.holdings)

    @auth_required
    async def get_holding(self, request):
        """특정 보유 종목 조회"""
        stock_code = request.match_info['stock_code']
        if stock_code not in self.trader.holdings:
            return self.error_response(f"종목 {stock_code}을(를) 보유하고 있지 않습니다.", 404)

        return web.json_response(self.trader.holdings[stock_code])

    @auth_required
    async def get_orders(self, request):
        """주문 내역 조회"""
        order_manager = self.trader.order_manager

        # 주문 유형 필터
        order_status = request.query.get('status', 'all')

        if order_status == 'pending':
            orders = order_manager.pending_orders
        elif order_status == 'executed':
            orders = order_manager.executed_orders
        elif order_status == 'canceled':
            orders = order_manager.canceled_orders
        else:  # 'all'
            orders = {
                'pending': order_manager.pending_orders,
                'executed': order_manager.executed_orders,
                'canceled': order_manager.canceled_orders
            }

        return web.json_response(orders)

    @auth_required
    async def get_order(self, request):
        """특정 주문 조회"""
        order_id = request.match_info['order_id']
        order_info = self.trader.order_manager.get_order_info(order_id)

        if not order_info:
            return self.error_response(f"주문 {order_id}을(를) 찾을 수 없습니다.", 404)

        return web.json_response(order_info)

    @auth_required
    async def get_conditions(self, request):
        """조건검색식 목록 조회"""
        condition_list = self.trader.condition_manager.condition_list
        return web.json_response(condition_list)

    @auth_required
    async def run_condition(self, request):
        """조건검색 실행"""
        condition_id = request.match_info['condition_id']

        # 조건검색식 ID로 인덱스 찾기
        condition_manager = self.trader.condition_manager
        condition_index = -1

        for i, condition in enumerate(condition_manager.condition_list):
            if condition.get('cond_id') == condition_id:
                condition_index = i
                break

        if condition_index == -1:
            return self.error_response(f"조건검색식 ID {condition_id}을(를) 찾을 수 없습니다.", 404)

        # 조건검색 실행
        success = await condition_manager.run_condition(condition_index)

        if success:
            return web.json_response({"success": True, "message": "조건검색 시작"})
        else:
            return self.error_response("조건검색 실행 실패")

    @auth_required
    async def handle_buy(self, request):
        """종목 매수"""
        try:
            data = await request.json()
            stock_code = data.get('stock_code')
            quantity = int(data.get('quantity', 0))
            price = float(data.get('price', 0)) if 'price' in data else None

            if not stock_code or quantity <= 0:
                return self.error_response("종목코드와 매수 수량을 올바르게 입력해주세요.")

            # 매수 주문
            order_id = await self.trader.order_manager.place_buy_order(stock_code, quantity, price)

            if order_id:
                return web.json_response({"success": True, "order_id": order_id})
            else:
                return self.error_response("매수 주문 실패")

        except json.JSONDecodeError:
            return self.error_response("잘못된 JSON 형식")
        except ValueError:
            return self.error_response("매수 수량/가격이 유효하지 않습니다.")

    @auth_required
    async def handle_sell(self, request):
        """종목 매도"""
        try:
            data = await request.json()
            stock_code = data.get('stock_code')
            quantity = int(data.get('quantity', 0))
            price = float(data.get('price', 0)) if 'price' in data else None

            if not stock_code or quantity <= 0:
                return self.error_response("종목코드와 매도 수량을 올바르게 입력해주세요.")

            # 보유 확인
            if stock_code not in self.trader.holdings:
                return self.error_response(f"종목 {stock_code}을(를) 보유하고 있지 않습니다.", 404)

            # 보유 수량 확인
            holding_quantity = self.trader.holdings[stock_code].get('quantity', 0)
            if quantity > holding_quantity:
                return self.error_response(f"보유 수량({holding_quantity})보다 많은 수량({quantity})을 매도할 수 없습니다.")

            # 매도 주문
            order_id = await self.trader.order_manager.place_sell_order(stock_code, quantity, price)

            if order_id:
                return web.json_response({"success": True, "order_id": order_id})
            else:
                return self.error_response("매도 주문 실패")

        except json.JSONDecodeError:
            return self.error_response("잘못된 JSON 형식")
        except ValueError:
            return self.error_response("매도 수량/가격이 유효하지 않습니다.")

    @auth_required
    async def cancel_order(self, request):
        """주문 취소"""
        order_id = request.match_info['order_id']

        # 주문 존재 확인
        if order_id not in self.trader.order_manager.pending_orders:
            return self.error_response(f"주문 {order_id}을(를) 찾을 수 없거나 이미 체결/취소되었습니다.", 404)

        # 주문 취소
        success = await self.trader.order_manager.cancel_order(order_id)

        if success:
            return web.json_response({"success": True, "message": f"주문 {order_id} 취소 요청됨"})
        else:
            return self.error_response("주문 취소 실패")

    @auth_required
    async def start_trading(self, request):
        """자동매매 시작"""
        if self.trader.is_running:
            return web.json_response({"success": True, "message": "자동매매가 이미 실행 중입니다."})

        success = await self.trader.start()

        if success:
            return web.json_response({"success": True, "message": "자동매매 시작"})
        else:
            return self.error_response("자동매매 시작 실패")

    @auth_required
    async def stop_trading(self, request):
        """자동매매 중지"""
        if not self.trader.is_running:
            return web.json_response({"success": True, "message": "자동매매가 실행 중이 아닙니다."})

        await self.trader.stop()
        return web.json_response({"success": True, "message": "자동매매 중지"})