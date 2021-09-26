import os


class Settings:
    """Settings for the bot"""
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")
    phone = os.getenv("PHONE")
    username = os.getenv("USERNAME")
    email = os.getenv("EMAIL")
    tg_id = os.getenv("TG_ID")


settings = Settings()
