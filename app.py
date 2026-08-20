from flask import Flask
from models import db
import os
import secrets
from flask_wtf import CSRFProtect

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

    db.init_app(app)

    with app.app_context():

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

        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)