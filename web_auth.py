from functools import wraps
from flask import session, redirect, flash

from models import User


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        if not session.get('user_id'):
            flash('Faça login para continuar.', 'warning')
            return redirect('/login')

        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        user_id = session.get('user_id')

        if not user_id:
            flash('Faça login para continuar.', 'warning')
            return redirect('/login')

        user = User.query.get(user_id)

        if not user:
            session.clear()
            flash('Usuário não encontrado.', 'danger')
            return redirect('/login')

        if not user.is_admin:
            flash('Acesso restrito para administradores.', 'danger')
            return redirect('/')

        return f(*args, **kwargs)

    return decorated