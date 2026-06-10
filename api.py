from flask import request
from datetime import datetime, timedelta
import jwt
from werkzeug.security import check_password_hash

from app import app

print("API APP ID:", id(app))

from models import db, User, Todo
from auth import token_required


@app.route('/api/profile')
@token_required
def profile(current_user):

    if not current_user:
        return {'message': 'Usuário não encontrado'}, 404
    
    return {'id': current_user.id, 'name': current_user.name, 'email': current_user.email}


@app.route('/api/tasks', methods=['POST'])
@token_required
def create_task(current_user):

    data = request.get_json()

    content = data.get('content')

    if not content:
        return {'message': 'Conteúdo obrigatório'}, 400

    new_task = Todo(
        content=content,
        user_id=current_user.id
    )

    db.session.add(new_task)
    db.session.commit()

    return {
        'message': 'Tarefa criada com sucesso',
        'task_id': new_task.id
    }, 201


@app.route('/api/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):

    tasks = Todo.query.filter_by(
        user_id=current_user.id
    ).all()

    return [
        {
            'id': task.id,
            'content': task.content
        }
        for task in tasks
    ]


@app.route('/api/tasks/<int:id>', methods=['PUT'])
@token_required
def update_task(current_user, id):

    task = Todo.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first()

    if not task:
        return {'message': 'Tarefa não encontrada'}, 404

    data = request.get_json()

    content = data.get('content')

    if not content:
        return {'message': 'Conteúdo obrigatório'}, 400

    task.content = content

    db.session.commit()

    return {
        'message': 'Tarefa atualizada com sucesso'
    }


@app.route('/api/tasks/<int:id>', methods=['DELETE'])
@token_required
def delete_task(current_user, id):

    task = Todo.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first()

    if not task:
        return {'message': 'Tarefa não encontrada'}, 404

    db.session.delete(task)
    db.session.commit()

    return {
        'message': 'Tarefa excluída com sucesso'
    }


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data:
        return {'message': 'JSON inválido'}, 400
    
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return {'message': 'Usuário não encontrado'}, 404

    if not check_password_hash(
        user.password,
        password
    ):
        return {'message': 'Senha inválida'}, 401

    token = jwt.encode(
        {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=1)
        },
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return {'token': token}

print("API ROTAS REGISTRADAS")
print(app.url_map)