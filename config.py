import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database/invest.db')
    SECRET_KEY = secrets.token_urlsafe(32)
    UPLOAD_FOLDER = os.path.join(basedir)