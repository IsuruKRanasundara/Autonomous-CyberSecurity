"""Application configuration settings using Pydantic."""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class AppSettings(BaseSettings):
    """Application configuration."""

    # App metadata
    APP_NAME: str = Field(default="AI Multi-Agent SOC", description="Application name")
    APP_VERSION: str = Field(default="0.1.0", description="Application version")
    DEBUG: bool = Field(default=False, description="Enable debug mode")
    ENVIRONMENT: str = Field(default="development", description="Deployment environment")

    # Server
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")

    # CORS
    CORS_ORIGINS: list[str] = Field(
        default=["*"],
        description="Allowed origins for CORS",
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


class DatabaseSettings(BaseSettings):
    """Database configuration."""

    # PostgreSQL
    POSTGRES_HOST: str = Field(default="localhost", description="PostgreSQL host")
    POSTGRES_PORT: int = Field(default=5432, description="PostgreSQL port")
    POSTGRES_USER: str = Field(default="postgres", description="PostgreSQL user")
    POSTGRES_PASSWORD: str = Field(default="postgres", description="PostgreSQL password")
    POSTGRES_DB: str = Field(default="soc_db", description="PostgreSQL database name")
    POSTGRES_POOL_SIZE: int = Field(default=10, description="Connection pool size")
    POSTGRES_MAX_OVERFLOW: int = Field(default=20, description="Max pool overflow")

    @property
    def postgres_url(self) -> str:
        """Construct PostgreSQL connection URL."""
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


class ElasticsearchSettings(BaseSettings):
    """Elasticsearch configuration."""

    ELASTICSEARCH_HOST: str = Field(default="localhost", description="Elasticsearch host")
    ELASTICSEARCH_PORT: int = Field(default=9200, description="Elasticsearch port")
    ELASTICSEARCH_USERNAME: Optional[str] = Field(
        default=None, description="Elasticsearch username"
    )
    ELASTICSEARCH_PASSWORD: Optional[str] = Field(
        default=None, description="Elasticsearch password"
    )
    ELASTICSEARCH_SCHEME: str = Field(default="http", description="Elasticsearch scheme")
    ELASTICSEARCH_INDEX_PREFIX: str = Field(
        default="soc", description="Index name prefix"
    )

    @property
    def elasticsearch_url(self) -> str:
        """Construct Elasticsearch URL."""
        auth = ""
        if self.ELASTICSEARCH_USERNAME and self.ELASTICSEARCH_PASSWORD:
            auth = f"{self.ELASTICSEARCH_USERNAME}:{self.ELASTICSEARCH_PASSWORD}@"
        return (
            f"{self.ELASTICSEARCH_SCHEME}://{auth}{self.ELASTICSEARCH_HOST}:"
            f"{self.ELASTICSEARCH_PORT}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


class VectorDBSettings(BaseSettings):
    """Vector database configuration."""

    # Chroma
    CHROMA_ENABLED: bool = Field(default=True, description="Enable Chroma vector DB")
    CHROMA_HOST: str = Field(default="localhost", description="Chroma host")
    CHROMA_PORT: int = Field(default=8000, description="Chroma port")
    CHROMA_COLLECTION_NAME: str = Field(
        default="security_incidents", description="Chroma collection name"
    )

    # Pinecone
    PINECONE_ENABLED: bool = Field(default=False, description="Enable Pinecone vector DB")
    PINECONE_API_KEY: Optional[str] = Field(default=None, description="Pinecone API key")
    PINECONE_ENVIRONMENT: Optional[str] = Field(
        default=None, description="Pinecone environment"
    )
    PINECONE_INDEX_NAME: Optional[str] = Field(
        default="security-incidents", description="Pinecone index name"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


class KafkaSettings(BaseSettings):
    """Kafka configuration."""

    KAFKA_ENABLED: bool = Field(default=True, description="Enable Kafka")
    KAFKA_BOOTSTRAP_SERVERS: list[str] = Field(
        default=["localhost:9092"],
        description="Kafka bootstrap servers",
    )
    KAFKA_CONSUMER_GROUP: str = Field(
        default="soc-backend", description="Kafka consumer group"
    )
    KAFKA_AUTO_OFFSET_RESET: str = Field(
        default="earliest", description="Auto offset reset strategy"
    )
    KAFKA_SESSION_TIMEOUT_MS: int = Field(default=30000, description="Session timeout")

    # Topics
    KAFKA_ALERTS_TOPIC: str = Field(default="alerts", description="Alerts topic")
    KAFKA_INCIDENTS_TOPIC: str = Field(default="incidents", description="Incidents topic")
    KAFKA_LOGS_TOPIC: str = Field(default="logs", description="Logs topic")
    KAFKA_TELEMETRY_TOPIC: str = Field(default="telemetry", description="Telemetry topic")

    class Config:
        env_file = ".env"
        case_sensitive = True


class LLMSettings(BaseSettings):
    """LLM and AI configuration."""

    # OpenAI
    OPENAI_ENABLED: bool = Field(default=True, description="Enable OpenAI")
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API key")
    OPENAI_MODEL: str = Field(default="gpt-4", description="OpenAI model name")
    OPENAI_TEMPERATURE: float = Field(default=0.7, description="Temperature for generation")
    OPENAI_MAX_TOKENS: int = Field(default=2000, description="Max tokens for completion")

    # Ollama
    OLLAMA_ENABLED: bool = Field(default=False, description="Enable Ollama")
    OLLAMA_HOST: str = Field(default="http://localhost:11434", description="Ollama host")
    OLLAMA_MODEL: str = Field(default="mistral", description="Ollama model name")

    # Embeddings
    EMBEDDINGS_MODEL: str = Field(
        default="text-embedding-3-small", description="Embeddings model"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


class SecuritySettings(BaseSettings):
    """Security configuration."""

    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for JWT signing",
    )
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, description="Access token expiration in minutes"
    )

    # API Keys
    API_KEY_HEADER: str = Field(default="X-API-Key", description="API key header name")

    class Config:
        env_file = ".env"
        case_sensitive = True


class LoggingSettings(BaseSettings):
    """Logging configuration."""

    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format",
    )
    LOG_FILE: Optional[str] = Field(default=None, description="Log file path")

    class Config:
        env_file = ".env"
        case_sensitive = True


class Settings(BaseSettings):
    """Combined application settings."""

    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    elasticsearch: ElasticsearchSettings = Field(default_factory=ElasticsearchSettings)
    vector_db: VectorDBSettings = Field(default_factory=VectorDBSettings)
    kafka: KafkaSettings = Field(default_factory=KafkaSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
