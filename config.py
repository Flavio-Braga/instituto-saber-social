import os


class Config:
    """Application configuration. Override secrets via environment variables in production."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "instituto-saber-social-dev-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
