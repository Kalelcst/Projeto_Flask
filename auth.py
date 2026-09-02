from functools import wraps
from flask import request, current_app
import jwt
import logging

from models import User

logger = logging.getLogger(__name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get('Authorization')

        if not token:
            return {'message': 'Token não fornecido'}, 401

        try:
            parts = token.split()
            if len(parts) != 2:
                return {'message': 'Formato inválido'}, 401

            token = parts[1]

            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])

            current_user = User.query.filter_by(id=data['user_id']).first()

            if not current_user:
                return {'message': 'Usuário não encontrado'}, 404

        except jwt.ExpiredSignatureError:
            return {'message': 'Token expirado'}, 401

        except jwt.InvalidTokenError:
            return {'message': 'Token inválido'}, 401

        except Exception:
            # Loga o detalhe internamente, mas nunca expõe pro cliente
            logger.exception("Erro inesperado ao validar token JWT")
            return {'message': 'Não foi possível validar o token'}, 401

        return f(current_user, *args, **kwargs)

    return decorated