from flask import Flask
from models import db
app = Flask(__name__)

# print("APP.PY ID:", id(app))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'minha-chave-super-secreta'

db.init_app(app)



@app.route('/health')
def health():
    return {'status': 'ok'}

import web
import api

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )

print("APP FINAL:")
print(app.url_map)