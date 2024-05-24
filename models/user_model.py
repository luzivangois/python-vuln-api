from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from models import db

import hashlib

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(64), index=True)
    login = db.Column(db.String(64), unique=True)
    role = db.Column(db.String(13))
    password_hash = db.Column(db.String(128))
    account = relationship("Account", uselist=False, back_populates="user")

    def set_password(self, password):
        self.password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()

    def check_password(self, password):
        return self.password_hash == hashlib.md5(password.encode('utf-8')).hexdigest()
