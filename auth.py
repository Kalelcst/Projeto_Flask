from functools import wraps
from flask import request
import jwt

# from app import app
from models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get('Authorization')

        print("HEADER RECEBIDO:", token)

        if not token:
            return {'message': 'Token não fornecido'}, 401

        try:
            parts = token.split()
            if len(parts) != 2:
                return {'message': 'Formato inválido'}, 401
            token = parts[1]

            data = jwt.decode(
                token, "minha-chave-super-secreta", algorithms=['HS256'])

            current_user = User.query.get(data['user_id'])

            if not current_user:
                return {'message': 'Usuário não encontrado'}, 404

        except Exception as e:
            print("ERRO JWT:", e)
            return {'message': str(e)}, 401

        return f(current_user, *args, **kwargs)
    return decorated
