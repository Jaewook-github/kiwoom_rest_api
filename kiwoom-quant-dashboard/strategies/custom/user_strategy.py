# strategies/custom/user_strategy.py
from strategies.base import StrategyBase
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional


class UserStrategy(StrategyBase):
    """사용자 정의 전략 템플릿"""
    
    def __init__(self, name: str = "User Strategy", description: str = "사용자 정의 퀀트 전략"):
        """사용자 정의 전략 초기화
        
        Args:
            name: 전략 이름
            description: 전략 설명
        """
        super().__init__(name=name, description=description)
        self.set_parameters(
            n_stocks=20,   # 선택할 종목 수
            # 여기에 추가 파라미터 설정
        )
        
    def run(self, data: Dict[str, Any]) -> pd.DataFrame:
        """사용자 정의 전략 실행
        
        Args:
            data: 전략 실행에 필요한 데이터
            
        Returns:
            pd.DataFrame: 전략 실행 결과
        """
        # 데이터 추출
        financial_data = data.get("financial_data", pd.DataFrame())
        price_data = data.get("price_data", {})
        current_prices = data.get("current_prices", pd.DataFrame())
        
        if financial_data.empty or current_prices.empty:
            return pd.DataFrame()
        
        # TODO: 여기에 사용자 정의 전략 로직 구현
        # 예제: 단순 랜덤 선택
        if len(financial_data) <= self.parameters['n_stocks']:
            selected_stocks = financial_data
        else:
            selected_stocks = financial_data.sample(n=self.parameters['n_stocks'])
        
        # 현재가 정보 추가
        result = pd.merge(
            selected_stocks,
            current_prices[['종목코드', '종목명', '현재가', '전일대비', '등락률']],
            on='종목코드',
            how='left'
        )
        
        return result