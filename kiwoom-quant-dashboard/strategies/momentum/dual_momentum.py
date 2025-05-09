"""
키움증권 REST API 퀀트 대시보드 프로젝트의 퀀트 투자 전략 모듈
"""

# strategies/momentum/dual_momentum.py
from strategies.base import StrategyBase
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


class DualMomentumStrategy(StrategyBase):
    """듀얼 모멘텀 전략"""
    
    def __init__(self):
        """듀얼 모멘텀 전략 초기화"""
        super().__init__(
            name="Dual Momentum Strategy",
            description="절대 모멘텀과 상대 모멘텀을 결합한 전략"
        )
        self.set_parameters(
            n_stocks=10,              # 선택할 종목 수
            lookback_period=12,       # 모멘텀 계산 기간(개월)
            market_index="KS11",      # 비교 시장 지수
            absolute_threshold=0.0    # 절대 모멘텀 임계값
        )
        
    def run(self, data: Dict[str, Any]) -> pd.DataFrame:
        """듀얼 모멘텀 전략 실행
        
        Args:
            data: {
                "price_data": 종목별 가격 히스토리 딕셔너리,
                "index_data": 시장 지수 가격 히스토리
            }
            
        Returns:
            pd.DataFrame: 듀얼 모멘텀 순위 결과
        """
        price_data = data.get("price_data", {})
        index_data = data.get("index_data", pd.DataFrame())
        
        if not price_data or index_data.empty:
            return pd.DataFrame()
        
        # 결과를 저장할 리스트
        momentum_list = []
        
        # 모멘텀 계산 기준일
        today = datetime.now()
        lookback_date = today - timedelta(days=self.parameters['lookback_period'] * 30)
        
        # 모든 종목에 대해 모멘텀 계산
        for code, df in price_data.items():
            if df.empty:
                continue
                
            # 날짜 필터링 (종목별 가격 데이터가 다를 수 있음)
            df = df[df['일자'] >= lookback_date]
            
            if len(df) < 2:  # 최소 2개 이상의 데이터가 필요
                continue
                
            # 가장 최근 종가와 lookback_period 이전 종가 추출
            recent_price = df['종가'].iloc[-1]
            past_price = df['종가'].iloc[0]
            
            # 상대 모멘텀 (최근 N개월 수익률) 계산
            relative_momentum = (recent_price / past_price - 1) * 100
            
            # 종목 정보 저장
            momentum_list.append({
                '종목코드': code,
                '종목명': df.get('종목명', [code]).iloc[0] if '종목명' in df.columns else code,
                '상대모멘텀': relative_momentum,
                '현재가': recent_price
            })
            
        # 데이터프레임으로 변환
        momentum_df = pd.DataFrame(momentum_list)
        
        if momentum_df.empty:
            return pd.DataFrame()
        
        # 시장 지수의 모멘텀 계산
        index_df = index_data[index_data['일자'] >= lookback_date]
        
        if len(index_df) >= 2:
            recent_index = index_df['종가'].iloc[-1]
            past_index = index_df['종가'].iloc[0]
            market_momentum = (recent_index / past_index - 1) * 100
        else:
            market_momentum = 0
            
        # 절대 모멘텀 필터링: 시장 수익률보다 높고, 임계값보다 높은 종목만 선택
        momentum_df = momentum_df[
            (momentum_df['상대모멘텀'] > market_momentum) & 
            (momentum_df['상대모멘텀'] > self.parameters['absolute_threshold'])
        ]
        
        # 상대 모멘텀 기준으로 정렬
        momentum_df = momentum_df.sort_values('상대모멘텀', ascending=False)
        
        # 상위 N개 종목 선택
        if len(momentum_df) > self.parameters['n_stocks']:
            momentum_df = momentum_df.head(self.parameters['n_stocks'])
            
        # 필요한 정보 추가
        momentum_df['시장모멘텀'] = market_momentum
        momentum_df['초과수익률'] = momentum_df['상대모멘텀'] - market_momentum
        
        return momentum_df