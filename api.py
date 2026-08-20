from flask import Blueprint, request, current_app
from datetime import datetime, timedelta, timezone
import jwt
from werkzeug.security import check_password_hash

from models import db, User, Todo
from auth import token_required

api = Blueprint('api', __name__, url_prefix='/api')


# PROFILE
@api.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return {'id': current_user.id, 'name': current_user.name, 'email': current_user.email}


# CREATE TASK
@api.route('/tasks', methods=['POST'])
@token_required
def create_task(current_user):

    data = request.get_json()
    content = data.get('content')

    if not content:
        return {'message': 'Conteúdo obrigatório'}, 400

    new_task = Todo(content=content, user_id=current_user.id)

    db.session.add(new_task)
    db.session.commit()

    return {'message': 'Tarefa criada com sucesso', 'task_id': new_task.id}, 201


# GET TASKS
@api.route('/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):

    tasks = Todo.query.filter_by(user_id=current_user.id).all()

    return [
        {'id': task.id, 'content': task.content}
        for task in tasks
    ]


# UPDATE TASK
@api.route('/tasks/<int:id>', methods=['PUT'])
@token_required
def update_task(current_user, id):

    task = Todo.query.filter_by(id=id, user_id=current_user.id).first()

    if not task:
        return {'message': 'Tarefa não encontrada'}, 404

    data = request.get_json()
    content = data.get('content')

    if not content:
        return {'message': 'Conteúdo obrigatório'}, 400

    task.content = content
    db.session.commit()

    return {'message': 'Tarefa atualizada com sucesso'}


# DELETE TASK
@api.route('/tasks/<int:id>', methods=['DELETE'])
@token_required
def delete_task(current_user, id):

    task = Todo.query.filter_by(id=id, user_id=current_user.id).first()

    if not task:
        return {'message': 'Tarefa não encontrada'}, 404

    db.session.delete(task)
    db.session.commit()

    return {'message': 'Tarefa excluída com sucesso'}


# LOGIN (JWT)
@api.route('/login', methods=['POST'])
def api_login():

    data = request.get_json()

    if not data:
        return {'message': 'JSON inválido'}, 400

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return {'message': 'Credenciais inválidas'}, 401

    token = jwt.encode(
        {
            'user_id': user.id,
            'exp': datetime.now(timezone.utc) + timedelta(hours=1)
        },
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return {'token': token}