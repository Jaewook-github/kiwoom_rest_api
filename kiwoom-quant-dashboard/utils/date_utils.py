"""
키움증권 REST API 퀀트 대시보드 프로젝트의 유틸리티 모듈
- 날짜 유틸리티
- 재무 유틸리티
- 시각화 유틸리티
"""

# utils/date_utils.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional, Union, Tuple
import pytz


def get_korea_time() -> datetime:
    """한국 현재 시간 반환
    
    Returns:
        datetime: 한국 시간
    """
    korea_tz = pytz.timezone('Asia/Seoul')
    return datetime.now(korea_tz)


def is_market_open() -> bool:
    """현재 한국 주식 시장이 열려있는지 확인
    
    Returns:
        bool: 시장 개장 여부
    """
    now = get_korea_time()
    
    # 주말 체크
    if now.weekday() >= 5:  # 토요일(5)이나 일요일(6)
        return False
    
    # 시간 체크 (9:00 - 15:30)
    market_open = now.replace(hour=9, minute=0, second=0, microsecond=0)
    market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)
    
    return market_open <= now <= market_close


def get_previous_business_day(date: Optional[datetime] = None, n: int = 1) -> datetime:
    """이전 영업일 계산
    
    Args:
        date: 기준 날짜 (기본값: 현재 시간)
        n: 이전 영업일 수 (기본값: 1)
        
    Returns:
        datetime: 이전 영업일
    """
    if date is None:
        date = get_korea_time()
    
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    count = 0
    while count < n:
        date = date - timedelta(days=1)
        
        # 주말 제외
        if date.weekday() < 5:  # 월요일(0) ~ 금요일(4)
            count += 1
    
    return date


def get_next_business_day(date: Optional[datetime] = None, n: int = 1) -> datetime:
    """다음 영업일 계산
    
    Args:
        date: 기준 날짜 (기본값: 현재 시간)
        n: 다음 영업일 수 (기본값: 1)
        
    Returns:
        datetime: 다음 영업일
    """
    if date is None:
        date = get_korea_time()
    
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    count = 0
    while count < n:
        date = date + timedelta(days=1)
        
        # 주말 제외
        if date.weekday() < 5:  # 월요일(0) ~ 금요일(4)
            count += 1
    
    return date


def date_range(start_date: Union[str, datetime], end_date: Union[str, datetime], 
              freq: str = 'D', business_days_only: bool = True) -> List[datetime]:
    """날짜 범위 생성
    
    Args:
        start_date: 시작 날짜
        end_date: 종료 날짜
        freq: 날짜 간격 ('D': 일간, 'W': 주간, 'M': 월간, 'Q': 분기, 'Y': 년간)
        business_days_only: 영업일만 포함 여부
        
    Returns:
        List[datetime]: 날짜 목록
    """
    # 문자열을 datetime으로 변환
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
    
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)
    
    # 날짜 범위 생성
    if freq == 'D':
        date_list = pd.date_range(start=start_date, end=end_date, freq='D')
    elif freq == 'W':
        date_list = pd.date_range(start=start_date, end=end_date, freq='W-MON')
    elif freq == 'M':
        date_list = pd.date_range(start=start_date, end=end_date, freq='MS')
    elif freq == 'Q':
        date_list = pd.date_range(start=start_date, end=end_date, freq='QS')
    elif freq == 'Y':
        date_list = pd.date_range(start=start_date, end=end_date, freq='YS')
    else:
        date_list = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 영업일만 필터링
    if business_days_only:
        date_list = [d for d in date_list if d.weekday() < 5]
    
    return date_list


def format_date(date: datetime, format_str: str = '%Y%m%d') -> str:
    """날짜 형식 변환
    
    Args:
        date: 날짜
        format_str: 날짜 형식 문자열
        
    Returns:
        str: 형식이 변환된 날짜 문자열
    """
    return date.strftime(format_str)


def parse_date(date_str: str, format_str: str = '%Y%m%d') -> datetime:
    """날짜 문자열 파싱
    
    Args:
        date_str: 날짜 문자열
        format_str: 날짜 형식 문자열
        
    Returns:
        datetime: 파싱된 날짜
    """
    return datetime.strptime(date_str, format_str)


def get_period_start_end(period: str) -> Tuple[datetime, datetime]:
    """기간 시작/종료일 계산
    
    Args:
        period: 기간 지정 ('1D', '1W', '1M', '3M', '6M', '1Y', '3Y', '5Y', 'YTD')
        
    Returns:
        Tuple[datetime, datetime]: (시작일, 종료일)
    """
    today = get_korea_time()
    end_date = today
    
    if period == '1D':
        start_date = today - timedelta(days=1)
    elif period == '1W':
        start_date = today - timedelta(days=7)
    elif period == '1M':
        start_date = today.replace(month=today.month - 1) if today.month > 1 else today.replace(year=today.year - 1, month=12)
    elif period == '3M':
        start_date = today.replace(month=today.month - 3) if today.month > 3 else today.replace(year=today.year - 1, month=today.month + 9)
    elif period == '6M':
        start_date = today.replace(month=today.month - 6) if today.month > 6 else today.replace(year=today.year - 1, month=today.month + 6)
    elif period == '1Y':
        start_date = today.replace(year=today.year - 1)
    elif period == '3Y':
        start_date = today.replace(year=today.year - 3)
    elif period == '5Y':
        start_date = today.replace(year=today.year - 5)
    elif period == 'YTD':
        start_date = today.replace(month=1, day=1)
    else:
        start_date = today - timedelta(days=30)  # 기본값: 1개월
    
    return start_date, end_date
