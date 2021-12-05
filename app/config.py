from pydantic import BaseSettings

#perform validation that all env vars are set
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    #Pull env variables
    class Config:
        env_file = '.env'

settings = Settings()