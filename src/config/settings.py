from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "AgentCellphoneV2"
    APP_ENV: str = "development"
    TZ: str = "America/Chicago"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_DIRECTORY: str = "logs"
    LOG_FILE: str = "logs/app.log"
    DEBUG_MODE: bool = False
    FLASK_DEBUG: bool = False
    VERBOSE_LOGGING: bool = False

    # Observability
    LOG_SLOW_QUERIES: bool = True
    SLOW_QUERY_THRESHOLD: float = 1.0
    LOG_MEMORY_USAGE: bool = True
    MEMORY_THRESHOLD: int = 100
    LOG_AUTH_ATTEMPTS: bool = True
    LOG_API_CALLS: bool = True
    LOG_FILE_ACCESS: bool = False
    MASK_SENSITIVE_DATA: bool = True
    LOG_EXTERNAL_APIS: bool = True
    LOG_DATABASE_CONNECTIONS: bool = True
    LOG_MESSAGE_QUEUE: bool = True
    LOG_WEBSOCKET: bool = True

    # Feature flags
    ENABLE_DEVELOPMENT_FEATURES: bool = False
    ENABLE_TESTING_MODE: bool = False
    ENABLE_PROFILING: bool = False

    # Paths
    CONFIG_DIRECTORY: str = "config"
    DATA_DIRECTORY: str = "data"
    CACHE_DIRECTORY: str = "cache"
    REPORTS_DIR: str = "reports"

    # API
    API_TIMEOUT: int = 30
    API_RETRY_ATTEMPTS: int = 3
    API_RATE_LIMIT: int = 100

    # DB
    DB_CONNECTION_TIMEOUT: int = 10
    DB_QUERY_TIMEOUT: int = 30
    DB_POOL_SIZE: int = 10
    CURSOR_DB_PATH: str = "data/cursor_tasks.db"

    # Web
    WEB_HOST: str = "127.0.0.1"
    WEB_PORT: int = 5000
    WEB_WORKERS: int = 4
    WEB_TIMEOUT: int = 60

    # Secrets
    FLASK_DEV_SECRET_KEY: str | None = None
    FLASK_TEST_SECRET_KEY: str | None = None
    FLASK_PROD_SECRET_KEY: str | None = None
    PORTAL_SECRET_KEY: str | None = None
    PORTAL_SESSION_SECRET: str | None = None

    # Redis / Rabbit
    PORTAL_REDIS_PASSWORD: str | None = None
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_URL: str | None = None

    PORTAL_RABBITMQ_USERNAME: str | None = None
    PORTAL_RABBITMQ_PASSWORD: str | None = None
    PORTAL_RABBITMQ_HOST: str = "127.0.0.1"
    PORTAL_RABBITMQ_PORT: int = 5672
    RABBITMQ_URL: str | None = None

    TEST_USER_PASSWORD: str | None = None
    ADMIN_USER_PASSWORD: str | None = None
    HEALTH_MONITOR_SECRET_KEY: str | None = None

    # Timeouts / intervals
    SCRAPE_TIMEOUT: float = 30.0
    RESPONSE_WAIT_TIMEOUT: float = 120.0
    QUALITY_CHECK_INTERVAL: float = 30.0
    METRICS_COLLECTION_INTERVAL: float = 60.0
    SMOKE_TEST_TIMEOUT: int = 60
    UNIT_TEST_TIMEOUT: int = 120
    INTEGRATION_TEST_TIMEOUT: int = 300
    PERFORMANCE_TEST_TIMEOUT: int = 600
    SECURITY_TEST_TIMEOUT: int = 180
    API_TEST_TIMEOUT: int = 240
    COORDINATION_TEST_TIMEOUT: int = 180
    LEARNING_TEST_TIMEOUT: int = 180

    # Swarm
    AGENT_COUNT: int = 8
    CAPTAIN_ID: str = "Agent-4"
    DEFAULT_MODE: str = "pyautogui"
    COORDINATE_MODE: str = "8-agent"

    # Patterns
    TEST_FILE_PATTERN: str = "test_*.py"
    ARCHITECTURE_FILES: str = r"\.(py|js|ts|java|cpp|h|md)$"
    CONFIG_FILES: str = r"(config|settings|env|yml|yaml|json|toml|ini)$"
    TEST_FILES: str = r"(test|spec)\.(py|js|ts|java)$"
    DOCS_FILES: str = r"(README|CHANGELOG|CONTRIBUTING|docs?)\.md$"
    BUILD_FILES: str = (
        r"(Dockerfile|docker-compose|\.gitlab-ci|\.github|Makefile|build\.gradle|pom\.xml)$"
    )

    # SLOs
    TEST_FAILURE_THRESHOLD: int = 0
    PERFORMANCE_DEGRADATION_THRESHOLD: float = 100.0
    COVERAGE_THRESHOLD: float = 80.0
    RESPONSE_TIME_TARGET: float = 100.0
    THROUGHPUT_TARGET: float = 1000.0
    SCALABILITY_TARGET: int = 100
    RELIABILITY_TARGET: float = 99.9
    LATENCY_TARGET: float = 50.0
    SINGLE_MESSAGE_TIMEOUT: float = 1.0
    BULK_MESSAGE_TIMEOUT: float = 10.0
    CONCURRENT_MESSAGE_TIMEOUT: float = 5.0
    MIN_THROUGHPUT: float = 10.0
    MAX_MEMORY_PER_MESSAGE: int = 1024

    # Browser
    GPT_URL: str
    CONVERSATION_URL: str
    INPUT_SELECTOR: str = "textarea[data-testid='prompt-textarea']"
    SEND_BUTTON_SELECTOR: str = "button[data-testid='send-button']"
    RESPONSE_SELECTOR: str = "[data-testid='conversation-turn']:last-child .markdown"
    THINKING_INDICATOR: str = "[data-testid='thinking-indicator']"
    MAX_SCRAPE_RETRIES: int = 3
    HEADLESS: bool = True
    CHROME_PROFILE_PATH: str | None = None

    # Coverage / history / reports
    COVERAGE_REPORT_PRECISION: int = 2
    HISTORY_WINDOW: int = 100
    INCLUDE_METADATA: bool = True
    INCLUDE_RECOMMENDATIONS: bool = True

    # Concurrency
    DEFAULT_MAX_WORKERS: int = 4

    @validator("REDIS_URL", pre=True, always=True)
    def build_redis_url(cls, v, values):
        if v:
            return v
        pwd = values.get("PORTAL_REDIS_PASSWORD") or ""
        host = values.get("REDIS_HOST")
        port = values.get("REDIS_PORT")
        db = values.get("REDIS_DB")
        auth = f":{pwd}@" if pwd else ""
        return f"redis://{auth}{host}:{port}/{db}"

    @validator("RABBITMQ_URL", pre=True, always=True)
    def build_amqp_url(cls, v, values):
        if v:
            return v
        user = values.get("PORTAL_RABBITMQ_USERNAME") or ""
        pwd = values.get("PORTAL_RABBITMQ_PASSWORD") or ""
        host = values.get("PORTAL_RABBITMQ_HOST")
        port = values.get("PORTAL_RABBITMQ_PORT")
        if user and pwd:
            return f"amqp://{user}:{pwd}@{host}:{port}//"
        # allow localhost without creds for dev
        return f"amqp://{host}:{port}//"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Allow extra fields from environment


settings = Settings()
