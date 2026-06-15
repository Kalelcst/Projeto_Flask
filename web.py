from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Todo

web = Blueprint('web', __name__)


@web.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']

        user_id = session.get('user_id')

        if not user_id:
            return redirect('/login')

        new_task = Todo(content=task_content, user_id=user_id)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Ocorreu um problema ao adicionar sua tarefa.'

    else:
        user_id = session.get('user_id')
        if not user_id:
            return redirect('/login')

        tasks = Todo.query.filter_by(user_id=user_id).order_by(Todo.date_created).all()

        return render_template('index.html', tasks=tasks)


@web.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    user_id = session.get('user_id')

    if not user_id:
        return redirect('/login')

    task = Todo.query.filter_by(id=id, user_id=user_id).first_or_404()

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Ocorreu um problema ao atualizar sua tarefa.'

    return render_template('update.html', task=task)


@web.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name

            return redirect('/')

        return 'Email ou senha inválidos.'

    return render_template('login.html')


@web.route('/users', methods=['GET', 'POST'])
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

    users = User.query.order_by(User.date_created).all()
    return render_template('users.html', users=users)


@web.route('/user/update/<int:id>', methods=['GET', 'POST'])
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

    return render_template('update_user.html', user=user)


@web.route('/user/delete/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)

    try:
        db.session.delete(user)
        db.session.commit()
        return redirect('/users')
    except:
        return 'Erro ao excluir usuário.'


@web.route('/delete/<int:id>')
def delete(id):

    user_id = session.get('user_id')

    if not user_id:
        return redirect('/login')

    task_to_delete = Todo.query.filter_by(id=id, user_id=user_id).first_or_404()

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Ocorreu um problema ao excluir sua tarefa.'


@web.route('/logout')
def logout():
    session.clear()
    return redirect('/login')