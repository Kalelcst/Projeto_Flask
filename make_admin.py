# make_admin.py
import sys
from app import app
from models import db, User

def make_admin(email):
    with app.app_context():
        user = User.query.filter_by(email=email).first()

        if user:
            user.is_admin = True
            db.session.commit()
            print(f"Usuário {email} promovido a administrador com sucesso!")
        else:
            print(f"Usuário com email {email} não encontrado!")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python make_admin.py <email>")
        sys.exit(1)

    make_admin(sys.argv[1])