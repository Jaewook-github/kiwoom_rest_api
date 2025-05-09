"""
시장 데이터 모델 클래스
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, date
import pandas as pd


@dataclass
class MarketIndex:
    """시장 지수 데이터 클래스"""
    
    code: str
    name: str
    date: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int = 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarketIndex':
        """딕셔너리에서 MarketIndex 객체 생성
        
        Args:
            data: 시장 지수 딕셔너리
            
        Returns:
            MarketIndex: 시장 지수 객체
        """
        return cls(
            code=data.get('지수코드', ''),
            name=data.get('지수명', ''),
            date=pd.to_datetime(data.get('일자')),
            open_price=float(data.get('시가', 0)),
            high_price=float(data.get('고가', 0)),
            low_price=float(data.get('저가', 0)),
            close_price=float(data.get('종가', 0)),
            volume=int(data.get('거래량', 0))
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """MarketIndex 객체를 딕셔너리로 변환
        
        Returns:
            Dict[str, Any]: 시장 지수 딕셔너리
        """
        return {
            '지수코드': self.code,
            '지수명': self.name,
            '일자': self.date.strftime('%Y%m%d'),
            '시가': self.open_price,
            '고가': self.high_price,
            '저가': self.low_price,
            '종가': self.close_price,
            '거래량': self.volume
        }


@dataclass
class MarketSector:
    """업종 데이터 클래스"""
    
    code: str
    name: str
    date: datetime
    change_rate: float = 0.0
    volume: int = 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarketSector':
        """딕셔너리에서 MarketSector 객체 생성
        
        Args:
            data: 업종 데이터 딕셔너리
            
        Returns:
            MarketSector: 업종 데이터 객체
        """
        return cls(
            code=data.get('업종코드', ''),
            name=data.get('업종명', ''),
            date=pd.to_datetime(data.get('일자')),
            change_rate=float(data.get('등락률', 0)),
            volume=int(data.get('거래량', 0))
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """MarketSector 객체를 딕셔너리로 변환
        
        Returns:
            Dict[str, Any]: 업종 데이터 딕셔너리
        """
        return {
            '업종코드': self.code,
            '업종명': self.name,
            '일자': self.date.strftime('%Y%m%d'),
            '등락률': self.change_rate,
            '거래량': self.volume
        }


@dataclass
class MarketStatus:
    """시장 상태 데이터 클래스"""
    
    date: datetime
    market_type: str  # 'KOSPI', 'KOSDAQ', 'KONEX'
    status: str  # '장전', '장중', '장후', '장종료'
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarketStatus':
        """딕셔너리에서 MarketStatus 객체 생성
        
        Args:
            data: 시장 상태 딕셔너리
            
        Returns:
            MarketStatus: 시장 상태 객체
        """
        return cls(
            date=pd.to_datetime(data.get('일자')),
            market_type=data.get('시장구분', ''),
            status=data.get('장상태', '')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """MarketStatus 객체를 딕셔너리로 변환
        
        Returns:
            Dict[str, Any]: 시장 상태 딕셔너리
        """
        return {
            '일자': self.date.strftime('%Y%m%d'),
            '시장구분': self.market_type,
            '장상태': self.status
        }


@dataclass
class Market:
    """시장 데이터 클래스"""
    
    market_type: str  # 'KOSPI', 'KOSDAQ', 'KONEX'
    date: datetime
    
    # 시장 지수
    index_value: float = 0.0
    index_change: float = 0.0
    index_change_rate: float = 0.0
    
    # 시장 거래 정보
    volume: int = 0
    trading_value: int = 0
    up_count: int = 0
    down_count: int = 0
    unchanged_count: int = 0
    
    # 투자자별 순매수 (백만원)
    individual_netbuy: int = 0
    foreign_netbuy: int = 0
    institution_netbuy: int = 0
    
    # 섹터 정보
    sectors: List[MarketSector] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Market':
        """딕셔너리에서 Market 객체 생성
        
        Args:
            data: 시장 데이터 딕셔너리
            
        Returns:
            Market: 시장 데이터 객체
        """
        return cls(
            market_type=data.get('시장구분', ''),
            date=pd.to_datetime(data.get('일자')),
            index_value=float(data.get('지수', 0)),
            index_change=float(data.get('전일대비', 0)),
            index_change_rate=float(data.get('등락률', 0)),
            volume=int(data.get('거래량', 0)),
            trading_value=int(data.get('거래대금', 0)),
            up_count=int(data.get('상승종목수', 0)),
            down_count=int(data.get('하락종목수', 0)),
            unchanged_count=int(data.get('보합종목수', 0)),
            individual_netbuy=int(data.get('개인순매수', 0)),
            foreign_netbuy=int(data.get('외국인순매수', 0)),
            institution_netbuy=int(data.get('기관순매수', 0))
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Market 객체를 딕셔너리로 변환
        
        Returns:
            Dict[str, Any]: 시장 데이터 딕셔너리
        """
        return {
            '시장구분': self.market_type,
            '일자': self.date.strftime('%Y%m%d'),
            '지수': self.index_value,
            '전일대비': self.index_change,
            '등락률': self.index_change_rate,
            '거래량': self.volume,
            '거래대금': self.trading_value,
            '상승종목수': self.up_count,
            '하락종목수': self.down_count,
            '보합종목수': self.unchanged_count,
            '개인순매수': self.individual_netbuy,
            '외국인순매수': self.foreign_netbuy,
            '기관순매수': self.institution_netbuy
        }
    
    def add_sector(self, sector: MarketSector):
        """업종 데이터 추가
        
        Args:
            sector: 추가할 업종 데이터
        """
        self.sectors.append(sector)
        
    def get_sectors_as_dataframe(self) -> pd.DataFrame:
        """업종 데이터를 데이터프레임으로 변환
        
        Returns:
            pd.DataFrame: 업종 데이터프레임
        """
        if not self.sectors:
            return pd.DataFrame()
        
        data = [sector.to_dict() for sector in self.sectors]
        df = pd.DataFrame(data)
        
        return df
    
    def get_advance_decline_ratio(self) -> float:
        """등락비율 계산
        
        Returns:
            float: 등락비율 (상승종목수 / 하락종목수)
        """
        if self.down_count == 0:
            return float('inf')
            
        return self.up_count / self.down_count