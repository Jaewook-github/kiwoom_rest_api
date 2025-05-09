# strategies/base.py
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional


class StrategyBase(ABC):
    """퀀트 전략 기본 클래스"""
    
    def __init__(self, name: str, description: str):
        """전략 초기화
        
        Args:
            name: 전략 이름
            description: 전략 설명
        """
        self.name = name
        self.description = description
        self.parameters = {}
        
    def set_parameters(self, **kwargs) -> None:
        """전략 파라미터 설정
        
        Args:
            **kwargs: 전략 파라미터
        """
        self.parameters.update(kwargs)
        
    @abstractmethod
    def run(self, data: Dict[str, Any]) -> pd.DataFrame:
        """전략 실행
        
        Args:
            data: 전략 실행에 필요한 데이터
            
        Returns:
            pd.DataFrame: 전략 실행 결과
        """
        pass
    
    def evaluate(self, result: pd.DataFrame) -> Dict[str, Any]:
        """전략 평가
        
        Args:
            result: 전략 실행 결과
            
        Returns:
            Dict[str, Any]: 평가 지표
        """
        return {
            "strategy_name": self.name,
            "parameters": self.parameters
        }