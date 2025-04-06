"""
키움증권 자동매매 시스템 실행 파일
"""
import asyncio
import argparse
import os
import signal
import sys

from config import config
from utils.logger import logger
from core.trader import KiwoomAutoTrader
from strategies.condition_strategy import ConditionStrategy
from strategies.ma_cross_strategy import MACrossStrategy

# 전역 변수 - 트레이더 인스턴스
trader = None


async def shutdown(signal_=None, loop=None):
    """프로그램 종료 처리"""
    if signal_:
        logger.info(f"시그널 수신: {signal_.name}")

    logger.info("자동매매 시스템 종료 중...")

    # 트레이더 중지
    global trader
    if trader:
        await trader.stop()

    # 이벤트 루프 중지
    if loop:
        tasks = [t for t in asyncio.all_tasks(loop) if t is not asyncio.current_task()]
        if tasks:
            logger.info(f"{len(tasks)}개 실행 중인 태스크 취소...")
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)

        loop.stop()

    logger.info("자동매매 시스템 종료 완료")


def register_signals(loop):
    """시그널 핸들러 등록"""
    # Windows에서는 SIGTERM이 지원되지 않음
    if sys.platform != 'win32':
        loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(shutdown(signal.SIGTERM, loop)))

    # Ctrl+C 처리
    loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(shutdown(signal.SIGINT, loop)))


async def main(args):
    """메인 함수"""
    try:
        # 액세스 토큰 설정
        access_token = args.token or os.environ.get('KIWOOM_ACCESS_TOKEN')
        if not access_token:
            logger.error("액세스 토큰이 설정되지 않았습니다. 명령행 인자 또는 환경 변수 KIWOOM_ACCESS_TOKEN를 설정해주세요.")
            sys.exit(1)

        # 트레이더 인스턴스 생성
        global trader
        trader = KiwoomAutoTrader(access_token=access_token, is_real=args.real)

        # 전략 설정
        if args.strategy == 'condition':
            strategy = ConditionStrategy()
            trader.set_strategy(strategy)
        elif args.strategy == 'ma_cross':
            strategy = MACrossStrategy(trader.rest_api)
            trader.set_strategy(strategy)
        else:
            logger.error(f"알 수 없는 전략: {args.strategy}")
            return

        # 시스템 초기화
        initialized = await trader.initialize()
        if not initialized:
            logger.error("시스템 초기화 실패")
            return

        # 자동매매 시작
        started = await trader.start()
        if not started:
            logger.error("자동매매 시작 실패")
            return

        # 실행 중 유지
        while True:
            await asyncio.sleep(1)

    except asyncio.CancelledError:
        logger.info("메인 태스크 취소됨")
    except Exception as e:
        logger.exception(f"메인 실행 중 오류: {str(e)}")
    finally:
        await shutdown()


if __name__ == "__main__":
    # 명령행 인자 파싱
    parser = argparse.ArgumentParser(description="키움증권 자동매매 시스템")
    parser.add_argument("--token", type=str, help="키움증권 접근 토큰")
    parser.add_argument("--real", action="store_true", help="실전투자 모드 (지정하지 않으면 모의투자)")
    parser.add_argument("--strategy", type=str, default="condition", choices=["condition", "ma_cross"],
                        help="매매 전략 (condition: 조건검색 기반, ma_cross: 이동평균 교차)")

    args = parser.parse_args()

    # 이벤트 루프 설정
    loop = asyncio.get_event_loop()

    # 시그널 핸들러 등록
    register_signals(loop)

    try:
        # 메인 태스크 실행
        loop.run_until_complete(main(args))
    except KeyboardInterrupt:
        logger.info("사용자에 의한 중단")
    finally:
        loop.close()
        logger.info("프로그램 종료")