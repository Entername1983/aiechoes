# import json
# import os

# from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
# print("dotenv_path", dotenv_path)
# load_dotenv(dotenv_path)


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


# https://platform.openai.com/docs/models
class OpenAiSettings(BaseSettings):
    openai_api_key: str
    main_model: str = "gpt-4o-mini"
    image_model: str = "dall-e-2"
    audio_model: str = "whisper-1"
    image_size: str = "256x256"
    max_tokens: int = 4095


# https://docs.anthropic.com/en/docs/resources/model-deprecations
class AnthropicSettings(BaseSettings):
    anthropic_api_key: str
    main_model: str = "claude-3-haiku-20240307"
    max_tokens: int = 2000


# https://docs.mistral.ai/getting-started/models/
# https://mistral.ai/technology/#pricing
class MistralSettings(BaseSettings):
    mistral_api_key: str
    main_model: str = "open-mistral-nemo-2407"


# https://ai.google.dev/pricing
class GeminiSettings(BaseSettings):
    gemini_api_key: str
    main_model: str = "gemini-1.5-flash"


# https://replicate.com/pricing
## do not use meta-llama-3-8b, it suxxors
## meta-llama-3-70b is also not able to follow simple instructions,
# repeats the entire prompt before answering
class LlamaSettings(BaseSettings):
    replicate_api_key: str
    main_model: str = "meta-llama-3.1-405b-instruct"
    min_tokens: int = 0


class AISettings(BaseSettings):
    open_ai: OpenAiSettings = OpenAiSettings()  # type: ignore
    anthropic: AnthropicSettings = AnthropicSettings()  # type: ignore
    mistral: MistralSettings = MistralSettings()  # type: ignore
    gemini: GeminiSettings = GeminiSettings()  # type: ignore
    llama: LlamaSettings = LlamaSettings()  # type: ignore
    temperature: float = 0.2
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    max_ai_caller_attempts: int = 3
    type_response: str = "text"
    echo: bool = True
    top_p: float = 0.9
    top_k: int = 0


class MonitoringSettings(BaseSettings):
    sentry_dsn: str = "dummy_key"
    traces_sample_rate: float = 1.0
    profiles_sample_rate: float = 0.1
    post_hog_api_key: str = "dummy_key"
    post_hog_host: str = "https://eu.posthog.com"
    monitoring_enabled: bool = False


class S3Settings(BaseSettings):
    s3_access_key_id: str
    s3_secret_access_key: str
    s3_public_endpoint: str
    s3_internal_endpoint: str
    s3_bucket_name: str
    s3_default_region: str = "us-east-1"


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
    s3: S3Settings = S3Settings()  # type: ignore
