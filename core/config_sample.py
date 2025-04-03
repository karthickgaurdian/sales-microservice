from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application settings
    APP_ENV: str = "development"
    APP_NAME: str = "kafka-consumer-service"
    
    # Kafka settings
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_GROUP_ID: str = "consumer-group"
    KAFKA_TOPIC: str = "events-topic"
    KAFKA_AUTO_OFFSET_RESET: str = "earliest"
    KAFKA_MAX_POLL_RECORDS: int = 100
    KAFKA_SESSION_TIMEOUT_MS: int = 60000
    
    # Database settings
    DATABASE_URL: str = "sqlite:///data/enterprise.db"
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/consumer.log"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    LOG_MAX_BYTES: int = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    # Retry settings
    MAX_RETRIES: int = 3
    INITIAL_RETRY_DELAY: float = 1.0
    MAX_RETRY_DELAY: float = 60.0
    
    # Cleanup settings
    LOG_CLEANUP_DAYS: int = 30
    LOG_CLEANUP_ENABLED: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create a global settings instance
settings = Settings() 