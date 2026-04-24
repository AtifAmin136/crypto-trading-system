"""
Data Models - Pydantic validation schemas
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Any, Dict
from datetime import datetime
from enum import Enum


# ==================== Enums ====================

class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_LOSS = "STOP_LOSS"
    TAKE_PROFIT = "TAKE_PROFIT"
    OCO = "OCO"


class TradeStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    OPEN = "OPEN"
    CLOSING = "CLOSING"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"


class PositionStatus(str, Enum):
    OPEN = "OPEN"
    PARTIALLY_CLOSED = "PARTIALLY_CLOSED"
    CLOSED = "CLOSED"


class TradingMode(str, Enum):
    MANUAL = "manual"
    SEMI_AUTO = "semi_auto"
    AUTO = "auto"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Timeframe(str, Enum):
    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"


class MarketTrend(str, Enum):
    BULL = "BULL"
    BEAR = "BEAR"
    SIDEWAYS = "SIDEWAYS"


# ==================== Request Models ====================

class SignalRequest(BaseModel):
    """Trade signal generation request"""
    symbol: str = Field(..., description="Trading pair (e.g., BTCUSDT)")
    side: OrderSide = Field(..., description="BUY or SELL")
    entry_price: Optional[float] = Field(None, description="Entry price (optional)")
    stop_loss: float = Field(..., description="Stop loss price", gt=0)
    take_profit_1: Optional[float] = Field(None, description="First take profit target")
    take_profit_2: Optional[float] = Field(None, description="Second take profit target")
    take_profit_3: Optional[float] = Field(None, description="Third take profit target")
    risk_amount: Optional[float] = Field(None, description="Risk in USDT")
    leverage: float = Field(1.0, ge=1, le=10, description="Leverage multiplier")
    timeframe: Timeframe = Field(Timeframe.H1, description="Chart timeframe")
    notes: Optional[str] = Field(None, description="Additional notes")
    
    @validator('take_profit_1', 'take_profit_2', 'take_profit_3')
    def validate_take_profits(cls, v, values):
        if v is None:
            return v
        if v <= 0:
            raise ValueError("Take profit must be greater than 0")
        return v


class TradeExecutionRequest(BaseModel):
    """Trade execution request"""
    symbol: str
    side: OrderSide
    entry_price: float
    stop_loss: float
    take_profits: List[float]
    position_size: float
    leverage: float = 1.0
    mode: TradingMode = TradingMode.MANUAL
    notes: Optional[str] = None


class CloseTradeRequest(BaseModel):
    """Close trade request"""
    trade_id: str
    exit_price: Optional[float] = None
    close_reason: Optional[str] = None


# ==================== Response Models ====================

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    version: str
    environment: str
    market_aggregator_status: str
    binance_api_status: str


class SuccessResponse(BaseModel):
    """Standard success response"""
    message: str
    data: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


# ==================== Trading Models ====================

class Order(BaseModel):
    """Order representation"""
    id: str
    symbol: str
    order_type: OrderType
    side: OrderSide
    price: float
    quantity: float
    status: str
    filled_quantity: float = 0.0
    timestamp: datetime
    binance_order_id: Optional[str] = None


class TradeSignal(BaseModel):
    """Trading signal"""
    id: str
    symbol: str
    side: OrderSide
    entry_price: float
    stop_loss: float
    take_profits: List[float] = []
    quality_score: float = Field(0, ge=0, le=100)
    confidence: float = Field(0, ge=0, le=1)
    reasoning: str
    ai_insights: Optional[str] = None
    risk_level: RiskLevel
    timestamp: datetime
    status: TradeStatus


class Trade(BaseModel):
    """Trade record"""
    id: str
    symbol: str
    side: OrderSide
    entry_price: float
    entry_time: datetime
    stop_loss: float
    take_profits: List[float]
    position_size: float
    leverage: float
    status: TradeStatus
    exit_price: Optional[float] = None
    exit_time: Optional[datetime] = None
    pnl: Optional[float] = None
    pnl_percent: Optional[float] = None
    duration_minutes: Optional[int] = None
    strategy_type: Optional[str] = None
    notes: Optional[str] = None
    ai_quality_score: Optional[float] = None
    mode: TradingMode = TradingMode.MANUAL


class Position(BaseModel):
    """Open position"""
    symbol: str
    side: OrderSide
    entry_price: float
    entry_time: datetime
    quantity: float
    leverage: float
    current_price: float
    unrealized_pnl: float
    unrealized_pnl_percent: float
    status: PositionStatus


# ==================== Risk Management Models ====================

class RiskAssessment(BaseModel):
    """Trade risk assessment"""
    trade_id: str
    risk_level: RiskLevel
    max_position_size: float
    warnings: List[str] = []
    recommendations: List[str] = []
    risk_score: float = Field(0, ge=0, le=100)
    can_trade: bool
    reasons: Optional[str] = None


class BehavioralWarning(BaseModel):
    """Behavioral trading warning"""
    type: str  # revenge_trading, overtrading, emotional, etc.
    severity: str  # low, medium, high, critical
    message: str
    suggested_action: str
    timestamp: datetime


# ==================== Market Data Models ====================

class Candle(BaseModel):
    """OHLCV candle data"""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class OrderBookSnapshot(BaseModel):
    """Order book snapshot"""
    symbol: str
    bids: List[tuple] = Field(..., description="List of [price, quantity]")
    asks: List[tuple] = Field(..., description="List of [price, quantity]")
    timestamp: datetime


class MarketData(BaseModel):
    """Current market data for a symbol"""
    symbol: str
    current_price: float
    high_24h: float
    low_24h: float
    volume_24h: float
    price_change_24h: float
    price_change_percent_24h: float
    bid: float
    ask: float
    timestamp: datetime


# ==================== AI Models ====================

class TradeAnalysis(BaseModel):
    """AI trade analysis result"""
    symbol: str
    trade_quality_score: float = Field(0, ge=0, le=100)
    should_trade: bool
    risk_level: RiskLevel
    trend: MarketTrend
    volatility_level: str
    technical_setup: str
    warnings: List[str] = []
    insights: List[str] = []
    recommendations: List[str] = []
    confidence: float = Field(0, ge=0, le=1)
    analysis_time: datetime


class AICoachingTip(BaseModel):
    """AI coaching tip"""
    type: str
    title: str
    message: str
    severity: str  # info, warning, critical
    action_items: List[str] = []
    timestamp: datetime


# ==================== Portfolio Models ====================

class Portfolio(BaseModel):
    """User portfolio overview"""
    total_balance: float
    available_balance: float
    used_margin: float
    total_pnl: float
    total_pnl_percent: float
    open_positions_count: int
    total_trades: int
    win_rate: float
    average_rr: float
    largest_win: Optional[float] = None
    largest_loss: Optional[float] = None
    daily_pnl: float
    daily_pnl_percent: float


class PortfolioStats(BaseModel):
    """Portfolio statistics"""
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    average_win: float
    average_loss: float
    profit_factor: float
    max_drawdown: float
    max_drawdown_percent: float
    average_trade_duration_minutes: float
    best_trade: float
    worst_trade: float
    daily_loss_limit: float
    daily_loss_used: float


# ==================== History Models ====================

class TradeHistoryEntry(BaseModel):
    """Trade history entry"""
    trade_id: str
    symbol: str
    entry_time: datetime
    exit_time: Optional[datetime]
    side: OrderSide
    entry_price: float
    exit_price: Optional[float]
    quantity: float
    pnl: Optional[float]
    pnl_percent: Optional[float]
    status: TradeStatus


class DailyStats(BaseModel):
    """Daily trading statistics"""
    date: str
    trades_count: int
    winning_trades: int
    losing_trades: int
    daily_pnl: float
    daily_pnl_percent: float
    win_rate: float


# ==================== Alert Models ====================

class Alert(BaseModel):
    """Alert notification"""
    id: str
    type: str  # trade_signal, tp_hit, sl_hit, risk_violation, ai_warning
    title: str
    message: str
    severity: str  # low, medium, high, critical
    symbol: Optional[str] = None
    trade_id: Optional[str] = None
    timestamp: datetime
    read: bool = False


class AlertConfig(BaseModel):
    """Alert configuration"""
    enable_desktop_alerts: bool = True
    enable_telegram_alerts: bool = False
    enable_email_alerts: bool = False
    alert_types: List[str] = []
    min_severity: str = "medium"
