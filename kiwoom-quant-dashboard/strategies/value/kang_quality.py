# strategies/value/kang_quality.py
from strategies.base import StrategyBase
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional


class KangQualityStrategy(StrategyBase):
    """강환국의 퀄리티 전략"""
    
    def __init__(self):
        """강환국 퀄리티 전략 초기화"""
        super().__init__(
            name="Kang's Quality Strategy",
            description="강환국의 퀄리티 전략 (PER, PBR, ROE, GP/A 기반)"
        )
        self.set_parameters(
            n_stocks=30,  # 선택할 종목 수
            min_market_cap=50000000000  # 최소 시가총액 (500억)
        )
        
    def run(self, data: Dict[str, Any]) -> pd.DataFrame:
        """강환국 퀄리티 전략 실행
        
        Args:
            data: {
                "financial_data": 재무제표 데이터프레임,
                "current_prices": 현재가 데이터프레임
            }
            
        Returns:
            pd.DataFrame: 퀄리티 순위 결과
        """
        financial_data = data.get("financial_data", pd.DataFrame())
        current_prices = data.get("current_prices", pd.DataFrame())
        
        if financial_data.empty or current_prices.empty:
            return pd.DataFrame()
        
        # 필요한 데이터 확인 및 계산
        if 'PER' not in financial_data.columns:
            financial_data['PER'] = financial_data.get('시가총액', 0) / financial_data.get('당기순이익', 1)
            
        if 'PBR' not in financial_data.columns:
            financial_data['PBR'] = financial_data.get('시가총액', 0) / financial_data.get('자본총계', 1)
            
        if 'ROE' not in financial_data.columns:
            financial_data['ROE'] = financial_data.get('당기순이익', 0) / financial_data.get('자본총계', 1) * 100
            
        if 'GP/A' not in financial_data.columns:
            financial_data['GP/A'] = financial_data.get('매출총이익', 0) / financial_data.get('자산총계', 1) * 100
        
        # 필터링: 시가총액이 최소 기준 이상
        filtered_data = financial_data[financial_data['시가총액'] >= self.parameters['min_market_cap']]
        
        # 필터링: PER > 0, PBR > 0
        filtered_data = filtered_data[(filtered_data['PER'] > 0) & (filtered_data['PBR'] > 0)]
        
        if filtered_data.empty:
            return pd.DataFrame()
        
        # 퀄리티 전략 계산
        # 1. PER 순위 매기기 (낮을수록 좋음)
        filtered_data['PER_rank'] = filtered_data['PER'].rank()
        
        # 2. PBR 순위 매기기 (낮을수록 좋음)
        filtered_data['PBR_rank'] = filtered_data['PBR'].rank()
        
        # 3. ROE 순위 매기기 (높을수록 좋음)
        filtered_data['ROE_rank'] = filtered_data['ROE'].rank(ascending=False)
        
        # 4. GP/A 순위 매기기 (높을수록 좋음)
        filtered_data['GP/A_rank'] = filtered_data['GP/A'].rank(ascending=False)
        
        # 5. 종합 순위 계산
        filtered_data['quality_rank'] = (
            filtered_data['PER_rank'] + 
            filtered_data['PBR_rank'] + 
            filtered_data['ROE_rank'] + 
            filtered_data['GP/A_rank']
        )
        
        # 6. 최종 순위로 정렬
        result = filtered_data.sort_values('quality_rank')
        
        # 7. 상위 N개 종목 선택
        if len(result) > self.parameters['n_stocks']:
            result = result.head(self.parameters['n_stocks'])
        
        # 현재가 정보 추가
        result = pd.merge(
            result,
            current_prices[['종목코드', '종목명', '현재가', '전일대비', '등락률']],
            on='종목코드',
            how='left'
        )
        
        return result[['종목코드', '종목명_y', 'PER', 'PBR', 'ROE', 'GP/A', 'quality_rank', '현재가', '전일대비', '등락률']]

