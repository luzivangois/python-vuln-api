from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from.user_model import User
from.account_model import Account
from.documents_model import Document