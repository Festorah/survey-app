from decouple import config


class Settings:
    HOST = config("HOST", "0.0.0.0")
    PORT = int(config("PORT", 8000))
    DEBUG = config("DEBUG", "false").lower() == "true"

    # MongoDB configuration
    DATABASE_URI = config("MONGODB_URI")
    OPENAI_API_KEY = config("OPENAI_API_KEY")


settings = Settings()
