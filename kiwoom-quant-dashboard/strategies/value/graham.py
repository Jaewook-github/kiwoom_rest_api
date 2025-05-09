# strategies/value/graham.py
from strategies.base import StrategyBase
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional


class Graham(StrategyBase):
    """벤자민 그레이엄의 가치투자 전략"""
    
    def __init__(self):
        """그레이엄 전략 초기화"""
        super().__init__(
            name="Graham Value Investing",
            description="벤자민 그레이엄의 기본 가치 투자 전략"
        )
        self.set_parameters(
            n_stocks=30,              # 선택할 종목 수
            min_market_cap=50000000000,  # 최소 시가총액 (500억)
            max_per=15,               # 최대 PER
            max_pbr=1.5,              # 최대 PBR
            min_dividend_yield=0.0,   # 최소 배당수익률
            min_current_ratio=2.0,    # 최소 유동비율
            max_debt_to_equity=0.5    # 최대 부채비율
        )
        
    def run(self, data: Dict[str, Any]) -> pd.DataFrame:
        """그레이엄 전략 실행
        
        Args:
            data: {
                "financial_data": 재무제표 데이터프레임,
                "current_prices": 현재가 데이터프레임
            }
            
        Returns:
            pd.DataFrame: 그레이엄 기준을 충족하는 종목
        """
        financial_data = data.get("financial_data", pd.DataFrame())
        current_prices = data.get("current_prices", pd.DataFrame())
        
        if financial_data.empty or current_prices.empty:
            return pd.DataFrame()
        
        # 필요한 컬럼들 확인 및 계산
        if 'PER' not in financial_data.columns:
            financial_data['PER'] = financial_data.get('시가총액', 0) / financial_data.get('당기순이익', 1)
            
        if 'PBR' not in financial_data.columns:
            financial_data['PBR'] = financial_data.get('시가총액', 0) / financial_data.get('자본총계', 1)
            
        if '유동비율' not in financial_data.columns:
            financial_data['유동비율'] = financial_data.get('유동자산', 0) / financial_data.get('유동부채', 1) * 100
            
        if '부채비율' not in financial_data.columns:
            financial_data['부채비율'] = financial_data.get('부채총계', 0) / financial_data.get('자본총계', 1) * 100
        
        # 그레이엄 기준에 따른 필터링
        graham_filter = (
            (financial_data['시가총액'] >= self.parameters['min_market_cap']) &
            (financial_data['PER'] <= self.parameters['max_per']) &
            (financial_data['PER'] > 0) &  # 적자 기업 제외
            (financial_data['PBR'] <= self.parameters['max_pbr']) &
            (financial_data['PBR'] > 0) &  # 자본잠식 기업 제외
            (financial_data['배당수익률'] >= self.parameters['min_dividend_yield']) &
            (financial_data['유동비율'] >= self.parameters['min_current_ratio'] * 100) &  # 100% 단위로 변환
            (financial_data['부채비율'] <= self.parameters['max_debt_to_equity'] * 100)  # 100% 단위로 변환
        )
        
        # 필터링된 결과
        filtered_data = financial_data[graham_filter].copy()
        
        if filtered_data.empty:
            return pd.DataFrame()
        
        # 종합 점수 계산
        # - PER과 PBR은 낮을수록 좋음
        # - 배당수익률과 유동비율은 높을수록 좋음
        # - 부채비율은 낮을수록 좋음
        filtered_data['PER_rank'] = filtered_data['PER'].rank()
        filtered_data['PBR_rank'] = filtered_data['PBR'].rank()
        filtered_data['배당수익률_rank'] = filtered_data['배당수익률'].rank(ascending=False)
        filtered_data['유동비율_rank'] = filtered_data['유동비율'].rank(ascending=False)
        filtered_data['부채비율_rank'] = filtered_data['부채비율'].rank()
        
        # 종합 점수
        filtered_data['graham_score'] = (
            filtered_data['PER_rank'] +
            filtered_data['PBR_rank'] +
            filtered_data['배당수익률_rank'] +
            filtered_data['유동비율_rank'] +
            filtered_data['부채비율_rank']
        )
        
        # 종합 점수로 정렬
        result = filtered_data.sort_values('graham_score')
        
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
            '종목코드', '종목명_y', 'PER', 'PBR', '배당수익률', '유동비율', '부채비율',
            'graham_score', '현재가', '전일대비', '등락률'
        ]
        
        return result[display_columns]