import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")

