from pydantic import BaseSettings

# Used to validate the variables found as they are env variables
# Pydantic is also case unsensitive so does not matter the case of the object
class Settings(BaseSettings):
    database_url: str
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()