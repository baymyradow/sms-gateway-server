import secrets
import warnings
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    PostgresDsn,
    computed_field,
    model_validator
)
from typing import Literal
from typing_extensions import Self

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V0_STR: str = "/api/v0"
    GATEWAY_PRIVATE_TOKEN: str = secrets.token_hex(32)
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str = "Sms-Gateway-Server"
    POSTGRES_HOST: str 
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str 

    @computed_field
    @property
    def ASYNCPG_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB
        )
    
    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis" ',
                "Please change it for security, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message)
            else:
                raise ValueError(message)
            
    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("GATEWAY_PRIVATE_TOKEN", self.GATEWAY_PRIVATE_TOKEN)
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)

        return self



settings = Settings()
