from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    K221000_FILE_URL: str    
    K230909_FILE_URL: str
    K232639_FILE_URL: str

    EMBEDDING_MODEL: str
    OPENROUTER_MODEL_NAME: str
    OPENROUTER_API_KEY: str
    DATABASE_DIR: str

    model_config = SettingsConfigDict(env_file=".env")



def get_settings():
    return Settings()

def get_pdfs_urls():
    settings = Settings()
    return [
        settings.K221000_FILE_URL,
        settings.K230909_FILE_URL,
        settings.K232639_FILE_URL
    ]