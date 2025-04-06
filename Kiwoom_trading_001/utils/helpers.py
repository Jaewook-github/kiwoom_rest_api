"""
헬퍼 함수 모듈
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
import json
import os
import pandas as pd


def format_money(amount: float) -> str:
    """금액 포맷팅"""
    return f"{amount:,.0f}원"


def format_percentage(percentage: float) -> str:
    """퍼센트 포맷팅"""
    return f"{percentage:.2f}%"


def timestamp_to_str(timestamp: Optional[float] = None, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """타임스탬프를 문자열로 변환"""
    if timestamp is None:
        dt = datetime.now()
    else:
        dt = datetime.fromtimestamp(timestamp)
    return dt.strftime(format_str)


def str_to_timestamp(date_str: str, format_str: str = '%Y-%m-%d %H:%M:%S') -> float:
    """문자열을 타임스탬프로 변환"""
    dt = datetime.strptime(date_str, format_str)
    return dt.timestamp()


def get_current_time_str(format_str: str = '%Y%m%d%H%M%S') -> str:
    """현재 시간을 문자열로 반환"""
    return datetime.now().strftime(format_str)


def calculate_wait_seconds(current_time: str, target_time: str, format_str: str = '%H%M%S') -> int:
    """현재 시간부터 목표 시간까지의 대기 시간(초) 계산"""
    current = datetime.strptime(current_time, format_str)
    target = datetime.strptime(target_time, format_str)

    # 목표 시간이 현재보다 이전이면 다음날로 설정
    if target < current:
        target = target + timedelta(days=1)

    delta = target - current
    return int(delta.total_seconds())


def save_json_data(data: Any, file_path: str) -> bool:
    """데이터를 JSON 파일로 저장"""
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"JSON 데이터 저장 실패: {str(e)}")
        return False


def load_json_data(file_path: str) -> Optional[Any]:
    """JSON 파일에서 데이터 로드"""
    try:
        if not os.path.exists(file_path):
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"JSON 데이터 로드 실패: {str(e)}")
        return None


def create_dataframe_from_trades(trades: List[Dict[str, Any]]) -> pd.DataFrame:
    """거래 데이터를 DataFrame으로 변환"""
    if not trades:
        return pd.DataFrame()

    df = pd.DataFrame(trades)

    # 날짜/시간 형식 변환
    if 'timestamp' in df.columns:
        df['date'] = pd.to_datetime(df['timestamp'], unit='s')

    # 수익률 계산
    if all(col in df.columns for col in ['buy_price', 'sell_price']):
        df['profit_rate'] = (df['sell_price'] - df['buy_price']) / df['buy_price'] * 100

    return df


def calculate_portfolio_stats(holdings: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """포트폴리오 통계 계산"""
    if not holdings:
        return {
            "total_value": 0,
            "total_profit": 0,
            "total_profit_rate": 0,
            "best_stock": None,
            "worst_stock": None
        }

    total_buy_value = 0
    total_current_value = 0
    stock_profits = {}

    for code, data in holdings.items():
        buy_price = data.get('buy_price', 0)
        current_price = data.get('current_price', 0)
        quantity = data.get('quantity', 0)

        buy_value = buy_price * quantity
        current_value = current_price * quantity
        profit = current_value - buy_value
        profit_rate = (profit / buy_value * 100) if buy_value > 0 else 0

        total_buy_value += buy_value
        total_current_value += current_value
        stock_profits[code] = {
            "profit": profit,
            "profit_rate": profit_rate
        }

    # 최고/최저 수익률 종목 찾기
    if stock_profits:
        best_stock = max(stock_profits.items(), key=lambda x: x[1]["profit_rate"])
        worst_stock = min(stock_profits.items(), key=lambda x: x[1]["profit_rate"])
    else:
        best_stock = worst_stock = None

    # 전체 수익률 계산
    total_profit = total_current_value - total_buy_value
    total_profit_rate = (total_profit / total_buy_value * 100) if total_buy_value > 0 else 0

    return {
        "total_value": total_current_value,
        "total_profit": total_profit,
        "total_profit_rate": total_profit_rate,
        "best_stock": best_stock,
        "worst_stock": worst_stock
    }


async def execute_with_timeout(coro: Any, timeout: float = 30.0) -> Any:
    """비동기 작업 타임아웃 처리"""
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        raise TimeoutError(f"작업이 {timeout}초 내에 완료되지 않았습니다.")