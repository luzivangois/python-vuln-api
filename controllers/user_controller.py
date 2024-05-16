from flask import Blueprint, request, jsonify, abort
from flask_login import login_user
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
    return jsonify({'Status': 'Usuário Registrado com Sucesso!', 'Usuário': new_user.login}), 201

@user.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(login=data['login']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'message': 'logged in successfully'})
    return jsonify({'message': 'invalid username or password'}), 401

@user.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'login': user.login} for user in users])

@user.route('/user/<id>', methods=['GET'])
def get_user(id):
    try:
        uid = uuid.UUID(id)
    except ValueError:
        abort(400, "Invalid UUID")

    user = User.query.get(uid)
    if user:
        return jsonify({'id': user.id, 'name': user.name, 'login': user.login, 'password': user.password_hash})
    return jsonify({'message': 'user not found'}), 404