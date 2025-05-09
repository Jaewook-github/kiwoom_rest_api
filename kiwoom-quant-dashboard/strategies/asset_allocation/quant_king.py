# strategies/asset_allocation/quant_king.py
from strategies.base import StrategyBase
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


class QuantKingAssetAllocation(StrategyBase):
    """퀀트킹 자산배분 전략"""
    
    def __init__(self):
        """퀀트킹 자산배분 전략 초기화"""
        super().__init__(
            name="Quant King Asset Allocation",
            description="시장 상황에 따른 동적 자산배분 전략"
        )
        self.set_parameters(
            momentum_period=12,           # 모멘텀 계산 기간(개월)
            volatility_lookback=20,       # 변동성 계산 기간(일)
            max_stock_allocation=60,      # 주식 최대 배분 비율(%)
            min_stock_allocation=20,      # 주식 최소 배분 비율(%)
            trend_period=200              # 추세 판단 기간(일)
        )
        
    def run(self, data: Dict[str, Any]) -> pd.DataFrame:
        """퀀트킹 자산배분 전략 실행
        
        Args:
            data: {
                "asset_data": {
                    "stock_index": 주식 지수 데이터,
                    "bond_index": 채권 지수 데이터,
                    "gold_index": 금 지수 데이터,
                    "cash_index": 현금(MMF) 지수 데이터
                }
            }
            
        Returns:
            pd.DataFrame: 자산배분 결과
        """
        asset_data = data.get("asset_data", {})
        
        # 필요한 모든 자산 데이터가 있는지 확인
        required_assets = ["stock_index", "bond_index", "gold_index", "cash_index"]
        for asset in required_assets:
            if asset not in asset_data or asset_data[asset].empty:
                return pd.DataFrame()
                
        # 각 자산별 데이터 추출
        stock_df = asset_data["stock_index"].copy()
        bond_df = asset_data["bond_index"].copy()
        gold_df = asset_data["gold_index"].copy()
        cash_df = asset_data["cash_index"].copy()
        
        # 날짜 기준으로 정렬
        for df in [stock_df, bond_df, gold_df, cash_df]:
            df.sort_values('일자', inplace=True)
            
        # 모멘텀 계산 기준일
        today = datetime.now()
        momentum_date = today - timedelta(days=self.parameters['momentum_period'] * 30)
        
        # 추세 판단 (이동평균선 활용)
        ma_long = stock_df['종가'].rolling(window=self.parameters['trend_period']).mean()
        stock_df['MA_long'] = ma_long
        
        # 상승 추세 여부 판단
        is_uptrend = stock_df['종가'].iloc[-1] > stock_df['MA_long'].iloc[-1]
        
        # 각 자산별 모멘텀 계산
        momentum_results = {}
        
        for asset_name, df in [
            ("주식", stock_df),
            ("채권", bond_df),
            ("금", gold_df),
            ("현금", cash_df)
        ]:
            # 모멘텀 기간 필터링
            df_momentum = df[df['일자'] >= momentum_date]
            
            if len(df_momentum) >= 2:
                recent_price = df_momentum['종가'].iloc[-1]
                past_price = df_momentum['종가'].iloc[0]
                momentum = (recent_price / past_price - 1) * 100
            else:
                momentum = 0
                
            # 변동성 계산
            if len(df) > self.parameters['volatility_lookback']:
                returns = df['종가'].pct_change().dropna()
                volatility = returns.tail(self.parameters['volatility_lookback']).std() * np.sqrt(252) * 100
            else:
                volatility = 0
                
            momentum_results[asset_name] = {
                "momentum": momentum,
                "volatility": volatility
            }
            
        # 모멘텀 기준 자산 순위
        sorted_momentum = sorted(
            momentum_results.items(),
            key=lambda x: x[1]["momentum"],
            reverse=True
        )
        
        # 자산 배분 로직
        allocation = {}
        
        # 기본 전략: 상위 2개 자산에 집중 투자
        if is_uptrend:
            # 상승 추세일 때
            # 주식 비중 계산: 변동성에 따라 조정
            stock_volatility = momentum_results["주식"]["volatility"]
            stock_allocation = max(
                self.parameters['min_stock_allocation'],
                min(
                    self.parameters['max_stock_allocation'],
                    self.parameters['max_stock_allocation'] - (stock_volatility - 15) * 2
                )
            )
            
            # 모멘텀 상위 2개 자산에 투자 (주식 제외)
            non_stock_assets = [item for item in sorted_momentum if item[0] != "주식"]
            top_assets = non_stock_assets[:2]
            
            allocation["주식"] = stock_allocation
            
            remaining = 100 - stock_allocation
            for i, (asset, _) in enumerate(top_assets):
                if i == 0:
                    allocation[asset] = remaining * 0.7  # 1등 자산에 70%
                else:
                    allocation[asset] = remaining * 0.3  # 2등 자산에 30%
                    
            # 누락된 자산은 0%로 설정
            for asset in ["주식", "채권", "금", "현금"]:
                if asset not in allocation:
                    allocation[asset] = 0
        else:
            # 하락 추세일 때 - 안전자산 중심 배분
            # 모멘텀 상위 2개 자산에 집중 투자
            top_assets = sorted_momentum[:2]
            
            for i, (asset, _) in enumerate(top_assets):
                if i == 0:
                    allocation[asset] = 60  # 1등 자산에 60%
                else:
                    allocation[asset] = 40  # 2등 자산에 40%
                    
            # 누락된 자산은 0%로 설정
            for asset in ["주식", "채권", "금", "현금"]:
                if asset not in allocation:
                    allocation[asset] = 0
                    
        # 결과 데이터프레임 생성
        result_data = []
        
        for asset, percent in allocation.items():
            result_data.append({
                "자산": asset,
                "배분비율": percent,
                "모멘텀": momentum_results[asset]["momentum"],
                "변동성": momentum_results[asset]["volatility"]
            })
            
        result_df = pd.DataFrame(result_data)
        
        # 추가 정보
        result_df["시장추세"] = "상승" if is_uptrend else "하락"
        result_df["기준일자"] = today.strftime("%Y-%m-%d")
        
        return result_df