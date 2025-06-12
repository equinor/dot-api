import os
from pydantic import Field
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    CLIENT_ID: str = Field(
        default=os.getenv("CLIENT_ID", "4251833c-b9c3-4013-afda-cbfd2cc50f3f")
    )
 
    REDIRECT_URL: str = Field(
        default=os.getenv("REDIRECT_URL", "http://localhost:8000/docs/oauth2-redirect")
    )
    SCOPE: str = Field(
        default=os.getenv("SCOPE", "api://4251833c-b9c3-4013-afda-cbfd2cc50f3f/Read")
    )
    TENANT_ID: str = "3aa4a235-b6e2-48d5-9195-7fcf05b459b0"
    AUTHORITY: str = f"https://login.microsoftonline.com/{TENANT_ID}"
    AUTH_URL: str = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"
    TOKEN_URL: str = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    JWKS_URL: str = f"{AUTHORITY}/discovery/v2.0/keys"
    AUDIENCE: str = Field(default=os.getenv("AUDIENCE", "api://4251833c-b9c3-4013-afda-cbfd2cc50f3f"))
    JWKS_URI: str = (
        f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"
    )
    ISSUER: str = f"https://sts.windows.net/{TENANT_ID}/"
    APP_ENV: str = Field(
        default=os.getenv("APP_ENV", "local")
    )
    DATABASE_URL: str = Field(
        default=os.getenv("DATABASE_URL", "devurl")
    )