from app import app
from models import db, User

with app.app_context():

    user = User.query.filter_by(
        email='kalelcst@gmail.com'
    ).first()

    if user:
        user.is_admin = True
        db.session.commit()
        print('Administrador criado com sucesso!')
    else:
        print('Usuário não encontrado!')