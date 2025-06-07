import os
"""
to use an external database simply create a .env file
and inside give value to

DATABASE_URL="your-database-url"

for render and supabase simply login to your account and get
the required url from those sites and asssign it to DATABASE_URL as
shown above
"""

class Config:
    SECRET_KEY = "your-secret-key-here"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'upload'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///test.db")
    SECRET_KEY = 'test'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
