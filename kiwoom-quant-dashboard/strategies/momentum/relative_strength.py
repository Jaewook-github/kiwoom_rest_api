# strategies/momentum/relative_strength.py
from strategies.base import StrategyBase
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


class RelativeStrengthStrategy(StrategyBase):
    """상대 강도 전략"""
    
    def __init__(self):
        """상대 강도 전략 초기화"""
        super().__init__(
            name="Relative Strength Strategy",
            description="상대 강도 지수(RSI)를 활용한 모멘텀 전략"
        )
        self.set_parameters(
            n_stocks=20,              # 선택할 종목 수
            rsi_period=14,            # RSI 계산 기간
            rsi_upper=70,             # RSI 상단 기준
            rsi_lower=30,             # RSI 하단 기준
            lookback_period=6         # 모멘텀 계산 기간(개월)
        )
        
    def run(self, data: Dict[str, Any]) -> pd.DataFrame:
        """상대 강도 전략 실행
        
        Args:
            data: {
                "price_data": 종목별 가격 히스토리 딕셔너리,
                "current_prices": 현재가 데이터프레임
            }
            
        Returns:
            pd.DataFrame: 상대 강도 전략 결과
        """
        price_data = data.get("price_data", {})
        current_prices = data.get("current_prices", pd.DataFrame())
        
        if not price_data or current_prices.empty:
            return pd.DataFrame()
        
        # 결과를 저장할 리스트
        results = []
        
        # 모멘텀 계산 기준일
        today = datetime.now()
        lookback_date = today - timedelta(days=self.parameters['lookback_period'] * 30)
        
        # 각 종목별로 RSI 및 모멘텀 계산
        for code, df in price_data.items():
            if df.empty or len(df) < self.parameters['rsi_period'] * 2:
                continue
                
            # 날짜 필터링
            df = df.sort_values('일자')
            df_recent = df[df['일자'] >= lookback_date]
            
            if len(df_recent) < 2:
                continue
                
            # RSI 계산
            delta = df['종가'].diff()
            gain = delta.mask(delta < 0, 0)
            loss = -delta.mask(delta > 0, 0)
            
            avg_gain = gain.rolling(window=self.parameters['rsi_period']).mean()
            avg_loss = loss.rolling(window=self.parameters['rsi_period']).mean()
            
            rs = avg_gain / avg_loss.abs()
            rsi = 100 - (100 / (1 + rs))
            
            current_rsi = rsi.iloc[-1]
            
            # 모멘텀 계산
            recent_price = df_recent['종가'].iloc[-1]
            past_price = df_recent['종가'].iloc[0]
            momentum = (recent_price / past_price - 1) * 100
            
            # 가격 변동성 계산
            price_std = df_recent['종가'].pct_change().std() * 100
            
            # 결과 저장
            results.append({
                '종목코드': code,
                '종목명': df.get('종목명', [code]).iloc[0] if '종목명' in df.columns else code,
                'RSI': current_rsi,
                '모멘텀': momentum,
                '변동성': price_std,
                '현재가': recent_price
            })
            
        # 데이터프레임으로 변환
        result_df = pd.DataFrame(results)
        
        if result_df.empty:
            return pd.DataFrame()
            
        # RSI 구간에 따른 종목 필터링
        if self.parameters['rsi_upper'] and self.parameters['rsi_lower']:
            # 과매수/과매도 구간 모두 필터링
            result_df = result_df[
                (result_df['RSI'] >= self.parameters['rsi_upper']) | 
                (result_df['RSI'] <= self.parameters['rsi_lower'])
            ]
            
            # 과매수/과매도 구분
            result_df['상태'] = '중립'
            result_df.loc[result_df['RSI'] >= self.parameters['rsi_upper'], '상태'] = '과매수'
            result_df.loc[result_df['RSI'] <= self.parameters['rsi_lower'], '상태'] = '과매도'
        
        # 모멘텀 기준 내림차순 정렬
        result_df = result_df.sort_values('모멘텀', ascending=False)
        
        # 상위 N개 종목 선택
        if len(result_df) > self.parameters['n_stocks']:
            result_df = result_df.head(self.parameters['n_stocks'])
            
        # 현재가 정보 추가
        result_df = pd.merge(
            result_df,
            current_prices[['종목코드', '전일대비', '등락률']],
            on='종목코드',
            how='left'
        )
        
        return result_df