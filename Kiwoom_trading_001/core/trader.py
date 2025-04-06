"""
트레이더 핵심 모듈
"""
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional, Set, Tuple
import os
import json

from config import config
from utils.logger import logger
from utils.helpers import get_current_time_str, save_json_data, load_json_data, calculate_portfolio_stats, \
    calculate_wait_seconds
from api.rest_api import KiwoomRestAPI
from api.websocket_api import KiwoomWebSocketAPI
from core.order_manager import OrderManager
from core.condition_manager import ConditionManager
from strategies.base_strategy import BaseStrategy


class KiwoomAutoTrader:
    """키움증권 자동매매 시스템 클래스"""

    def __init__(self, access_token: str, is_real: bool = False):
        """
        초기화

        Args:
            access_token: 키움증권 접근 토큰
            is_real: 실전투자 여부 (False면 모의투자)
        """
        self.access_token = access_token
        self.is_real = is_real
        self.is_initialized = False
        self.is_running = False

        # 트레이딩 설정
        self.trading_config = config.get('trading')

        # API 인스턴스 생성
        self.rest_api = KiwoomRestAPI(access_token, is_real)
        self.ws_api = KiwoomWebSocketAPI(access_token, is_real)

        # 관리자 인스턴스 생성
        self.order_manager = OrderManager(self.rest_api)
        self.condition_manager = ConditionManager(self.ws_api)

        # 전략 인스턴스
        self.strategy: Optional[BaseStrategy] = None

        # 보유 종목 정보
        self.holdings: Dict[str, Dict[str, Any]] = {}

        # 계좌 정보
        self.account_info: Dict[str, Any] = {}

        # 시장 운영 정보
        self.market_config = config.get('market')
        self.market_start_time = self.market_config.get('start_time', "090000")
        self.market_end_time = self.market_config.get('end_time', "153000")

        # 실행 중인 태스크
        self.main_task = None
        self.market_monitor_task = None
        self.profit_check_task = None

        # 데이터 저장 경로
        self.data_dir = config.get('system', 'data_dir', './trading_data')
        os.makedirs(self.data_dir, exist_ok=True)

        logger.info(f"KiwoomAutoTrader 초기화 - 실전투자: {is_real}")

    async def initialize(self) -> bool:
        """
        시스템 초기화

        Returns:
            초기화 성공 여부
        """
        try:
            logger.info("시스템 초기화 시작")

            # 웹소켓 연결
            ws_connected = await self.ws_api.connect()
            if not ws_connected:
                logger.error("웹소켓 연결 실패")
                return False

            # 조건검색 관리자 초기화
            condition_initialized = await self.condition_manager.initialize()
            if not condition_initialized:
                logger.error("조건검색 관리자 초기화 실패")
                return False

            # 콜백 등록
            self.condition_manager.set_result_callback(self._handle_condition_result)
            self.condition_manager.set_realtime_callback(self._handle_realtime_condition)

            # 실시간 시세 핸들러 등록
            self.ws_api.register_handler('REALT', self._handle_realtime_price)

            # 계좌 정보 조회
            await self._update_account_info()

            # 주문 모니터링 시작
            self.order_manager.start_monitoring()

            logger.info("시스템 초기화 완료")
            self.is_initialized = True
            return True

        except Exception as e:
            logger.exception(f"시스템 초기화 중 오류: {str(e)}")
            return False

    def set_strategy(self, strategy: BaseStrategy) -> None:
        """
        매매 전략 설정

        Args:
            strategy: 전략 인스턴스
        """
        self.strategy = strategy
        logger.info(f"매매 전략 설정: {strategy.name}")

    async def start(self) -> bool:
        """
        자동매매 시작

        Returns:
            시작 성공 여부
        """
        if not self.is_initialized:
            initialized = await self.initialize()
            if not initialized:
                logger.error("시스템 초기화 실패로 자동매매 시작 불가")
                return False

        if not self.strategy:
            logger.error("전략이 설정되지 않아 자동매매 시작 불가")
            return False

        if self.is_running:
            logger.warning("자동매매가 이미 실행 중입니다.")
            return True

        try:
            logger.info("자동매매 시작")
            self.is_running = True

            # 보유 종목 정보 불러오기
            await self._load_holdings()

            # 보유 종목 실시간 시세 등록
            if self.holdings:
                stock_codes = list(self.holdings.keys())
                await self.ws_api.register_realtime_price(stock_codes)
                logger.info(f"{len(stock_codes)}개 보유 종목 실시간 시세 등록")

            # 조건검색 스케줄러 시작
            self.condition_manager.start_scheduler()

            # 시장 모니터링 시작
            self.market_monitor_task = asyncio.create_task(self._monitor_market())

            # 익절/손절 모니터링 시작
            self.profit_check_task = asyncio.create_task(self._check_profit_loss_periodically())

            # 메인 루프 시작
            self.main_task = asyncio.create_task(self._main_loop())

            logger.info("자동매매 시작 완료")
            return True

        except Exception as e:
            logger.exception(f"자동매매 시작 중 오류: {str(e)}")
            self.is_running = False
            return False

    async def stop(self) -> None:
        """자동매매 중지"""
        if not self.is_running:
            logger.warning("자동매매가 실행 중이 아닙니다.")
            return

        logger.info("자동매매 중지 중...")
        self.is_running = False

        # 태스크 취소
        for task in [self.main_task, self.market_monitor_task, self.profit_check_task]:
            if task and not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        # 조건검색 스케줄러 중지
        self.condition_manager.stop_scheduler()

        # 보유 종목 정보 저장
        await self._save_holdings()

        logger.info("자동매매 중지 완료")

    async def _main_loop(self) -> None:
        """메인 처리 루프"""
        try:
            while self.is_running:
                # 장 중에만 작업 수행
                current_time = datetime.now().strftime("%H%M%S")

                if self.market_start_time <= current_time <= self.market_end_time:
                    # 계좌 정보 갱신
                    await self._update_account_info()

                # 10분마다 실행
                await asyncio.sleep(600)

        except asyncio.CancelledError:
            logger.info("메인 루프 취소됨")
        except Exception as e:
            logger.exception(f"메인 루프 중 오류: {str(e)}")

    async def _monitor_market(self) -> None:
        """시장 시간 모니터링"""
        try:
            while self.is_running:
                current_time = datetime.now().strftime("%H%M%S")

                # 장 시작 전
                if current_time < self.market_start_time:
                    # 시작 시간까지 대기
                    wait_seconds = calculate_wait_seconds(current_time, self.market_start_time)
                    logger.info(f"장 시작 대기 중... {wait_seconds}초 후 시작")
                    await asyncio.sleep(min(wait_seconds, 300))  # 최대 5분 대기

                # 장 중
                elif self.market_start_time <= current_time <= self.market_end_time:
                    # 10분마다 확인
                    await asyncio.sleep(600)

                # 장 종료 후
                else:
                    logger.info("장 종료")
                    # 종료 작업 수행
                    await self._perform_market_close_tasks()

                    # 다음 날 장 시작까지 대기
                    tomorrow_market_seconds = 24 * 60 * 60 - calculate_wait_seconds("000000",
                                                                                    current_time) + calculate_wait_seconds(
                        "000000", self.market_start_time)

                    logger.info(f"다음 거래일까지 대기... (약 {tomorrow_market_seconds // 3600}시간)")
                    await asyncio.sleep(min(tomorrow_market_seconds, 3600))  # 최대 1시간 대기

        except asyncio.CancelledError:
            logger.info("시장 모니터링 태스크 취소됨")
        except Exception as e:
            logger.exception(f"시장 모니터링 중 오류: {str(e)}")

    async def _perform_market_close_tasks(self) -> None:
        """장 마감 후 작업 수행"""
        try:
            # 계좌 정보 최종 갱신
            await self._update_account_info()

            # 보유 종목 정보 저장
            await self._save_holdings()

            # 당일 거래 내역 저장
            await self._save_daily_report()

            logger.info("장 마감 후 작업 완료")

        except Exception as e:
            logger.exception(f"장 마감 후 작업 중 오류: {str(e)}")

    async def _update_account_balance(self) -> Dict[str, Any]:
        """
        계좌 잔고 조회 및 업데이트

        Returns:
            계좌 정보
        """
        try:
            # 계좌 잔고 조회
            data = await self.rest_api.get_account_balance()

            if not data:
                logger.error("계좌 잔고 조회 실패")
                return {}

            # 계좌 요약 정보
            if 'output1' in data:
                self.account_info.update(data['output1'])

            # 보유 종목 정보 업데이트
            if 'output2' in data:
                # 기존 보유 종목 백업
                old_holdings = self.holdings.copy()
                self.holdings.clear()

                for item in data['output2']:
                    stock_code = item.get('stk_cd', '')
                    if not stock_code:
                        continue

                    # 기존 정보 유지 (매수가, 매수일 등)
                    holding_info = old_holdings.get(stock_code, {})

                    # 새로운 정보로 업데이트
                    holding_info.update({
                        'buy_price': float(item.get('pchs_avg_pric', 0)),
                        'quantity': int(item.get('hldn_qty', 0)),
                        'current_price': float(item.get('prpr', 0)),
                        'name': item.get('stk_nm', ''),
                        'open_price': float(item.get('stck_oprc', 0)),  # 당일 시가
                        'updated_at': get_current_time_str()
                    })

                    # 수익률 계산
                    buy_price = holding_info['buy_price']
                    current_price = holding_info['current_price']
                    if buy_price > 0:
                        profit_rate = (current_price - buy_price) / buy_price * 100
                        holding_info['profit_rate'] = profit_rate

                    self.holdings[stock_code] = holding_info

                logger.info(f"보유 종목 수: {len(self.holdings)}")

            return self.account_info

        except Exception as e:
            logger.exception(f"계좌 잔고 조회 중 오류: {str(e)}")
            return {}

    async def _update_account_info(self) -> None:
        """계좌 정보 업데이트"""
        try:
            # 계좌 잔고 조회
            account_data = await self._update_account_balance()

            if account_data:
                # 포트폴리오 통계 계산
                portfolio_stats = calculate_portfolio_stats(self.holdings)
                self.account_info['portfolio_stats'] = portfolio_stats

                # 가용 현금
                available_cash = float(account_data.get('cash_amt', 0))
                logger.info(f"계좌 정보 업데이트 - 가용 현금: {available_cash:,.0f}원")

                # 평가 손익
                total_profit = portfolio_stats.get('total_profit', 0)
                total_profit_rate = portfolio_stats.get('total_profit_rate', 0)
                logger.info(f"평가 손익: {total_profit:,.0f}원 ({total_profit_rate:.2f}%)")

        except Exception as e:
            logger.exception(f"계좌 정보 업데이트 중 오류: {str(e)}")

    async def _save_holdings(self) -> None:
        """보유 종목 정보 저장"""
        try:
            if not self.holdings:
                return

            # 파일 경로 설정
            file_path = f"{self.data_dir}/holdings.json"

            # 저장할 데이터 준비
            data = {
                'timestamp': get_current_time_str(),
                'holdings': self.holdings
            }

            # 파일 저장
            success = save_json_data(data, file_path)

            if success:
                logger.info(f"보유 종목 정보 저장 완료: {file_path}")
            else:
                logger.error("보유 종목 정보 저장 실패")

        except Exception as e:
            logger.exception(f"보유 종목 정보 저장 중 오류: {str(e)}")

    async def _load_holdings(self) -> None:
        """보유 종목 정보 불러오기"""
        try:
            # 파일 경로 설정
            file_path = f"{self.data_dir}/holdings.json"

            # 파일 로드
            data = load_json_data(file_path)

            if data and 'holdings' in data:
                self.holdings = data['holdings']
                logger.info(f"보유 종목 정보 로드 완료: {len(self.holdings)}개 종목")

                # 현재가 갱신
                await self._update_account_balance()
            else:
                logger.info("저장된 보유 종목 정보가 없습니다.")

        except Exception as e:
            logger.exception(f"보유 종목 정보 로드 중 오류: {str(e)}")

    async def _save_daily_report(self) -> None:
        """일일 거래 내역 저장"""
        try:
            # 오늘 날짜
            today = datetime.now().strftime('%Y%m%d')

            # 오늘의 주문 내역
            today_orders = self.order_manager.get_today_orders()

            # 계좌 정보
            account_info = {
                'cash': self.account_info.get('cash_amt', 0),
                'portfolio_value': self.account_info.get('portfolio_stats', {}).get('total_value', 0),
                'profit': self.account_info.get('portfolio_stats', {}).get('total_profit', 0),
                'profit_rate': self.account_info.get('portfolio_stats', {}).get('total_profit_rate', 0)
            }

            # 보고서 데이터
            report_data = {
                'date': today,
                'account': account_info,
                'holdings': self.holdings,
                'orders': today_orders,
                'executed_count': len(today_orders['executed']),
                'buy_count': len([o for o in today_orders['executed'] if o['type'] == 'buy']),
                'sell_count': len([o for o in today_orders['executed'] if o['type'] == 'sell'])
            }

            # 파일 저장
            file_path = f"{self.data_dir}/report_{today}.json"
            success = save_json_data(report_data, file_path)

            if success:
                logger.info(f"일일 거래 내역 저장 완료: {file_path}")
            else:
                logger.error("일일 거래 내역 저장 실패")

        except Exception as e:
            logger.exception(f"일일 거래 내역 저장 중 오류: {str(e)}")

    async def _handle_condition_result(self, result_info: Dict[str, Any]) -> None:
        """
        조건검색 결과 핸들러

        Args:
            result_info: 조건검색 결과 정보
        """
        if not self.is_running or not self.strategy:
            return

        try:
            stock_codes = result_info.get('stock_codes', [])

            if not stock_codes:
                logger.info("조건검색 결과가 없습니다.")
                return

            # 주문 관련 정보 일시 캐싱
            buying_stocks = self.order_manager.buying_stocks
            selling_stocks = self.order_manager.selling_stocks

            # 전략에 조건검색 결과 전달 (전략이 ConditionStrategy인 경우)
            if hasattr(self.strategy, 'handle_condition_result'):
                self.strategy.handle_condition_result(result_info)

            # 계좌 정보 갱신
            await self._update_account_info()

            # 가용 현금 확인
            available_cash = float(self.account_info.get('cash_amt', 0))
            if available_cash <= 0:
                logger.warning("가용 현금이 없습니다.")
                return

            # 최대 매수 종목 수 확인
            max_stocks = self.strategy.max_stocks
            current_count = len(self.holdings) + len(buying_stocks)

            if current_count >= max_stocks:
                logger.info(f"이미 최대 종목 수({max_stocks})에 도달했습니다: {current_count}개")
                return

            available_slots = max_stocks - current_count

            # 종목당 투자금액 계산
            max_budget_per_stock = min(available_cash / available_slots, self.strategy.max_budget_per_stock)

            if max_budget_per_stock < self.trading_config.get('min_budget_per_stock', 100000):
                logger.warning(f"종목당 투자금액이 너무 적습니다: {max_budget_per_stock:,.0f}원")
                return

            # 매수 처리
            for stock_code in stock_codes[:available_slots]:
                # 이미 보유/매수/매도 중인 종목은 스킵
                if (stock_code in self.holdings or
                        stock_code in buying_stocks or
                        stock_code in selling_stocks):
                    continue

                # 현재가 조회
                current_price = await self.rest_api.get_stock_price(stock_code)

                if current_price <= 0:
                    logger.warning(f"종목 {stock_code} 현재가 조회 실패")
                    continue

                # 매수 조건 확인
                buy_condition = await self.strategy.analyze_buy_condition(
                    stock_code, current_price, result_info
                )

                if buy_condition[0]:  # 매수 조건 충족
                    # 매수 수량 계산
                    quantity = await self.strategy.calculate_quantity(
                        stock_code, current_price, max_budget_per_stock
                    )

                    if quantity <= 0:
                        continue

                    # 매수 주문
                    order_id = await self.order_manager.place_buy_order(stock_code, quantity)

                    if order_id:
                        logger.info(f"매수 주문 - 종목: {stock_code}, 수량: {quantity}, 사유: {buy_condition[1]}")

                    # 슬롯 하나 사용
                    available_slots -= 1
                    if available_slots <= 0:
                        break

        except Exception as e:
            logger.exception(f"조건검색 결과 처리 중 오류: {str(e)}")

    async def _handle_realtime_condition(self, realtime_info: Dict[str, Any]) -> None:
        """
        실시간 조건검색 결과 핸들러

        Args:
            realtime_info: 실시간 조건검색 정보
        """
        if not self.is_running or not self.strategy:
            return

        try:
            # 전략에 실시간 조건검색 결과 전달 (전략이 ConditionStrategy인 경우)
            if hasattr(self.strategy, 'handle_realtime_condition'):
                self.strategy.handle_realtime_condition(realtime_info)

            # 편입 종목은 실시간 시세 등록
            stock_code = realtime_info.get('stock_code')
            status = realtime_info.get('status')

            if status == 'in' and stock_code:
                # 이미 보유/매수/매도 중인 종목은 스킵
                if (stock_code in self.holdings or
                        stock_code in self.order_manager.buying_stocks or
                        stock_code in self.order_manager.selling_stocks):
                    return

                # 현재가 조회
                current_price = await self.rest_api.get_stock_price(stock_code)

                if current_price <= 0:
                    return

                # 추가 정보 준비
                additional_info = {
                    'condition_id': realtime_info.get('condition_id', ''),
                    'condition_name': realtime_info.get('condition_name', ''),
                    'time': realtime_info.get('time', '')
                }

                # 매수 조건 확인
                buy_condition = await self.strategy.analyze_buy_condition(
                    stock_code, current_price, additional_info
                )

                if buy_condition[0]:  # 매수 조건 충족
                    # 추가 확인 필요 (계좌 정보, 최대 종목 수 등)
                    # 여기서는 바로 매수하지 않고 표시만 함
                    logger.info(f"실시간 매수 후보 - 종목: {stock_code}, 사유: {buy_condition[1]}")

        except Exception as e:
            logger.exception(f"실시간 조건검색 결과 처리 중 오류: {str(e)}")

    async def _handle_realtime_price(self, data: Dict[str, Any]) -> None:
        """
        실시간 시세 핸들러

        Args:
            data: 실시간 시세 데이터
        """
        if not self.is_running or not self.strategy:
            return

        try:
            stock_code = data.get('code')
            real_type = data.get('type')

            if not stock_code or real_type != '01':  # 현재가 정보
                return

            # 현재가 추출
            current_price = 0
            try:
                current_price = float(data.get('value', {}).get('prpr', 0))
            except (ValueError, TypeError):
                return

            if current_price <= 0:
                return

            # 보유 종목이면 현재가 업데이트 및 익절/손절 확인
            if stock_code in self.holdings:
                # 매도 중인 종목은 스킵
                if stock_code in self.order_manager.selling_stocks:
                    return

                # 현재가 업데이트
                self.holdings[stock_code]['current_price'] = current_price

                # 매도 조건 확인
                await self._check_sell_condition(stock_code, current_price)

        except Exception as e:
            logger.exception(f"실시간 시세 처리 중 오류: {str(e)}")

    async def _check_sell_condition(self, stock_code: str, current_price: float) -> None:
        """
        매도 조건 확인

        Args:
            stock_code: 종목코드
            current_price: 현재가
        """
        if stock_code not in self.holdings or not self.strategy:
            return

        try:
            # 매도 조건 확인
            holding_info = self.holdings[stock_code]
            sell_condition = await self.strategy.analyze_sell_condition(
                stock_code, holding_info, current_price
            )

            if sell_condition[0]:  # 매도 조건 충족
                quantity = holding_info.get('quantity', 0)

                if quantity <= 0:
                    return

                # 매도 주문
                order_id = await self.order_manager.place_sell_order(stock_code, quantity)

                if order_id:
                    logger.info(f"매도 주문 - 종목: {stock_code}, 수량: {quantity}, 사유: {sell_condition[1]}")

                    # 부분 매도 아니면 보유 종목에서 제거
                    # (실제 삭제는 주문 체결 확인 후 이루어짐)

        except Exception as e:
            logger.exception(f"매도 조건 확인 중 오류: {str(e)}")

    async def _check_profit_loss_periodically(self) -> None:
        """주기적인 익절/손절 확인"""
        try:
            while self.is_running:
                # 장 중에만 작업 수행
                current_time = datetime.now().strftime("%H%M%S")

                if self.market_start_time <= current_time <= self.market_end_time:
                    # 보유 종목 익절/손절 확인
                    await self._check_all_holdings()

                # 5분마다 실행
                await asyncio.sleep(300)

        except asyncio.CancelledError:
            logger.info("익절/손절 모니터링 태스크 취소됨")
        except Exception as e:
            logger.exception(f"익절/손절 모니터링 중 오류: {str(e)}")

    async def _check_all_holdings(self) -> None:
        """모든 보유 종목 익절/손절 확인"""
        if not self.holdings or not self.strategy:
            return

        try:
            # 현재 보유 종목 목록 (도중에 변경될 수 있으므로 복사)
            stock_codes = list(self.holdings.keys())

            for stock_code in stock_codes:
                # 이미 매도 중인 종목은 스킵
                if stock_code in self.order_manager.selling_stocks:
                    continue

                # 보유 정보가 없어진 경우 스킵
                if stock_code not in self.holdings:
                    continue

                # 현재가 확인
                holding_info = self.holdings[stock_code]
                current_price = holding_info.get('current_price', 0)

                if current_price <= 0:
                    # API로 현재가 조회
                    current_price = await self.rest_api.get_stock_price(stock_code)

                    if current_price <= 0:
                        continue

                    # 현재가 업데이트
                    self.holdings[stock_code]['current_price'] = current_price

                # 매도 조건 확인
                sell_condition = await self.strategy.analyze_sell_condition(
                    stock_code, holding_info, current_price
                )

                if sell_condition[0]:  # 매도 조건 충족
                    quantity = holding_info.get('quantity', 0)

                    if quantity <= 0:
                        continue

                    # 매도 주문
                    order_id = await self.order_manager.place_sell_order(stock_code, quantity)

                    if order_id:
                        logger.info(f"주기적 검사 매도 주문 - 종목: {stock_code}, 수량: {quantity}, 사유: {sell_condition[1]}")

        except Exception as e:
            logger.exception(f"보유 종목 익절/손절 확인 중 오류: {str(e)}")