from functools import wraps
from flask import session, redirect

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        if not session.get('user_id'):
            return redirect('/login')

        return f(*args, **kwargs)

    return decorated