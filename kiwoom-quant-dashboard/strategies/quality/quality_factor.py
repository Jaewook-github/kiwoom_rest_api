# strategies/quality/quality_factor.py
from strategies.base import StrategyBase
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional


class QualityFactorStrategy(StrategyBase):
    """퀄리티 팩터 전략"""
    
    def __init__(self):
        """퀄리티 팩터 전략 초기화"""
        super().__init__(
            name="Quality Factor Strategy",
            description="퀄리티 팩터를 활용한 우량 기업 발굴 전략"
        )
        self.set_parameters(
            n_stocks=30,                 # 선택할 종목 수
            min_market_cap=50000000000,  # 최소 시가총액 (500억)
            min_roe=10,                  # 최소 ROE (%)
            min_roa=5,                   # 최소 ROA (%)
            max_debt_ratio=150,          # 최대 부채비율 (%)
            min_operating_margin=10,     # 최소 영업이익률 (%)
            min_net_margin=5             # 최소 순이익률 (%)
        )
        
    def run(self, data: Dict[str, Any]) -> pd.DataFrame:
        """퀄리티 팩터 전략 실행
        
        Args:
            data: {
                "financial_data": 재무제표 데이터프레임,
                "current_prices": 현재가 데이터프레임
            }
            
        Returns:
            pd.DataFrame: 퀄리티 팩터 전략 결과
        """
        financial_data = data.get("financial_data", pd.DataFrame())
        current_prices = data.get("current_prices", pd.DataFrame())
        
        if financial_data.empty or current_prices.empty:
            return pd.DataFrame()
        
        # 필요한 지표들 계산
        if 'ROE' not in financial_data.columns:
            financial_data['ROE'] = financial_data.get('당기순이익', 0) / financial_data.get('자본총계', 1) * 100
            
        if 'ROA' not in financial_data.columns:
            financial_data['ROA'] = financial_data.get('당기순이익', 0) / financial_data.get('자산총계', 1) * 100
            
        if '부채비율' not in financial_data.columns:
            financial_data['부채비율'] = financial_data.get('부채총계', 0) / financial_data.get('자본총계', 1) * 100
            
        if '영업이익률' not in financial_data.columns:
            financial_data['영업이익률'] = financial_data.get('영업이익', 0) / financial_data.get('매출액', 1) * 100
            
        if '순이익률' not in financial_data.columns:
            financial_data['순이익률'] = financial_data.get('당기순이익', 0) / financial_data.get('매출액', 1) * 100
            
        if 'GP/A' not in financial_data.columns:
            financial_data['GP/A'] = financial_data.get('매출총이익', 0) / financial_data.get('자산총계', 1) * 100
            
        # 퀄리티 팩터 필터링
        quality_filter = (
            (financial_data['시가총액'] >= self.parameters['min_market_cap']) &
            (financial_data['ROE'] >= self.parameters['min_roe']) &
            (financial_data['ROA'] >= self.parameters['min_roa']) &
            (financial_data['부채비율'] <= self.parameters['max_debt_ratio']) &
            (financial_data['영업이익률'] >= self.parameters['min_operating_margin']) &
            (financial_data['순이익률'] >= self.parameters['min_net_margin'])
        )
        
        filtered_data = financial_data[quality_filter].copy()
        
        if filtered_data.empty:
            return pd.DataFrame()
        
        # 퀄리티 점수 계산
        # - ROE, ROA, 영업이익률, 순이익률, GP/A: 높을수록 좋음
        # - 부채비율: 낮을수록 좋음
        filtered_data['ROE_rank'] = filtered_data['ROE'].rank(ascending=False)
        filtered_data['ROA_rank'] = filtered_data['ROA'].rank(ascending=False)
        filtered_data['부채비율_rank'] = filtered_data['부채비율'].rank()
        filtered_data['영업이익률_rank'] = filtered_data['영업이익률'].rank(ascending=False)
        filtered_data['순이익률_rank'] = filtered_data['순이익률'].rank(ascending=False)
        filtered_data['GP/A_rank'] = filtered_data['GP/A'].rank(ascending=False)
        
        # 종합 점수 (가중치 적용 가능)
        filtered_data['quality_score'] = (
            filtered_data['ROE_rank'] +
            filtered_data['ROA_rank'] +
            filtered_data['부채비율_rank'] +
            filtered_data['영업이익률_rank'] +
            filtered_data['순이익률_rank'] +
            filtered_data['GP/A_rank']
        )
        
        # 점수 기준 정렬
        result = filtered_data.sort_values('quality_score')
        
        # 상위 N개 종목 선택
        if len(result) > self.parameters['n_stocks']:
            result = result.head(self.parameters['n_stocks'])
        
        # 현재가 정보 추가
        result = pd.merge(
            result,
            current_prices[['종목코드', '종목명', '현재가', '전일대비', '등락률']],
            on='종목코드',
            how='left'
        )
        
        # 필요한 컬럼만 선택
        display_columns = [
            '종목코드', '종목명_y', 'ROE', 'ROA', '부채비율', '영업이익률', '순이익률', 'GP/A',
            'quality_score', '현재가', '전일대비', '등락률'
        ]
        
        return result[display_columns]