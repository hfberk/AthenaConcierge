from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: Optional[str] = ""
    SUPABASE_SERVICE_KEY: Optional[str] = ""
    DATABASE_URL: Optional[str] = "sqlite:///./test.db"
    
    # Anthropic
    ANTHROPIC_API_KEY: Optional[str] = ""
    
    # Slack
    SLACK_BOT_TOKEN: Optional[str] = ""
    SLACK_APP_TOKEN: Optional[str] = ""
    SLACK_SIGNING_SECRET: Optional[str] = ""
    
    # AWS
    AWS_ACCESS_KEY_ID: Optional[str] = ""
    AWS_SECRET_ACCESS_KEY: Optional[str] = ""
    AWS_REGION: str = "us-east-1"
    SES_EMAIL_ADDRESS: Optional[str] = ""
    
    # Application
    SECRET_KEY: str = "temporary-secret-key-change-in-production"
    ENVIRONMENT: str = "development"
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }

settings = Settings()   