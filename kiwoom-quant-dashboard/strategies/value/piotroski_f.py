# strategies/value/piotroski_f.py
from strategies.base import StrategyBase
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional


class PiotroskiFScore(StrategyBase):
    """피오트로스키 F-Score 전략"""
    
    def __init__(self):
        """피오트로스키 F-Score 전략 초기화"""
        super().__init__(
            name="Piotroski F-Score",
            description="재무 상태가 개선되고 있는 저평가 가치주 선정"
        )
        self.set_parameters(
            n_stocks=20,          # 선택할 종목 수
            min_fscore=7,         # 최소 F-Score (0-9)
            max_pbr=1.0           # 최대 PBR
        )
        
    def run(self, data: Dict[str, Any]) -> pd.DataFrame:
        """피오트로스키 F-Score 전략 실행
        
        Args:
            data: {
                "financial_data": 재무제표 데이터프레임,
                "financial_data_prev": 이전 기간 재무제표 데이터프레임,
                "current_prices": 현재가 데이터프레임
            }
            
        Returns:
            pd.DataFrame: F-Score 결과
        """
        financial_data = data.get("financial_data", pd.DataFrame())
        financial_data_prev = data.get("financial_data_prev", pd.DataFrame())
        current_prices = data.get("current_prices", pd.DataFrame())
        
        if financial_data.empty or financial_data_prev.empty or current_prices.empty:
            return pd.DataFrame()
            
        # 종목별 F-Score 계산
        result_list = []
        
        for index, row in financial_data.iterrows():
            code = row.get('종목코드')
            
            # 이전 기간 데이터 확인
            prev_data = financial_data_prev[financial_data_prev['종목코드'] == code]
            if prev_data.empty:
                continue
                
            prev_row = prev_data.iloc[0]
            
            # F-Score 계산 (9가지 지표)
            f_score = 0
            criteria = {}
            
            # 1. 수익성 (Profitability)
            # 1.1 ROA > 0
            roa = row.get('당기순이익', 0) / row.get('자산총계', 1)
            criteria['ROA > 0'] = roa > 0
            f_score += 1 if criteria['ROA > 0'] else 0
            
            # 1.2 영업현금흐름 > 0
            ocf = row.get('영업현금흐름', 0)
            criteria['OCF > 0'] = ocf > 0
            f_score += 1 if criteria['OCF > 0'] else 0
            
            # 1.3 ROA 증가
            prev_roa = prev_row.get('당기순이익', 0) / prev_row.get('자산총계', 1)
            criteria['ROA 증가'] = roa > prev_roa
            f_score += 1 if criteria['ROA 증가'] else 0
            
            # 1.4 OCF > ROA
            criteria['OCF > ROA'] = ocf / row.get('자산총계', 1) > roa
            f_score += 1 if criteria['OCF > ROA'] else 0
            
            # 2. 레버리지, 유동성, 자금조달원천 (Leverage, Liquidity and Source of Funds)
            # 2.1 장기부채 비율 감소
            lt_debt_ratio = row.get('비유동부채', 0) / row.get('자산총계', 1)
            prev_lt_debt_ratio = prev_row.get('비유동부채', 0) / prev_row.get('자산총계', 1)
            criteria['LTDebt 감소'] = lt_debt_ratio < prev_lt_debt_ratio
            f_score += 1 if criteria['LTDebt 감소'] else 0
            
            # 2.2 유동비율 증가
            current_ratio = row.get('유동자산', 0) / max(row.get('유동부채', 1), 1)
            prev_current_ratio = prev_row.get('유동자산', 0) / max(prev_row.get('유동부채', 1), 1)
            criteria['유동비율 증가'] = current_ratio > prev_current_ratio
            f_score += 1 if criteria['유동비율 증가'] else 0
            
            # 2.3 신주발행 없음
            shares_now = row.get('발행주식수', 0)
            shares_prev = prev_row.get('발행주식수', 0)
            criteria['신주발행 없음'] = shares_now <= shares_prev
            f_score += 1 if criteria['신주발행 없음'] else 0
            
            # 3. 운영효율성 (Operating Efficiency)
            # 3.1 매출총이익률 증가
            gross_margin = row.get('매출총이익', 0) / max(row.get('매출액', 1), 1)
            prev_gross_margin = prev_row.get('매출총이익', 0) / max(prev_row.get('매출액', 1), 1)
            criteria['매출총이익률 증가'] = gross_margin > prev_gross_margin
            f_score += 1 if criteria['매출총이익률 증가'] else 0
            
            # 3.2 자산회전율 증가
            asset_turnover = row.get('매출액', 0) / row.get('자산총계', 1)
            prev_asset_turnover = prev_row.get('매출액', 0) / prev_row.get('자산총계', 1)
            criteria['자산회전율 증가'] = asset_turnover > prev_asset_turnover
            f_score += 1 if criteria['자산회전율 증가'] else 0
            
            # PBR 계산
            pbr = row.get('PBR', row.get('시가총액', 0) / max(row.get('자본총계', 1), 1))
            
            # 결과 저장
            result_list.append({
                '종목코드': code,
                '종목명': row.get('종목명', code),
                'F-Score': f_score,
                'PBR': pbr,
                'ROA': roa * 100,  # 백분율로 변환
                '당기순이익': row.get('당기순이익', 0),
                '영업현금흐름': ocf,
                '자산총계': row.get('자산총계', 0)
            })
            
        # 데이터프레임으로 변환
        result_df = pd.DataFrame(result_list)
        
        if result_df.empty:
            return pd.DataFrame()
            
        # 필터링: F-Score >= min_fscore, PBR <= max_pbr
        result_df = result_df[
            (result_df['F-Score'] >= self.parameters['min_fscore']) & 
            (result_df['PBR'] <= self.parameters['max_pbr'])
        ]
        
        # F-Score 내림차순, PBR 오름차순 정렬
        result_df = result_df.sort_values(['F-Score', 'PBR'], ascending=[False, True])
        
        # 상위 N개 종목 선택
        if len(result_df) > self.parameters['n_stocks']:
            result_df = result_df.head(self.parameters['n_stocks'])
            
        # 현재가 정보 추가
        result_df = pd.merge(
            result_df,
            current_prices[['종목코드', '현재가', '전일대비', '등락률']],
            on='종목코드',
            how='left'
        )
        
        return result_df