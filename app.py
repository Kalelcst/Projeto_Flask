from flask import Flask
from models import db
import os
from flask_wtf import CSRFProtect
from flask_migrate import Migrate

csrf = CSRFProtect()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        "chave-dev-temporaria"
    )

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