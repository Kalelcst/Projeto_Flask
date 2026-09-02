import os
import tempfile

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from models import db as _db, User


@pytest.fixture
def app():
    """Cria a aplicação com um banco SQLite temporário e isolado
    para cada teste, evitando que um teste interfira no outro."""

    db_fd, db_path = tempfile.mkstemp(suffix=".sqlite")

    flask_app = create_app("testing")
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    with flask_app.app_context():
        _db.create_all()

    yield flask_app

    with flask_app.app_context():
        _db.session.remove()
        _db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Cliente HTTP de teste — simula um navegador/API client."""
    return app.test_client()


@pytest.fixture
def create_user(app):
    """Fábrica para criar usuários direto no banco de teste."""

    def _create_user(name="Usuário Teste", email="user@teste.com",
                      password="senha123", is_admin=False):
        with app.app_context():
            user = User(
                name=name,
                email=email,
                password=generate_password_hash(password),
                is_admin=is_admin,
            )
            _db.session.add(user)
            _db.session.commit()
            return user.id

    return _create_user


@pytest.fixture
def login_web(client, create_user):
    """Cria um usuário comum e faz login via formulário web.
    Retorna o id do usuário logado."""

    user_id = create_user(email="user@teste.com", password="senha123")

    client.post(
        "/login",
        data={"email": "user@teste.com", "password": "senha123"},
        follow_redirects=True,
    )

    return user_id


@pytest.fixture
def login_admin_web(client, create_user):
    """Cria um usuário admin e faz login via formulário web."""

    user_id = create_user(
        name="Admin Teste",
        email="admin@teste.com",
        password="senha123",
        is_admin=True,
    )

    client.post(
        "/login",
        data={"email": "admin@teste.com", "password": "senha123"},
        follow_redirects=True,
    )

    return user_id


@pytest.fixture
def api_token(client, create_user):
    """Cria um usuário e retorna um token JWT válido para ele."""

    create_user(email="api@teste.com", password="senha123")

    response = client.post(
        "/api/login",
        json={"email": "api@teste.com", "password": "senha123"},
    )

    return response.get_json()["token"]