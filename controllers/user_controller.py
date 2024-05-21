from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import create_access_token
from flask_login import login_user

from models import Account
from models.user_model import db, User
import uuid

user = Blueprint('user', __name__)

@user.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(name=data['name'], login=data['login'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    # Criar uma conta de investimentos para o novo usuário
    new_account = Account(user_id=new_user.id)
    db.session.add(new_account)
    db.session.commit()

    return jsonify({'Sucesso': 'Criado o Usuário com Login: ' +new_user.login}), 201


@user.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(login=data['login']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        access_token = create_access_token(identity=data['login'])
        return jsonify({'Sucesso': 'Login Realizado', 'token': access_token}), 200
    return jsonify({'Erro': 'Login/Senha Inválida'}), 401

@user.route('/allusers', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'login': user.login} for user in users])

@user.route('/update/<id>', methods=['PUT'])
def update_user(id):
    try:
        uid = uuid.UUID(id)
    except ValueError:
        abort(400, "Invalid UUID")

    user = User.query.get(uid)
    if user:
        data = request.get_json()
        new_login = data.get('login')
        new_password = data.get('password')
        if new_login:
            user.login = new_login
        if new_password:
            user.set_password(new_password)
        db.session.commit()
        return jsonify({'Sucesso': 'Usuário atualizado'}), 200
    return jsonify({'Erro': 'Usuário não encontrado'}), 404

@user.route('/data/<id>', methods=['GET'])
def get_user(id):
    try:
        uid = uuid.UUID(id)
    except ValueError:
        abort(400, "Invalid UUID")

    user = User.query.get(uid)
    if user:
        account = {
            'id': user.account.id,
            'user_id': user.account.user_id,
            'balance': user.account.balance,
            'crypto': user.account.crypto_investment_balance,
            'stocks': user.account.stock_investment_balance}
        return jsonify({'id': user.id, 'name': user.name, 'login': user.login, 'password': user.password_hash, 'account': account}), 200
    return jsonify({'Erro': 'Usuário não encontrado'}), 404


@user.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        uid = uuid.UUID(id)
    except ValueError:
        abort(400, "UUID Inválido")

    user = User.query.get(uid)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'Sucesso': 'Usuário excluído'}), 200
    return jsonify({'Erro': 'Usuário não encontrado'}), 404