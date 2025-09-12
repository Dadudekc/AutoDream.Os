"""
Trading Robot Configuration Settings
"""

from pydantic_settings import BaseSettings


class TradingConfig(BaseSettings):
    """Trading Robot Configuration"""

    # Alpaca API Configuration
    alpaca_api_key: str = ""
    alpaca_secret_key: str = ""
    alpaca_base_url: str = "https://paper-api.alpaca.markets"  # Paper trading by default
    alpaca_feed: str = "iex"  # Market data feed

    # Trading Configuration
    max_positions: int = 10
    max_position_size_pct: float = 0.1  # Max 10% of portfolio per position
    max_portfolio_risk_pct: float = 0.05  # Max 5% portfolio risk
    default_stop_loss_pct: float = 0.02  # 2% stop loss
    default_take_profit_pct: float = 0.04  # 4% take profit

    # Risk Management
    daily_loss_limit_pct: float = 0.03  # Stop trading if daily loss exceeds 3%
    max_daily_trades: int = 20
    min_order_value: float = 100.0
    max_order_value: float = 10000.0

    # Trading Hours (EST)
    market_open_hour: int = 9
    market_close_hour: int = 16
    trading_days: list[str] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # Database Configuration
    database_url: str = "sqlite:///trading_robot.db"
    redis_url: str | None = None

    # Web Dashboard
    web_host: str = "0.0.0.0"
    web_port: int = 8000
    enable_dashboard: bool = True

    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/trading_robot.log"

    # Backtesting
    backtest_initial_balance: float = 100000.0
    backtest_commission_pct: float = 0.001  # 0.1% commission
    backtest_slippage_pct: float = 0.0005  # 0.05% slippage

    # Alert Configuration
    enable_email_alerts: bool = False
    email_smtp_server: str = ""
    email_smtp_port: int = 587
    email_username: str = ""
    email_password: str = ""
    alert_email_recipients: list[str] = []

    # Emergency Configuration
    emergency_stop_enabled: bool = True
    emergency_stop_loss_pct: float = 0.1  # Emergency stop at 10% loss
    emergency_shutdown_timeout: int = 300  # 5 minutes timeout

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global configuration instance
config = TradingConfig()
