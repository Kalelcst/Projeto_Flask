from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.id}>'
        
@app.route('/health')
def health():
    return {'status': 'ok'}

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

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




@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_user = User(name=name, email=email)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/users')

        except:
            return 'Erro ao cadastrar usuário.'

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


if __name__ == '__main__':  
    app.run(debug=True, host='0.0.0.0', port=5000)