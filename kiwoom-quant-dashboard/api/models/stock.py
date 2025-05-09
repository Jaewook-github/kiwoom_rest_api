"""
주식 데이터 모델 클래스
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, date
import pandas as pd


@dataclass
class StockPrice:
    """주가 정보 데이터 클래스"""
    
    date: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StockPrice':
        """딕셔너리에서 StockPrice 객체 생성
        
        Args:
            data: 주가 정보 딕셔너리
            
        Returns:
            StockPrice: 주가 정보 객체
        """
        return cls(
            date=pd.to_datetime(data.get('일자')),
            open_price=float(data.get('시가', 0)),
            high_price=float(data.get('고가', 0)),
            low_price=float(data.get('저가', 0)),
            close_price=float(data.get('종가', 0)),
            volume=int(data.get('거래량', 0))
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """StockPrice 객체를 딕셔너리로 변환
        
        Returns:
            Dict[str, Any]: 주가 정보 딕셔너리
        """
        return {
            '일자': self.date.strftime('%Y%m%d'),
            '시가': self.open_price,
            '고가': self.high_price,
            '저가': self.low_price,
            '종가': self.close_price,
            '거래량': self.volume
        }


@dataclass
class Stock:
    """종목 데이터 클래스"""
    
    code: str
    name: str
    market_type: str = ""
    sector: str = ""
    industry: str = ""
    listing_date: Optional[date] = None
    settlement_month: str = ""
    capital: int = 0
    par_value: int = 0
    
    # 실시간 정보
    current_price: float = 0
    price_change: float = 0
    change_rate: float = 0
    volume: int = 0
    trading_value: int = 0
    
    # 가격 히스토리
    prices: List[StockPrice] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Stock':
        """딕셔너리에서 Stock 객체 생성
        
        Args:
            data: 종목 정보 딕셔너리
            
        Returns:
            Stock: 종목 객체
        """
        listing_date = None
        if '상장일' in data and data['상장일']:
            try:
                listing_date = datetime.strptime(str(data['상장일']), '%Y%m%d').date()
            except:
                pass
            
        return cls(
            code=data.get('종목코드', ''),
            name=data.get('종목명', ''),
            market_type=data.get('시장구분', ''),
            sector=data.get('섹터', ''),
            industry=data.get('산업군', ''),
            listing_date=listing_date,
            settlement_month=data.get('결산월', ''),
            capital=int(data.get('자본금', 0)),
            par_value=int(data.get('액면가', 0)),
            current_price=float(data.get('현재가', 0)),
            price_change=float(data.get('전일대비', 0)),
            change_rate=float(data.get('등락률', 0)),
            volume=int(data.get('거래량', 0)),
            trading_value=int(data.get('거래대금', 0))
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Stock 객체를 딕셔너리로 변환
        
        Returns:
            Dict[str, Any]: 종목 정보 딕셔너리
        """
        listing_date_str = None
        if self.listing_date:
            listing_date_str = self.listing_date.strftime('%Y%m%d')
            
        return {
            '종목코드': self.code,
            '종목명': self.name,
            '시장구분': self.market_type,
            '섹터': self.sector,
            '산업군': self.industry,
            '상장일': listing_date_str,
            '결산월': self.settlement_month,
            '자본금': self.capital,
            '액면가': self.par_value,
            '현재가': self.current_price,
            '전일대비': self.price_change,
            '등락률': self.change_rate,
            '거래량': self.volume,
            '거래대금': self.trading_value
        }
    
    def add_price(self, price: StockPrice):
        """가격 데이터 추가
        
        Args:
            price: 추가할 가격 데이터
        """
        self.prices.append(price)
        
    def get_prices_as_dataframe(self) -> pd.DataFrame:
        """가격 데이터를 데이터프레임으로 변환
        
        Returns:
            pd.DataFrame: 가격 데이터프레임
        """
        if not self.prices:
            return pd.DataFrame()
        
        data = [price.to_dict() for price in self.prices]
        df = pd.DataFrame(data)
        
        if not df.empty and '일자' in df.columns:
            df['일자'] = pd.to_datetime(df['일자'])
            df = df.sort_values('일자')
            
        return df
    
    def calculate_returns(self, period: int = 1) -> float:
        """일정 기간 수익률 계산
        
        Args:
            period: 기간 (일)
            
        Returns:
            float: 수익률
        """
        if not self.prices or len(self.prices) <= period:
            return 0.0
        
        # 가격 데이터 정렬
        sorted_prices = sorted(self.prices, key=lambda x: x.date)
        
        # 현재가와 기간 전 가격
        current_price = sorted_prices[-1].close_price
        past_price = sorted_prices[-period-1].close_price if period < len(sorted_prices) else sorted_prices[0].close_price
        
        if past_price == 0:
            return 0.0
            
        return (current_price / past_price - 1) * 100


@dataclass
class StockIndicator:
    """주식 지표 데이터 클래스"""
    
    code: str
    name: str
    date: datetime
    
    # 투자 지표
    per: float = 0.0
    pbr: float = 0.0
    pcr: float = 0.0
    psr: float = 0.0
    eps: float = 0.0
    bps: float = 0.0
    roe: float = 0.0
    dividend_yield: float = 0.0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StockIndicator':
        """딕셔너리에서 StockIndicator 객체 생성
        
        Args:
            data: 주식 지표 딕셔너리
            
        Returns:
            StockIndicator: 주식 지표 객체
        """
        return cls(
            code=data.get('종목코드', ''),
            name=data.get('종목명', ''),
            date=pd.to_datetime(data.get('기준일', datetime.now().strftime('%Y%m%d'))),
            per=float(data.get('PER', 0)),
            pbr=float(data.get('PBR', 0)),
            pcr=float(data.get('PCR', 0)),
            psr=float(data.get('PSR', 0)),
            eps=float(data.get('EPS', 0)),
            bps=float(data.get('BPS', 0)),
            roe=float(data.get('ROE', 0)),
            dividend_yield=float(data.get('배당수익률', 0))
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """StockIndicator 객체를 딕셔너리로 변환
        
        Returns:
            Dict[str, Any]: 주식 지표 딕셔너리
        """
        return {
            '종목코드': self.code,
            '종목명': self.name,
            '기준일': self.date.strftime('%Y%m%d'),
            'PER': self.per,
            'PBR': self.pbr,
            'PCR': self.pcr,
            'PSR': self.psr,
            'EPS': self.eps,
            'BPS': self.bps,
            'ROE': self.roe,
            '배당수익률': self.dividend_yield
        }