from flask import Flask
from models import db
import os
import secrets
from flask_wtf import CSRFProtect
from flask_migrate import Migrate

csrf = CSRFProtect()
migrate = Migrate()


def get_or_create_secret_key(app):

    env_key = os.environ.get("SECRET_KEY")
    if env_key:
        return env_key

    if os.environ.get("FLASK_ENV") == "production":
        raise RuntimeError(
            "SECRET_KEY não definida. Configure a variável de ambiente "
            "SECRET_KEY antes de rodar em produção."
        )

    os.makedirs(app.instance_path, exist_ok=True)
    key_path = os.path.join(app.instance_path, "secret_key")

    if os.path.exists(key_path):
        with open(key_path, "r") as f:
            return f.read().strip()

    key = secrets.token_hex(32)
    with open(key_path, "w") as f:
        f.write(key)

    return key


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SECRET_KEY"] = get_or_create_secret_key(app)
    app.config["SESSION_COOKIE_SECURE"] = os.environ.get("FLASK_ENV") == "production"
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from routes.auth_routes import auth
    from routes.task_routes import task
    from routes.user_routes import user
    from routes.admin_routes import admin
    from api import api as api_bp

    app.register_blueprint(auth)
    app.register_blueprint(task)
    app.register_blueprint(user)
    app.register_blueprint(admin)
    app.register_blueprint(api_bp)

    csrf.exempt(api_bp)

    return app


app = create_app()


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"

    app.run(
        debug=debug_mode,
        host="0.0.0.0",
        port=5000
    )