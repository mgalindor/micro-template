from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    name: str = Field(default="metrics", description="Nombre de la base de datos")
    user: str = Field(default="metrics", description="Usuario de la base de datos")
    password: str = Field(
        default="pa55word", description="Password de la base de datos"
    )
    host: str = Field(default="localhost", description="Host de la base de datos")
    port: int = Field(default=5432, description="Puerto de la base de datos")
    driver: str = Field(
        default="postgresql+asyncpg", description="Driver de SQLAlchemy a utilizar"
    )
    echo: bool = Field(default=False, description="Loguea las queries SQL en consola")
    pool_size: int = Field(
        default=10,
        description="Número de conexiones a mantener abiertas dentro del pool",
    )
    max_overflow: int = Field(
        default=20, description="Conexiones que se pueden abrir por encima de pool_size"
    )
    pool_recycle: int = Field(
        default=3600,
        description="Segundos tras los cuales el pool recicla una conexión",
    )
    pool_pre_ping: bool = Field(
        default=True,
        description="Verifica que la conexión siga viva antes de entregarla desde el pool",
    )
    pool_timeout: int = Field(
        default=30,
        description="Segundos de espera antes de fallar al pedir una conexión del pool",
    )
    isolation_level: Literal[
        "AUTOCOMMIT",
        "READ COMMITTED",
        "READ UNCOMMITTED",
        "REPEATABLE READ",
        "SERIALIZABLE",
    ] = Field(
        default="READ COMMITTED",
        description="Nivel de aislamiento de las transacciones",
    )

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class LoggingConfig(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Nivel de logging (structlog/logging)"
    )


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.local", env_prefix="app_", env_nested_delimiter="__", extra="ignore"
    )

    name: str = Field(
        default="metrics-colelctor", description="Nombre de la aplicación"
    )
    mode: Literal["dev", "prod", "test"] = Field(
        default="dev", description="Modo de ejecución de la aplicación"
    )
    run_migrations_on_startup: bool = Field(
        default=True,
        description="Aplica las migraciones de Alembic (upgrade head) al iniciar la app. "
        "Desactivar en despliegues con múltiples réplicas concurrentes.",
    )
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


settings = AppConfig()
