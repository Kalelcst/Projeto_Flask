from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'minha-chave-super-secreta'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(255), nullable=False)

    tasks = db.relationship('Todo', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.id}>'
        
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get('Authorization')

        print("HEADER RECEBIDO:", token)

        if not token:
            return {'message': 'Token não fornecido'}, 401

        try:
            token = token.split(" ")[1]

            data = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms=['HS256']
            )

            current_user = User.query.get(data['user_id'])

        except Exception as e:
            print("ERRO JWT:", e)
            return {'message': str(e)}, 401

        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/profile')
@token_required
def profile(current_user):

    if not current_user:
        return {'message': 'Usuário não encontrado'}, 404
    
    return {'id': current_user.id, 'name': current_user.name, 'email': current_user.email}

@app.route('/api/tasks', methods=['POST'])
@token_required
def create_task(current_user):

    data = request.get_json()

    content = data.get('content')

    if not content:
        return {'message': 'Conteúdo obrigatório'}, 400

    new_task = Todo(
        content=content,
        user_id=current_user.id
    )

    db.session.add(new_task)
    db.session.commit()

    return {
        'message': 'Tarefa criada com sucesso',
        'task_id': new_task.id
    }, 201

@app.route('/api/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):

    tasks = Todo.query.filter_by(
        user_id=current_user.id
    ).all()

    return [
        {
            'id': task.id,
            'content': task.content
        }
        for task in tasks
    ]

@app.route('/health')
def health():
    return {'status': 'ok'}


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content, user_id=1)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Ocorreu um problema ao adicionar sua tarefa.'


    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Ocorreu um problema ao excluir sua tarefa.'
    

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Ocorreu um problema ao atualizar sua tarefa.'
        
    else:
        return render_template('update.html', task=task)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(
            user.password,
            password
        ):
            return f' {user.name}!'

        return 'Email ou senha inválidos.'

    return render_template('login.html')


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/users')

        except Exception as e:
            print(e)
            return str(e)

    else:
        users = User.query.order_by(User.date_created).all()
        return render_template('users.html', users=users)
    

@app.route('/user/delete/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()

        return redirect('/users')

    except:
        return 'Erro ao excluir usuário.'
    

@app.route('/user/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':

        user.name = request.form['name']
        user.email = request.form['email']

        try:
            db.session.commit()
            return redirect('/users')

        except:
            return 'Erro ao atualizar usuário.'

    return render_template('update_user.html',user=user)


@app.route('/api/login', methods=['POST'])
def api_login():

    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return {'message': 'Usuário não encontrado'}, 404

    if not check_password_hash(
        user.password,
        password
    ):
        return {'message': 'Senha inválida'}, 401

    token = jwt.encode(
        {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=1)
        },
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return {'token': token}

if __name__ == '__main__':  
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

    