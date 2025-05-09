# strategies/value/magic_formula.py
from strategies.base import StrategyBase
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional


class MagicFormula(StrategyBase):
    """조엘 그린블랫의 마법공식 전략"""
    
    def __init__(self):
        """마법공식 전략 초기화"""
        super().__init__(
            name="Magic Formula",
            description="조엘 그린블랫의 마법공식 (영업이익률과 자본수익률 기반)"
        )
        self.set_parameters(
            n_stocks=30,  # 선택할 종목 수
            min_market_cap=50000000000  # 최소 시가총액 (500억)
        )
        
    def run(self, data: Dict[str, Any]) -> pd.DataFrame:
        """마법공식 전략 실행
        
        Args:
            data: {
                "financial_data": 재무제표 데이터프레임,
                "current_prices": 현재가 데이터프레임
            }
            
        Returns:
            pd.DataFrame: 마법공식 순위 결과
        """
        financial_data = data.get("financial_data", pd.DataFrame())
        current_prices = data.get("current_prices", pd.DataFrame())
        
        if financial_data.empty or current_prices.empty:
            return pd.DataFrame()
        
        # 필요한 컬럼 확인 및 계산
        if 'EBIT' not in financial_data.columns or 'EV' not in financial_data.columns:
            # EBIT(영업이익), EV(기업가치) 계산
            financial_data['EBIT'] = financial_data.get('영업이익', 0)
            
            # EV = 시가총액 + 총부채 - 현금 및 현금성자산
            financial_data['EV'] = financial_data.get('시가총액', 0) + \
                                 financial_data.get('총부채', 0) - \
                                 financial_data.get('현금및현금성자산', 0)
        
        # 필터링: 시가총액이 최소 기준 이상
        filtered_data = financial_data[financial_data['시가총액'] >= self.parameters['min_market_cap']]
        
        # 필터링: EBIT > 0, EV > 0, 투자자본 > 0
        filtered_data = filtered_data[(filtered_data['EBIT'] > 0) & 
                                     (filtered_data['EV'] > 0) & 
                                     (filtered_data.get('투자자본', 0) > 0)]
        
        if filtered_data.empty:
            return pd.DataFrame()
        
        # 마법공식 계산
        # 1. 영업이익률(EBIT/EV) 계산 및 순위 매기기
        filtered_data['EBIT/EV'] = filtered_data['EBIT'] / filtered_data['EV']
        filtered_data['EBIT/EV_rank'] = filtered_data['EBIT/EV'].rank(ascending=False)
        
        # 2. 자본수익률(ROC = EBIT/투자자본) 계산 및 순위 매기기
        filtered_data['ROC'] = filtered_data['EBIT'] / filtered_data.get('투자자본', 1)
        filtered_data['ROC_rank'] = filtered_data['ROC'].rank(ascending=False)
        
        # 3. 종합 순위 계산
        filtered_data['magic_rank'] = filtered_data['EBIT/EV_rank'] + filtered_data['ROC_rank']
        
        # 4. 최종 순위로 정렬
        result = filtered_data.sort_values('magic_rank')
        
        # 5. 상위 N개 종목 선택
        if len(result) > self.parameters['n_stocks']:
            result = result.head(self.parameters['n_stocks'])
        
        # 현재가 정보 추가
        result = pd.merge(
            result,
            current_prices[['종목코드', '종목명', '현재가', '전일대비', '등락률']],
            on='종목코드',
            how='left'
        )
        
        return result[['종목코드', '종목명_y', 'EBIT/EV', 'ROC', 'magic_rank', '현재가', '전일대비', '등락률']]
