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

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

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
    """시그널 핸들러 등록 (플랫폼 호환성 고려)"""
    # Windows에서는 signal handler가 작동하지 않으므로 처리 방식 변경
    if sys.platform == 'win32':
        # Windows에서는 KeyboardInterrupt 예외로 처리됨 (try/except 블록에서 처리)
        logger.info("Windows 환경에서는 시그널 핸들러가 지원되지 않습니다. Ctrl+C로 종료할 수 있습니다.")
        return

    # POSIX 시스템(Linux/Mac)에서만 실행
    loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(shutdown(signal.SIGINT, loop)))

    # Windows에서는 SIGTERM이 지원되지 않음
    if hasattr(signal, 'SIGTERM'):  # 안전성 추가
        loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(shutdown(signal.SIGTERM, loop)))


async def main(args):
    """메인 함수"""
    try:
        # 액세스 토큰 설정 (우선순위: 명령줄 > 환경변수 > config 파일)
        access_token = args.token or os.environ.get('KIWOOM_ACCESS_TOKEN') or config.get('auth', 'access_token')

        if not access_token:
            logger.error("액세스 토큰이 설정되지 않았습니다. 명령행 인자, 환경 변수 또는 config 파일을 확인해주세요.")
            return 1  # 에러 코드 반환

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
            return 1

        # 시스템 초기화
        initialized = await trader.initialize()
        if not initialized:
            logger.error("시스템 초기화 실패")
            return 1

        # 자동매매 시작
        started = await trader.start()
        if not started:
            logger.error("자동매매 시작 실패")
            return 1

        # 실행 중 유지
        while True:
            await asyncio.sleep(1)

    except asyncio.CancelledError:
        logger.info("메인 태스크 취소됨")
    except Exception as e:
        logger.exception(f"메인 실행 중 오류: {str(e)}")
        return 1
    finally:
        if trader:
            await shutdown()
        return 0  # 성공 코드 반환

if __name__ == "__main__":
    # 이전 코드는 유지...

    try:
        # 메인 태스크 실행
        loop.run_until_complete(main(args))
    except KeyboardInterrupt:
        logger.info("사용자에 의한 중단")
    except Exception as e:
        logger.exception(f"예상치 못한 오류: {str(e)}")
    finally:
        # 이미 종료되지 않은 경우만 종료 프로세스 실행
        # shutdown 함수가 내부적으로 호출되었는지 확인하는 플래그 추가
        if not hasattr(main, "_shutdown_called") and not loop.is_closed():
            loop.run_until_complete(shutdown(None, loop))
            main._shutdown_called = True

        if not loop.is_closed():
            loop.close()
        logger.info("프로그램 종료")