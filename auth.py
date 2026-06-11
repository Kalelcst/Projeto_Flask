from functools import wraps
from flask import request, current_app
import jwt

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
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )

            current_user = User.query.filter_by(id=data['user_id']).first()

            if not current_user:
                return {'message': 'Usuário não encontrado'}, 404

        except jwt.ExpiredSignatureError:
            return {'message': 'Token expirado'}, 401

        except jwt.InvalidTokenError:
            return {'message': 'Token inválido'}, 401

        except Exception as e:
            print("ERRO JWT:", e)
            return {'message': str(e)}, 401

        return f(current_user, *args, **kwargs)

    return decorated