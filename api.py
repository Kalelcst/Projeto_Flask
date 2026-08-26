from flask import Blueprint, request, current_app
from datetime import datetime, timedelta, timezone
import logging
import jwt
from werkzeug.security import check_password_hash

from models import db, User, Todo
from auth import token_required

logger = logging.getLogger(__name__)

api = Blueprint('api', __name__, url_prefix='/api')

VALID_PRIORITIES = ('baixa', 'media', 'alta')
MAX_CONTENT_LENGTH = 200


# Helpers de validação
def get_json_body():
    return request.get_json(silent=True)


def validate_content(data):
    content = data.get('content')

    if content is None:
        return None, 'Campo "content" é obrigatório'

    if not isinstance(content, str):
        return None, 'Campo "content" deve ser texto'

    content = content.strip()

    if not content:
        return None, 'Campo "content" não pode ficar vazio'

    if len(content) > MAX_CONTENT_LENGTH:
        return None, f'Campo "content" deve ter no máximo {MAX_CONTENT_LENGTH} caracteres'

    return content, None


def validate_priority(data):
    if 'priority' not in data:
        return None, None

    priority = data.get('priority')

    if priority not in VALID_PRIORITIES:
        return None, f'Campo "priority" deve ser um de: {", ".join(VALID_PRIORITIES)}'

    return priority, None


# Tratamento de erro do blueprint
@api.errorhandler(Exception)
def handle_unexpected_error(e):
    logger.exception("Erro inesperado na API")
    return {'message': 'Erro interno no servidor'}, 500


# PROFILE
@api.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return {
        'id': current_user.id,
        'name': current_user.name,
        'email': current_user.email
    }


# CREATE TASK
@api.route('/tasks', methods=['POST'])
@token_required
def create_task(current_user):

    data = get_json_body()

    if data is None:
        return {'message': 'JSON inválido ou ausente'}, 400

    content, error = validate_content(data)
    if error:
        return {'message': error}, 400

    priority, error = validate_priority(data)
    if error:
        return {'message': error}, 400

    new_task = Todo(
        content=content,
        user_id=current_user.id,
        priority=priority or 'media'
    )

    db.session.add(new_task)
    db.session.commit()

    return {
        'message': 'Tarefa criada com sucesso',
        'task_id': new_task.id
    }, 201


# GET TASKS
@api.route('/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):

    tasks = Todo.query.filter_by(user_id=current_user.id).all()

    return [
        {
            'id': task.id,
            'content': task.content,
            'status': task.status,
            'priority': task.priority
        }
        for task in tasks
    ]


# UPDATE TASK
@api.route('/tasks/<int:id>', methods=['PUT'])
@token_required
def update_task(current_user, id):

    task = Todo.query.filter_by(id=id, user_id=current_user.id).first()

    if not task:
        return {'message': 'Tarefa não encontrada'}, 404

    data = get_json_body()

    if data is None:
        return {'message': 'JSON inválido ou ausente'}, 400

    content, error = validate_content(data)
    if error:
        return {'message': error}, 400

    priority, error = validate_priority(data)
    if error:
        return {'message': error}, 400

    task.content = content

    if priority:
        task.priority = priority

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

    data = get_json_body()

    if data is None:
        return {'message': 'JSON inválido ou ausente'}, 400

    email = data.get('email')
    password = data.get('password')

    if not email or not isinstance(email, str):
        return {'message': 'Email é obrigatório'}, 400

    if not password or not isinstance(password, str):
        return {'message': 'Senha é obrigatória'}, 400

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