from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy.orm import relationship

from models import db

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    user = relationship("User", back_populates="account")
    balance = db.Column(db.Float, default=0.00) # Saldo da conta
    crypto_investment_balance = db.Column(db.Float, default=0.00)  # Saldo de investimentos em criptomoedas
    stock_investment_balance = db.Column(db.Float, default=0.00)  # Saldo de investimentos em ações