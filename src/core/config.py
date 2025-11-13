from typing import Literal

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置（支持PostgreSql 和 SqLite，含连接池配置）"""
    app_name: str = "What to Eat"
    debug: bool = False

    # 数据库类型
    db_type: Literal["postgresql", "sqlite"] = "postgresql"

    # PostgreSql 配置
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_name: str = "what2eat"

    # 连接池配置 （仅PostGreSql有效）
    # --- 必选参数：中等并发常用 ---
    pool_size: int = 20  # 连接池基础大小：低：- 高：+
    max_overflow: int = 10  # 超出 pool_size 的最大连接数
    pool_timeout: int = 30  # 获取链接超时时间
    pool_pre_ping: bool = True  # 取连接前是否检查可用性

    # --- 可选调优参数（高级场景） ---
    pool_recycle: int = 3600  # 最大存活时间，避免长连接被数据库踢掉
    pool_use_lifo: bool = True  # 连接池连接连接顺序，False = FIFO（默认先进先出），True = LIFO（后进先出）可提高高并发命中率
    echo: bool = False  # 是否打印sql，开发可打开，生产关闭

    # SqLite 配置
    sqlite_db_path: str = "./data/what2eat.sqlite3"

    # Redis配置
    redis_host: str = "localhost"
    redis_port: int = 6379
    auth_redis_db: int = 0
    redis_db: int = 1

    @computed_field
    @property
    def database_url(self) -> str:
        if self.db_type == "postgresql":
            return (f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
                    f"@{self.db_host}:{self.db_port}/{self.db_name}")
        elif self.db_type == "sqlite":
            return f"sqlite+aiosqlite:///{self.sqlite_db_path}"
        else:
            raise ValueError(f"Unsupported DB_TYPE: {self.db_type}")

    @computed_field
    @property
    def engine_options(self) -> dict:
        """统一封装 engine options，供 create_async_engine 使用"""
        if self.db_type == "postgresql":
            return {
                "pool_size": self.pool_size,
                "max_overflow": self.max_overflow,
                "pool_timeout": self.pool_timeout,
                "pool_pre_ping": self.pool_pre_ping,
                "pool_recycle": self.pool_recycle,
                "pool_use_lifo": self.pool_use_lifo,
                "echo": self.echo,
            }
        return {"echo": self.echo}

    @computed_field
    @property
    def auth_redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.auth_redis_db}"

    @computed_field
    @property
    def cache_redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    # JWT配置
    jwt_secret: str = "龘爨麤鬻籱灪蠼蠛纛齉鬲靐龗齾龕鑪鸙饢驫麣"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)


settings = Settings()
