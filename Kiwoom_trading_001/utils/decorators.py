"""
유틸리티 데코레이터 모듈
"""
import time
import functools
import asyncio
from typing import Callable, Any, TypeVar, cast
from logger import logger

# 제네릭 타입 정의
F = TypeVar('F', bound=Callable[..., Any])
AsyncF = TypeVar('AsyncF', bound=Callable[..., Any])

def measure_time(func: F) -> F:
    """
    함수 실행 시간 측정 데코레이터 (동기 함수용)
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        if elapsed > 1.0:  # 1초 이상 걸린 작업 로깅
            logger.warning(f"{func.__name__} 실행 시간: {elapsed:.2f}초")
        return result
    return cast(F, wrapper)

def async_measure_time(func: AsyncF) -> AsyncF:
    """
    비동기 함수 실행 시간 측정 데코레이터
    """
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = await func(*args, **kwargs)
        elapsed = time.time() - start_time
        if elapsed > 1.0:  # 1초 이상 걸린 작업 로깅
            logger.warning(f"{func.__name__} 실행 시간: {elapsed:.2f}초")
        return result
    return cast(AsyncF, wrapper)

def retry(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0,
          exceptions: tuple = (Exception,)) -> Callable[[F], F]:
    """
    재시도 데코레이터 (동기 함수용)
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            m_retries, m_delay = max_retries, delay
            while m_retries > 0:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    m_retries -= 1
                    if m_retries == 0:
                        logger.error(f"{func.__name__} 최대 재시도 횟수 초과: {e}")
                        raise
                    logger.warning(f"{func.__name__} 재시도 ({max_retries - m_retries}/{max_retries}): {e}")
                    time.sleep(m_delay)
                    m_delay *= backoff  # 지수 백오프
            return None  # 타입 체커를 위한 반환 (실제로는 도달하지 않음)
        return cast(F, wrapper)
    return decorator

def async_retry(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0,
               exceptions: tuple = (Exception,)) -> Callable[[AsyncF], AsyncF]:
    """
    비동기 재시도 데코레이터
    """
    def decorator(func: AsyncF) -> AsyncF:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            m_retries, m_delay = max_retries, delay
            while m_retries > 0:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    m_retries -= 1
                    if m_retries == 0:
                        logger.error(f"{func.__name__} 최대 재시도 횟수 초과: {e}")
                        raise
                    logger.warning(f"{func.__name__} 재시도 ({max_retries - m_retries}/{max_retries}): {e}")
                    await asyncio.sleep(m_delay)
                    m_delay *= backoff  # 지수 백오프
            return None  # 타입 체커를 위한 반환 (실제로는 도달하지 않음)
        return cast(AsyncF, wrapper)
    return decorator