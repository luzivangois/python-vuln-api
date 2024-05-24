import os

from flask import Blueprint, request, jsonify, abort
from flask_login import login_user

import services.jwt_service
from flask import current_app
from models import Account, Document
from models.user_model import db, User
import uuid

from services.document_service import allowed_file, save_to_db

user = Blueprint('user', __name__)

@user.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    existing_user = User.query.filter_by(login=data['login']).first()

    # Verificar se o usuário já existe
    if existing_user:
        return jsonify({'ERRO': 'Usuário já cadastrado no sistema!'}), 400

    new_user = User(name=data['name'], login=data['login'], role=data['role'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    # Criar uma conta de investimentos para o novo usuário
    new_account = Account(user_id=new_user.id)
    db.session.add(new_account)
    db.session.commit()

    return 'Usuário '+new_user.login+' criado com Sucesso', 201



@user.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(login=data['login']).first()
    if user:
        if user.check_password(data['password']):
            login_user(user)
            access_token = services.jwt_service.create_access_token_user(user=user)
            return {'OK':'Login realizado com Sucesso.', 'token': access_token}, 200
        else:
            return 'Senha inválida!', 401
    else:
        return 'Usuário não encontrado!', 404


@user.route('/allusers', methods=['GET'])
# @jwt_required()
def get_all_users():
    token = request.headers.get('Authorization')

    claims = services.jwt_service.get_user_role(token)

    if claims != 'admin':
        return 'Usuário sem permissão para consultar os dados solicitados.', 403

    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'login': user.login} for user in users])


@user.route('/data/<id>', methods=['GET'])
def get_user(id):
    try:
        uid = uuid.UUID(id)
    except ValueError:
        abort(400, "UUID Inválido!")

    user = User.query.get(uid)
    if user:
        account = {
            'id': user.account.id,
            'user_id': user.account.user_id,
            'balance': user.account.balance,
            'crypto': user.account.crypto_investment_balance,
            'stocks': user.account.stock_investment_balance}
        return jsonify({'id': user.id, 'name': user.name, 'login': user.login, 'password': user.password_hash, 'role': user.role, 'account': account}), 200
    return 'Usuário não encontrado', 404

@user.route('/update/<id>', methods=['PUT'])
def update_user(id):
    try:
        uid = uuid.UUID(id)
    except ValueError:
        abort(400, "UUID Inválido")

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
        return 'Usuário atualizado com Sucesso.', 200
    return 'Usuário não encontrado', 404


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
        return 'Usuário excluído com sucesso', 200
    return 'Usuário não encontrado', 404


@user.route('/documents', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Nenhum arquivo encontrado', 400
        file = request.files['file']
        if file.filename == '':
            return 'Nenhum documento selecionado', 400
        if file and allowed_file(file.filename):
            name = request.form.get('name', None)
            if not name:
                return 'Nome do documento em branco', 400
            filename = name
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            check_file_exists_in_db = Document.query.filter_by(filename=filename).first()
            if check_file_exists_in_db:
                return 'Já existe arquivo salvo com o nome '+filename, 400
            file.save(filepath)
            document_id, saved_path = save_to_db(filename, filepath)
            return jsonify(
                {'OK': 'Documento ' + filename + ' enviado com sucesso', 'id': document_id, 'path': saved_path}), 200