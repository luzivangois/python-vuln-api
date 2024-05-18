from flask import Blueprint, request
from models import db, Account
import uuid

account = Blueprint('account', __name__)

@account.route('/deposit/<account_id>', methods=['POST'])
def deposit(account_id):
    data = request.get_json()
    account = Account.query.get(uuid.UUID(account_id))
    if not account:
        return {"ERRO": "Conta não encontrada"}, 404
    try:
        amount = float(data.get('amount'))
    except (TypeError, ValueError):
        return {"ERRO": "Valor inválido"}, 400
    account.balance += amount
    db.session.commit()
    return {"SUCESSO": "Adicionado "+str(amount)+" ao saldo da conta"}, 200

@account.route('/withdraw/<account_id>', methods=['POST'])
def withdraw(account_id):
    data = request.get_json()
    account = Account.query.get(uuid.UUID(account_id))
    if not account:
        return {"ERRO": "Conta não encontrada"}, 404
    try:
        amount = float(data.get('amount'))
    except (TypeError, ValueError):
        return {"ERRO": "Valor inválido"}, 400
    account.balance -= amount
    db.session.commit()
    return {"SUCESSO": "Retirado " +str(amount)+" do saldo da conta."}, 200