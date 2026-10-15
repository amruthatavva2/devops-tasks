import os


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./projectpulse.db")
APP_NAME = "ProjectPulse API"
