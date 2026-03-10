import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me')

    # Use SQLite for development
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///train_booking.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
