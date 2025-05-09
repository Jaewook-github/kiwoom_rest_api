"""
계좌 관련 데이터 모델 클래스
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, date
import pandas as pd


@dataclass
class Position:
    """보유 종목 데이터 클래스"""
    
    code: str
    name: str
    quantity: int
    purchase_price: float
    current_price: float
    
    @property
    def evaluation_amount(self) -> float:
        """평가금액
        
        Returns:
            float: 평가금액
        """
        return self.current_price * self.quantity
    
    @property
    def purchase_amount(self) -> float:
        """매입금액
        
        Returns:
            float: 매입금액
        """
        return self.purchase_price * self.quantity
    
    @property
    def profit_loss(self) -> float:
        """손익금액
        
        Returns:
            float: 손익금액
        """
        return self.evaluation_amount - self.purchase_amount
    
    @property
    def profit_loss_rate(self) -> float:
        """손익률
        
        Returns:
            float: 손익률 (%)
        """
        if self.purchase_amount == 0:
            return 0.0
            
        return (self.profit_loss / self.purchase_amount) * 100
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Position':
        """딕셔너리에서 Position 객체 생성
        
        Args:
            data: 보유 종목 딕셔너리
            
        Returns:
            Position: 보유 종목 객체
        """
        return cls(
            code=data.get('종목코드', ''),
            name=data.get('종목명', ''),
            quantity=int(data.get('보유수량', 0)),
            purchase_price=float(data.get('매입가', 0)),
            current_price=float(data.get('현재가', 0))
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Position 객체를 딕셔너리로 변환
        
        Returns:
            Dict[str, Any]: 보유 종목 딕셔너리
        """
        return {
            '종목코드': self.code,
            '종목명': self.name,
            '보유수량': self.quantity,
            '매입가': self.purchase_price,
            '현재가': self.current_price,
            '평가금액': self.evaluation_amount,
            '매입금액': self.purchase_amount,
            '손익금액': self.profit_loss,
            '손익률': self.profit_loss_rate
        }


@dataclass
class Order:
    """주문 데이터 클래스"""
    
    order_no: str
    code: str
    name: str
    order_type: str  # '매수' or '매도'
    order_price: float
    order_quantity: int
    executed_price: float = 0.0
    executed_quantity: int = 0
    order_status: str = '접수'  # '접수', '체결', '취소', '정정'
    order_time: datetime = field(default_factory=datetime.now)
    
    @property
    def order_amount(self) -> float:
        """주문금액
        
        Returns:
            float: 주문금액
        """
        return self.order_price * self.order_quantity
    
    @property
    def executed_amount(self) -> float:
        """체결금액
        
        Returns:
            float: 체결금액
        """
        return self.executed_price * self.executed_quantity
    
    @property
    def is_filled(self) -> bool:
        """체결 완료 여부
        
        Returns:
            bool: 체결 완료 여부
        """
        return self.order_status == '체결' and self.executed_quantity == self.order_quantity
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Order':
        """딕셔너리에서 Order 객체 생성
        
        Args:
            data: 주문 데이터 딕셔너리
            
        Returns:
            Order: 주문 데이터 객체
        """
        # 주문시간 변환
        order_time = datetime.now()
        if '주문시간' in data:
            try:
                order_time = pd.to_datetime(data['주문시간'])
            except:
                pass
                
        return cls(
            order_no=str(data.get('주문번호', '')),
            code=data.get('종목코드', ''),
            name=data.get('종목명', ''),
            order_type=data.get('주문구분', ''),
            order_price=float(data.get('주문가격', 0)),
            order_quantity=int(data.get('주문수량', 0)),
            executed_price=float(data.get('체결가격', 0)),
            executed_quantity=int(data.get('체결수량', 0)),
            order_status=data.get('주문상태', '접수'),
            order_time=order_time
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Order 객체를 딕셔너리로 변환
        
        Returns:
            Dict[str, Any]: 주문 데이터 딕셔너리
        """
        return {
            '주문번호': self.order_no,
            '종목코드': self.code,
            '종목명': self.name,
            '주문구분': self.order_type,
            '주문가격': self.order_price,
            '주문수량': self.order_quantity,
            '체결가격': self.executed_price,
            '체결수량': self.executed_quantity,
            '주문상태': self.order_status,
            '주문시간': self.order_time.strftime('%Y%m%d%H%M%S'),
            '주문금액': self.order_amount,
            '체결금액': self.executed_amount
        }


@dataclass
class Account:
    """계좌 데이터 클래스"""
    
    account_no: str
    account_name: str
    balance: float = 0.0  # 예수금
    total_purchase_amount: float = 0.0  # 총매입금액
    total_evaluation_amount: float = 0.0  # 총평가금액
    total_profit_loss: float = 0.0  # 총손익금액
    positions: List[Position] = field(default_factory=list)  # 보유종목 리스트
    orders: List[Order] = field(default_factory=list)  # 주문 리스트
    
    @property
    def total_asset(self) -> float:
        """총자산
        
        Returns:
            float: 총자산
        """
        return self.balance + self.total_evaluation_amount
    
    @property
    def profit_loss_rate(self) -> float:
        """손익률
        
        Returns:
            float: 손익률 (%)
        """
        if self.total_purchase_amount == 0:
            return 0.0
            
        return (self.total_profit_loss / self.total_purchase_amount) * 100
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Account':
        """딕셔너리에서 Account 객체 생성
        
        Args:
            data: 계좌 데이터 딕셔너리
            
        Returns:
            Account: 계좌 데이터 객체
        """
        account = cls(
            account_no=data.get('계좌번호', ''),
            account_name=data.get('계좌명', ''),
            balance=float(data.get('예수금', 0)),
            total_purchase_amount=float(data.get('총매입금액', 0)),
            total_evaluation_amount=float(data.get('총평가금액', 0)),
            total_profit_loss=float(data.get('총손익금액', 0))
        )
        
        # 보유종목 추가
        if 'positions' in data and isinstance(data['positions'], list):
            for pos_data in data['positions']:
                account.add_position(Position.from_dict(pos_data))
                
        # 주문 추가
        if 'orders' in data and isinstance(data['orders'], list):
            for order_data in data['orders']:
                account.add_order(Order.from_dict(order_data))
                
        return account
    
    def to_dict(self) -> Dict[str, Any]:
        """Account 객체를 딕셔너리로 변환
        
        Returns:
            Dict[str, Any]: 계좌 데이터 딕셔너리
        """
        return {
            '계좌번호': self.account_no,
            '계좌명': self.account_name,
            '예수금': self.balance,
            '총매입금액': self.total_purchase_amount,
            '총평가금액': self.total_evaluation_amount,
            '총손익금액': self.total_profit_loss,
            '총자산': self.total_asset,
            '손익률': self.profit_loss_rate,
            'positions': [pos.to_dict() for pos in self.positions],
            'orders': [order.to_dict() for order in self.orders]
        }
    
    def add_position(self, position: Position):
        """보유종목 추가
        
        Args:
            position: 추가할 보유종목
        """
        # 기존 보유종목인 경우 업데이트
        for pos in self.positions:
            if pos.code == position.code:
                pos.quantity = position.quantity
                pos.purchase_price = position.purchase_price
                pos.current_price = position.current_price
                return
        
        # 새로운 보유종목 추가
        self.positions.append(position)
        
    def add_order(self, order: Order):
        """주문 추가
        
        Args:
            order: 추가할 주문
        """
        # 기존 주문인 경우 업데이트
        for ord in self.orders:
            if ord.order_no == order.order_no:
                ord.order_status = order.order_status
                ord.executed_price = order.executed_price
                ord.executed_quantity = order.executed_quantity
                return
        
        # 새로운 주문 추가
        self.orders.append(order)
        