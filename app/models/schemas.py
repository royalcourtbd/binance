from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class P2POrder(BaseModel):
    """P2P Order model"""
    orderNumber: Optional[str] = None
    advNo: Optional[str] = None
    tradeType: Optional[str] = None
    asset: Optional[str] = None
    fiat: Optional[str] = None
    fiatSymbol: Optional[str] = None
    amount: Optional[str] = None
    totalPrice: Optional[str] = None
    unitPrice: Optional[str] = None
    orderStatus: Optional[str] = None
    createTime: Optional[int] = None
    commission: Optional[str] = None
    counterPartNickName: Optional[str] = None
    advertisementRole: Optional[str] = None
    payMethodName: Optional[str] = None
    takerCommission: Optional[str] = None
    takerCommissionRate: Optional[str] = None
    takerAmount: Optional[str] = None
    additionalKycVerify: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "orderNumber": "123456789",
                "advNo": "987654321",
                "tradeType": "BUY",
                "asset": "USDT",
                "fiat": "BDT",
                "fiatSymbol": "৳",
                "amount": "100.00",
                "totalPrice": "12000.00",
                "unitPrice": "120.00",
                "orderStatus": "COMPLETED",
                "createTime": 1640000000000,
                "commission": "0.10"
            }
        }


class OrdersResponse(BaseModel):
    """Response model for orders endpoint"""
    success: bool
    message: str
    data: List[P2POrder]
    count: int
    trade_type: Optional[str] = None
    cached: bool = False


class OrdersSummary(BaseModel):
    """Summary statistics for orders"""
    total_buy_orders: int
    total_sell_orders: int
    total_completed_orders: int
    total_buy_amount: float
    total_sell_amount: float
    total_buy_value: float
    total_sell_value: float
    total_buy_fees: float
    total_sell_fees: float
    total_fees: float
    average_buy_price: Optional[float] = None
    average_sell_price: Optional[float] = None
    net_profit_bdt: Optional[float] = None
    net_profit_percentage: Optional[float] = None


class SummaryResponse(BaseModel):
    """Response model for summary endpoint"""
    success: bool
    message: str
    data: OrdersSummary
    cached: bool = False


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    message: str
    error: Optional[str] = None
    status_code: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    app_name: str
    version: str
    timestamp: datetime
    binance_api_configured: bool


class CacheStatsResponse(BaseModel):
    """Cache statistics response"""
    success: bool
    message: str
    data: dict
