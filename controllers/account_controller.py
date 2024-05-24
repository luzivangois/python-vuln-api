from flask import Blueprint, request
from reportlab.pdfgen import canvas

from models import db, Account
import uuid
from flask import send_file

account = Blueprint('account', __name__)

@account.route('/deposit/<account_id>', methods=['POST'])
def deposit(account_id):
    data = request.get_json()
    account = Account.query.get(uuid.UUID(account_id))
    if not account:
        return {'ERRO': 'Conta não encontrada!'}, 404
    try:
        amount = float(data.get('amount'))
    except (TypeError, ValueError):
        return {'ERRO': 'Valor inválido'}, 400
    account.balance += amount
    db.session.commit()
    return 'Adicionado '+str(amount)+' ao saldo da conta '+account_id, 200

@account.route('/withdraw/<account_id>', methods=['POST'])
def withdraw(account_id):
    data = request.get_json()
    account = Account.query.get(uuid.UUID(account_id))
    if not account:
        return {'ERRO': 'Conta não encontrada'}, 404
    try:
        amount = float(data.get('amount'))
    except (TypeError, ValueError):
        return {'ERRO': 'Valor inválido'}, 400
    account.balance -= amount
    db.session.commit()
    return 'Efetuado o saque de ' +str(amount)+' da conta '+account_id, 200

@account.route('/balance/<account_id>', methods=['GET'])
def balance(account_id):
    account = Account.query.get(uuid.UUID(account_id))
    if not account:
        return {'ERRO': 'Conta não encontrada'}, 404
    return 'O saldo atual da conta ' +account_id+' é: '+str(account.balance), 200

@account.route('/invest_crypto/<account_id>', methods=['POST'])
def invest(account_id):
    data = request.get_json()
    account = Account.query.get(uuid.UUID(account_id))
    if not account:
        return {'ERRO': 'Conta não encontrada'}, 404
    try:
        investment_amount = float(data.get('amount'))
    except (TypeError, ValueError):
        return {'ERRO': 'Valor inválido'}, 400
    if account.balance < investment_amount:
        return {'ERRO': 'Saldo insuficiente'}, 400
    account.balance -= investment_amount
    account.crypto_investment_balance += investment_amount
    db.session.commit()
    return 'Investido '+str(investment_amount)+' em criptomoedas', 200

@account.route('/invest_stocks/<account_id>', methods=['POST'])
def invest_stocks(account_id):
    data = request.get_json()
    account = Account.query.get(uuid.UUID(account_id))
    if not account:
        return {'ERRO': 'Conta não encontrada'}, 404
    try:
        investment_amount = float(data.get('amount'))
    except (TypeError, ValueError):
        return {'ERRO': 'Valor inválido'}, 400
    if account.balance < investment_amount:
        return {'ERRO': 'Saldo insuficiente'}, 400
    account.balance -= investment_amount
    account.stock_investment_balance += investment_amount
    db.session.commit()
    return 'Investido '+str(investment_amount)+' em ações da bolsa', 200

@account.route('/total_investments/<account_id>', methods=['GET'])
def total_investments(account_id):
    account = Account.query.get(uuid.UUID(account_id))
    if not account:
        return {'ERRO': 'Conta não encontrada'}, 404

    return {
        'OK': 'O saldo total de investimentos é '+str(account.crypto_investment_balance+account.stock_investment_balance),
        'Investimento em Criptomoedas': str(account.crypto_investment_balance),
        'Investimento em Ações da Bolsa': str(account.stock_investment_balance)
    }, 200

@account.route('/investment_statement/<account_id>', methods=['GET'])
def investment_statement(account_id):
    account = Account.query.get(uuid.UUID(account_id))
    if not account:
        return {'ERRO': 'Conta não encontrada'}, 404

    total_balance = account.crypto_investment_balance + account.stock_investment_balance

    # Cria o PDF
    pdf_filename = 'extrato_investimentos.pdf'
    c = canvas.Canvas(pdf_filename, pagesize='letter')
    c.drawString(230, 750, 'Extrato de Investimentos')
    c.drawString(100, 720, f'ID da Conta: {account.id}')
    c.drawString(100, 700, f'ID do Titular da Conta: {account.user.id}')
    c.drawString(100, 680, f'Saldo de Criptomoedas: R$ {account.crypto_investment_balance:.2f}')
    c.drawString(100, 660, f'Saldo de Ações: R$ {account.stock_investment_balance:.2f}')
    c.drawString(100, 640, f'Saldo Total: R$ {total_balance:.2f}')
    c.save()

    # Retorna o arquivo PDF para download
    return send_file(pdf_filename, as_attachment=True)