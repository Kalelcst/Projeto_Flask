from flask import Flask
from extensions import db

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY'] = 'minha-chave-super-secreta'

    db.init_app(app)

    with app.app_context():
        from web import web as web_bp
        from api import api as api_bp

        app.register_blueprint(web_bp)
        app.register_blueprint(api_bp)

        db.create_all()

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)