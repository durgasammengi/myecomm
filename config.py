import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'  # Change this to a secure, random key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configure your mail server settings for password reset emails
    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'noreply@example.com'
    TWILIO_ACCOUNT_SID = 'AC912a89a85534513d221c5b2ab1973e75'
    TWILIO_AUTH_TOKEN = 'e54058d712b563aad9b36ec6ed0bfe3b'
    TWILIO_PHONE_NUMBER = '+18447591414'
