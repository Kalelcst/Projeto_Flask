from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Todo
from web_auth import login_required, admin_required

web = Blueprint('web', __name__)


@web.route('/', methods=['POST', 'GET'])
@login_required
def index():

    user_id = session.get('user_id')

    search = request.args.get('search')

    query = Todo.query.filter_by(user_id=user_id)

    if search:
        query = query.filter(Todo.content.contains(search))

    tasks = query.order_by(Todo.date_created).all()

    if request.method == 'POST':
        task_content = request.form['content']

        if not task_content.strip():
            flash('A tarefa não pode ficar vazia.', 'danger')
            return redirect('/')

        new_task = Todo(content=task_content, user_id=user_id, status='todo')

        db.session.add(new_task)
        db.session.commit()

        flash('Tarefa criada com sucesso!', 'success')
        return redirect('/')

    return render_template('index.html', tasks=tasks, search=search)


@web.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):

    user_id = session.get('user_id')

    task = Todo.query.filter_by(id=id, user_id=user_id).first_or_404()

    if request.method == 'POST':
        content = request.form['content']

        if not content.strip():
            flash('A tarefa não pode ficar vazia.', 'danger')
            return redirect(f'/update/{id}')

        task.content = content
        try:
            db.session.commit()
            flash('Tarefa atualizada com sucesso!', 'success')
            return redirect('/')
        except Exception as e:
            print(e)
            return 'Ocorreu um problema ao atualizar sua tarefa.'

    return render_template('update.html', task=task)


@web.route('/login', methods=['GET', 'POST'])
def login():

    if session.get('user_id'):
        return redirect('/')
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['is_admin'] = user.is_admin
            
            flash(f'Bem-vindo, {user.name}!', 'success')
            return redirect('/')

        flash('Email ou senha inválidos.', 'danger')
        return redirect('/login')

    return render_template('login.html')


@web.route('/users')
@login_required
def users():

    user_id = session.get('user_id')

    user = User.query.get_or_404(user_id)

    return render_template('users.html',users=[user])


@web.route('/user/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user(id):

    user_id = session.get('user_id')

    if user_id != id:
        flash('Acesso negado.', 'danger')
        return redirect('/users')

    user = User.query.get_or_404(id)

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']

        if not name.strip():
            flash('Nome é obrigatório.', 'danger')
            return redirect(f'/user/update/{id}')

        if not email.strip():
            flash('Email é obrigatório.', 'danger')
            return redirect(f'/user/update/{id}')

        existing_user = User.query.filter(User.email == email, User.id != id).first()

        if existing_user:
            flash('Este email já está em cadastrado!', 'danger')
            return redirect(f'/user/update/{id}')

        user.name = name
        user.email = email

        try:
            db.session.commit()
            flash('Usuário atualizado com sucesso!', 'success')
            return redirect('/users')
        except Exception as e:
            print(e)
            return 'Ocorreu um problema ao atualizar o usuário.'

    return render_template('update_user.html', user=user)


@web.route('/user/delete/<int:id>')
@login_required
def delete_user(id):

    user_id = session.get('user_id')

    if user_id == id:
        flash('Você não pode excluir sua própria conta.', 'danger')
        return redirect('/users')

    return 'Funcionalidade reservada para administradores.', 403


@web.route('/delete/<int:id>')
@login_required
def delete(id):

    user_id = session.get('user_id')

    task_to_delete = Todo.query.filter_by(id=id, user_id=user_id).first_or_404()

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash('Tarefa excluída com sucesso!', 'success')
        return redirect('/')
    except Exception as e:
            print(e)
            return 'Ocorreu um problema ao excluir sua tarefa.'


@web.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Logout realizado com sucesso.', 'info')
    return redirect('/login')

@web.route('/register', methods=['GET', 'POST'])
def register():

    if session.get('user_id'):
        return redirect('/')
    
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if not name.strip():
            flash('Nome é obrigatório.', 'danger')
            return redirect('/register')

        if not email.strip():
            flash('Email é obrigatório.', 'danger')
            return redirect('/register')


        if not password.strip():
            flash('Senha é obrigatória.', 'danger')
            return redirect('/register')

        if len(password.strip()) < 6:
            flash('A senha deve possuir pelo menos 6 caracteres.', 'danger')
            return redirect('/register')

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Este email já está cadastrado.', 'danger')
            return redirect('/register')

        hashed_password = generate_password_hash(password)

        new_user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        try:
            db.session.add(new_user)
            db.session.commit()

            flash('Conta criada com sucesso! Faça login.', 'success')
            return redirect('/login')

        except Exception as e:
            print(e)
            return str(e)

    return render_template('register.html')

@web.route('/admin/users')
@login_required
@admin_required
def admin_users():

    users = User.query.all()

    users_data = []

    for user in users:

        total_tasks = Todo.query.filter_by(user_id=user.id).count()

        completed_tasks = Todo.query.filter_by(
            user_id=user.id,
            completed=True
        ).count()

        users_data.append({
            'user': user,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks
        })

    return render_template(
        'admin_users.html',
        users_data=users_data
    )

@web.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():

    total_users = User.query.count()

    total_tasks = Todo.query.count()

    completed_tasks = Todo.query.filter_by(
        completed=True
    ).count()

    pending_tasks = Todo.query.filter_by(
        completed=False
    ).count()

    admin_users = User.query.filter_by(
        is_admin=True
    ).count()

    return render_template(
        'admin_dashboard.html',
        total_users=total_users,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        admin_users=admin_users
    )

@web.route('/toggle-task/<int:id>')
@login_required
def toggle_task(id):

    user_id = session.get('user_id')

    task = Todo.query.filter_by(
        id=id,
        user_id=user_id
    ).first_or_404()

    task.completed = not task.completed

    try:
        db.session.commit()

        if task.completed:
            flash('Tarefa concluída!', 'success')
        else:
            flash('Tarefa reaberta!', 'info')

    except Exception as e:
        print(e)
        flash('Erro ao atualizar tarefa.', 'danger')

    return redirect('/')

@web.route('/admin/user/delete/<int:id>')
@login_required
@admin_required
def admin_delete_user(id):

    user = User.query.get_or_404(id)

    user_id = session.get('user_id')

    if user.id == user_id:
        flash('Você não pode excluir sua própria conta.', 'danger')
        return redirect('/admin/users')

    try:
        db.session.delete(user)
        db.session.commit()
        flash('Usuário deletado com sucesso!', 'success')
        return redirect('/admin/users')

    except Exception as e:
        print(e)
        flash('Erro ao deletar usuário.', 'danger')
        return redirect('/admin/users')
    
@web.route('/admin/user/toggle-admin/<int:id>')
@login_required
@admin_required
def toggle_admin(id):

    user = User.query.get_or_404(id)

    user_id = session.get('user_id')

    if user.id == user_id:
        flash('Você não pode alterar seu próprio status de admin.', 'danger')
        return redirect('/admin/users')

    user.is_admin = not user.is_admin

    try:
        db.session.commit()

        if user.is_admin:
            flash('Usuário promovido a admin!', 'success')
        else:
            flash('Admin removido com sucesso!', 'info')

    except Exception as e:
        print(e)
        flash('Erro ao atualizar usuário.', 'danger')

    return redirect('/admin/users')

@web.route('/move-task/<int:id>/<string:status>')
@login_required
def move_task(id, status):

    user_id = session.get('user_id')

    task = Todo.query.filter_by(id=id, user_id=user_id).first_or_404()

    if status not in ['todo', 'doing', 'done']:
        flash('Status inválido.', 'danger')
        return redirect('/')

    task.status = status

    db.session.commit()

    flash('Tarefa movida com sucesso!', 'success')
    return redirect('/')