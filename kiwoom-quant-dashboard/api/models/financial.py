# api/models/financial.py
from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Union
from datetime import datetime


@dataclass
class FinancialStatement:
    """재무제표 데이터 모델"""
    code: str
    name: str
    fiscal_year: str
    fiscal_quarter: str
    revenue: float
    operating_profit: float
    net_income: float
    eps: float
    bps: float
    roe: float
    debt_ratio: float
    quick_ratio: float
    reserve_ratio: float
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FinancialStatement':
        """딕셔너리에서 재무제표 객체 생성
        
        Args:
            data: API 응답 데이터
            
        Returns:
            FinancialStatement: 재무제표 객체
        """
        return cls(
            code=data.get('code', ''),
            name=data.get('name', ''),
            fiscal_year=data.get('fiscal_year', ''),
            fiscal_quarter=data.get('fiscal_quarter', ''),
            revenue=float(data.get('revenue', 0)),
            operating_profit=float(data.get('operating_profit', 0)),
            net_income=float(data.get('net_income', 0)),
            eps=float(data.get('eps', 0)),
            bps=float(data.get('bps', 0)),
            roe=float(data.get('roe', 0)),
            debt_ratio=float(data.get('debt_ratio', 0)),
            quick_ratio=float(data.get('quick_ratio', 0)),
            reserve_ratio=float(data.get('reserve_ratio', 0))
        )


@dataclass
class BalanceSheet:
    """재무상태표 데이터 모델"""
    code: str
    name: str
    fiscal_year: str
    fiscal_quarter: str
    total_assets: float
    current_assets: float
    non_current_assets: float
    total_liabilities: float
    current_liabilities: float
    non_current_liabilities: float
    total_equity: float
    capital: float
    retained_earnings: float
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BalanceSheet':
        """딕셔너리에서 재무상태표 객체 생성
        
        Args:
            data: API 응답 데이터
            
        Returns:
            BalanceSheet: 재무상태표 객체
        """
        return cls(
            code=data.get('code', ''),
            name=data.get('name', ''),
            fiscal_year=data.get('fiscal_year', ''),
            fiscal_quarter=data.get('fiscal_quarter', ''),
            total_assets=float(data.get('total_assets', 0)),
            current_assets=float(data.get('current_assets', 0)),
            non_current_assets=float(data.get('non_current_assets', 0)),
            total_liabilities=float(data.get('total_liabilities', 0)),
            current_liabilities=float(data.get('current_liabilities', 0)),
            non_current_liabilities=float(data.get('non_current_liabilities', 0)),
            total_equity=float(data.get('total_equity', 0)),
            capital=float(data.get('capital', 0)),
            retained_earnings=float(data.get('retained_earnings', 0))
        )


@dataclass
class IncomeStatement:
    """손익계산서 데이터 모델"""
    code: str
    name: str
    fiscal_year: str
    fiscal_quarter: str
    revenue: float
    cost_of_sales: float
    gross_profit: float
    operating_expenses: float
    operating_profit: float
    non_operating_income: float
    non_operating_expenses: float
    income_before_tax: float
    income_tax_expense: float
    net_income: float
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IncomeStatement':
        """딕셔너리에서 손익계산서 객체 생성
        
        Args:
            data: API 응답 데이터
            
        Returns:
            IncomeStatement: 손익계산서 객체
        """
        return cls(
            code=data.get('code', ''),
            name=data.get('name', ''),
            fiscal_year=data.get('fiscal_year', ''),
            fiscal_quarter=data.get('fiscal_quarter', ''),
            revenue=float(data.get('revenue', 0)),
            cost_of_sales=float(data.get('cost_of_sales', 0)),
            gross_profit=float(data.get('gross_profit', 0)),
            operating_expenses=float(data.get('operating_expenses', 0)),
            operating_profit=float(data.get('operating_profit', 0)),
            non_operating_income=float(data.get('non_operating_income', 0)),
            non_operating_expenses=float(data.get('non_operating_expenses', 0)),
            income_before_tax=float(data.get('income_before_tax', 0)),
            income_tax_expense=float(data.get('income_tax_expense', 0)),
            net_income=float(data.get('net_income', 0))
        )


@dataclass
class CashFlowStatement:
    """현금흐름표 데이터 모델"""
    code: str
    name: str
    fiscal_year: str
    fiscal_quarter: str
    operating_cash_flow: float
    investing_cash_flow: float
    financing_cash_flow: float
    net_cash_flow: float
    beginning_cash: float
    ending_cash: float
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CashFlowStatement':
        """딕셔너리에서 현금흐름표 객체 생성
        
        Args:
            data: API 응답 데이터
            
        Returns:
            CashFlowStatement: 현금흐름표 객체
        """
        return cls(
            code=data.get('code', ''),
            name=data.get('name', ''),
            fiscal_year=data.get('fiscal_year', ''),
            fiscal_quarter=data.get('fiscal_quarter', ''),
            operating_cash_flow=float(data.get('operating_cash_flow', 0)),
            investing_cash_flow=float(data.get('investing_cash_flow', 0)),
            financing_cash_flow=float(data.get('financing_cash_flow', 0)),
            net_cash_flow=float(data.get('net_cash_flow', 0)),
            beginning_cash=float(data.get('beginning_cash', 0)),
            ending_cash=float(data.get('ending_cash', 0))
        )


@dataclass
class FinancialRatio:
    """재무비율 데이터 모델"""
    code: str
    name: str
    fiscal_year: str
    fiscal_quarter: str
    per: float
    pbr: float
    pcr: float
    psr: float
    roe: float
    roa: float
    debt_ratio: float
    operating_margin: float
    net_margin: float
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FinancialRatio':
        """딕셔너리에서 재무비율 객체 생성
        
        Args:
            data: API 응답 데이터
            
        Returns:
            FinancialRatio: 재무비율 객체
        """
        return cls(
            code=data.get('code', ''),
            name=data.get('name', ''),
            fiscal_year=data.get('fiscal_year', ''),
            fiscal_quarter=data.get('fiscal_quarter', ''),
            per=float(data.get('per', 0)),
            pbr=float(data.get('pbr', 0)),
            pcr=float(data.get('pcr', 0)),
            psr=float(data.get('psr', 0)),
            roe=float(data.get('roe', 0)),
            roa=float(data.get('roa', 0)),
            debt_ratio=float(data.get('debt_ratio', 0)),
            operating_margin=float(data.get('operating_margin', 0)),
            net_margin=float(data.get('net_margin', 0))
        )