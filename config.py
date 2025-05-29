import os

class Config:
    """Configuration settings for the application."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-development-only'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///job_portal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
