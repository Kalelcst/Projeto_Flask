from functools import wraps
from flask import session, redirect, flash
from models import User

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
            flash('Usuário inválido.', 'danger')
            return redirect('/login')

        if not user.is_admin:
            flash('Acesso restrito para administradores.', 'danger')
            return redirect('/')

        return f(*args, **kwargs)

    return decorated