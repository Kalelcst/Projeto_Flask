from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


def utcnow():
    return datetime.now(timezone.utc)


class Todo(db.Model):
    __table_args__ = (
        db.CheckConstraint(
            "status IN ('todo', 'doing', 'done')",
            name="ck_todo_status_valido"
        ),
        db.CheckConstraint(
            "priority IN ('baixa', 'media', 'alta')",
            name="ck_todo_priority_valido"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    status = db.Column(db.String(20), nullable=False, default='todo')
    priority = db.Column(db.String(20), nullable=False, default='media')

    date_created = db.Column(db.DateTime, default=utcnow)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id}>'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=utcnow)

    is_admin = db.Column(db.Boolean, default=False)

    tasks = db.relationship(
        'Todo',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<User {self.id}>'