# import json
import os
from typing import Literal, TypedDict

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
print("dotenv_path", dotenv_path)
load_dotenv(dotenv_path)


class AppSettings(BaseSettings):
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 5000
    max_content: int = 104857600
    environment: str = "development"
    app_url: str
    front_end_url: str
    upload_folder: str
    secret_key: str
    stacktrace: bool = False
    # templates_auto_reload: bool = True
    # session_permanent: bool = False

    # security_password_salt: str
    # security_email_validator_args: str
    # max_content_length: int = 16 * 1024 * 1024
    look_up_query_limit: int = 10
    const_plan: list[int] = [4, 5, 6, 7, 8]
    image_folder_path: str = "static"


class StorySettings(BaseSettings):
    interval_min: str = "1"
    available_llms: list[str] = ["llama", "gpt", "claude", "mistral", "gemini"]


class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LOGGING_")

    level: str = "DEBUG"
    debug_arg_length: int = 20


class DbSettings(BaseSettings):
    # sqlalchemy_database_uri: str
    # sqlalchemy_engine_options: dict[str, int] = {
    #     "pool_recycle": 299,
    #     "pool_size": 20,
    #     "max_overflow": 10,
    # }
    sqlalchemy_track_modifications: str = "False"
    async_sqlalchemy_database_uri: str
    async_sqlalchemy_engine_options: dict[str, int] = {
        "pool_recycle": 299,
        "pool_size": 10,
        "max_overflow": 2,
    }
    expire_on_commit: bool = False
    auto_commit: bool = False
    auto_flush: bool = False


class TokenSettings(BaseSettings):
    tokens_per_page: int = 800
    pages_per_min: int = 3
    acceptable_error_ratio: float = 0.2
    max_tokens_per_job: int = 1500


# class AWSSettings(BaseSettings):
#     model_config = SettingsConfigDict(env_prefix="AWS_")
#     access_key: str
#     secret_access_key: str
#     default_region: str = "eu-north-1"
#     logging_level: str = "ERROR"
#     s3_uri: str = "https://cephadex-dev.s3.eu-north-1.amazonaws.com"
#     bucket: str = "cephadex-dev"


class CorsSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CORS_")

    origins: list[str] = ["http://localhost:5173"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]


class AISettings(BaseSettings):
    openai_api_key: str
    openai_main_model: str = "gpt-3.5-turbo-0125"
    temperature: float = 0.2
    images_model: str = "dall-e-2"
    anthropic_api_key: str
    mistral_api_key: str
    gemini_api_key: str
    replicate_api_key: str
    max_ai_caller_attempts: int = 3
    claude_main_model: str = "claude-instant-1.2"
    audio_model: str = "whisper-1"
    image_size: str = "256x256"
    type_response: str = "text"
    echo: bool = True


class MonitoringSettings(BaseSettings):
    sentry_dsn: str = "dummy_key"
    traces_sample_rate: float = 1.0
    profiles_sample_rate: float = 0.1
    post_hog_api_key: str = "dummy_key"
    post_hog_host: str = "https://eu.posthog.com"
    monitoring_enabled: bool = False


class Settings(BaseSettings):
    app: AppSettings = AppSettings()  # type: ignore
    logging: LoggingSettings = LoggingSettings()
    db: DbSettings = DbSettings()  # type: ignore
    token: TokenSettings = TokenSettings()
    monitoring: MonitoringSettings = MonitoringSettings()
    # aws: AWSSettings = AWSSettings()  # type: ignore
    cors: CorsSettings = CorsSettings()
    ai: AISettings = AISettings()  # type: ignore
    story: StorySettings = StorySettings()
