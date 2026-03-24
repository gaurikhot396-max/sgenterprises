import os

class Config:
    SECRET_KEY = "secret123"

    SQLALCHEMY_DATABASE_URI = "sqlite:///lms.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ---------------- MAIL CONFIG ----------------
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "yourgmail@gmail.com"
    MAIL_PASSWORD = "your_app_password"