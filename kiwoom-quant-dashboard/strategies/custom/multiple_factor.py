# strategies/custom/multiple_factor.py
from strategies.base import StrategyBase
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional


class MultipleFactorStrategy(StrategyBase):
    """다중 팩터 전략"""
    
    def __init__(self):
        """다중 팩터 전략 초기화"""
        super().__init__(
            name="Multiple Factor Strategy",
            description="여러 팩터를 조합한 사용자 정의 전략"
        )
        self.set_parameters(
            n_stocks=20,              # 선택할 종목 수
            min_market_cap=50000000000,  # 최소 시가총액 (500억)
            factors={                  # 사용할 팩터와 가중치
                "PER": {
                    "weight": 0.2,
                    "ascending": True      # True: 낮을수록 좋음
                },
                "PBR": {
                    "weight": 0.2,
                    "ascending": True
                },
                "ROE": {
                    "weight": 0.2,
                    "ascending": False     # False: 높을수록 좋음
                },
                "GP/A": {
                    "weight": 0.15,
                    "ascending": False
                },
                "모멘텀3개월": {
                    "weight": 0.15,
                    "ascending": False
                },
                "배당수익률": {
                    "weight": 0.1,
                    "ascending": False
                }
            }
        )
        
    def run(self, data: Dict[str, Any]) -> pd.DataFrame:
        """다중 팩터 전략 실행
        
        Args:
            data: {
                "financial_data": 재무제표 데이터프레임,
                "price_data": 종목별 가격 히스토리 딕셔너리,
                "current_prices": 현재가 데이터프레임
            }
            
        Returns:
            pd.DataFrame: 다중 팩터 순위 결과
        """
        financial_data = data.get("financial_data", pd.DataFrame())
        price_data = data.get("price_data", {})
        current_prices = data.get("current_prices", pd.DataFrame())
        
        if financial_data.empty or not price_data or current_prices.empty:
            return pd.DataFrame()
            
        # 필요한 팩터 계산
        result_df = financial_data.copy()
        
        # 모멘텀 계산 (3개월)
        momentum_list = []
        for code, df in price_data.items():
            if df.empty or len(df) < 60:  # 최소 60일 데이터 필요
                continue
                
            # 최근 가격과 3개월 전 가격
            recent_price = df['종가'].iloc[-1]
            past_price = df['종가'].iloc[-min(60, len(df))]
            
            momentum = (recent_price / past_price - 1) * 100
            
            momentum_list.append({
                '종목코드': code,
                '모멘텀3개월': momentum
            })
            
        momentum_df = pd.DataFrame(momentum_list)
        
        # 재무 데이터와 모멘텀 데이터 병합
        if not momentum_df.empty:
            result_df = pd.merge(result_df, momentum_df, on='종목코드', how='left')
            
        # 최소 시가총액 필터링
        result_df = result_df[result_df['시가총액'] >= self.parameters['min_market_cap']]
        
        if result_df.empty:
            return pd.DataFrame()
            
        # 각 팩터별 순위 계산
        factor_ranks = pd.DataFrame({'종목코드': result_df['종목코드']})
        
        for factor, config in self.parameters['factors'].items():
            if factor in result_df.columns:
                # 결측값 처리
                valid_data = result_df[['종목코드', factor]].dropna()
                
                if not valid_data.empty:
                    # 순위 계산 (ascending 설정에 따라 오름차순/내림차순)
                    ranks = valid_data[factor].rank(ascending=config['ascending'])
                    valid_data[f'{factor}_rank'] = ranks
                    
                    # 원본 데이터프레임에 순위 합치기
                    factor_ranks = pd.merge(
                        factor_ranks, 
                        valid_data[['종목코드', f'{factor}_rank']], 
                        on='종목코드', 
                        how='left'
                    )
        
        # 가중 평균 순위 계산
        weighted_rank = pd.Series(0, index=factor_ranks.index)
        total_weight = 0
        
        for factor, config in self.parameters['factors'].items():
            rank_col = f'{factor}_rank'
            if rank_col in factor_ranks.columns:
                weighted_rank += factor_ranks[rank_col] * config['weight']
                total_weight += config['weight']
                
        if total_weight > 0:
            factor_ranks['총점'] = weighted_rank / total_weight
        else:
            return pd.DataFrame()
            
        # 총점으로 정렬
        factor_ranks = factor_ranks.sort_values('총점')
        
        # 상위 N개 종목 선택
        if len(factor_ranks) > self.parameters['n_stocks']:
            top_n_codes = factor_ranks.head(self.parameters['n_stocks'])['종목코드'].tolist()
        else:
            top_n_codes = factor_ranks['종목코드'].tolist()
            
        # 최종 결과 데이터프레임 생성
        final_result = pd.merge(
            factor_ranks[factor_ranks['종목코드'].isin(top_n_codes)],
            result_df[['종목코드', '종목명'] + list(self.parameters['factors'].keys())],
            on='종목코드',
            how='left'
        )
        
        # 현재가 정보 추가
        final_result = pd.merge(
            final_result,
            current_prices[['종목코드', '현재가', '전일대비', '등락률']],
            on='종목코드',
            how='left'
        )
        
        # 정렬 및 컬럼 순서 조정
        final_result = final_result.sort_values('총점')
        
        column_order = ['종목코드', '종목명', '총점', '현재가', '전일대비', '등락률'] + \
                      list(self.parameters['factors'].keys()) + \
                      [f"{factor}_rank" for factor in self.parameters['factors'] if f"{factor}_rank" in final_result.columns]
                      
        return final_result[column_order]