from models import db, User, Todo


class AdminService:

    @staticmethod
    def get_dashboard_stats():
        return {
            "total_users": User.query.count(),
            "total_tasks": Todo.query.count(),
            "todo_tasks": Todo.query.filter_by(status="todo").count(),
            "doing_tasks": Todo.query.filter_by(status="doing").count(),
            "done_tasks": Todo.query.filter_by(status="done").count(),
            "admin_users": User.query.filter_by(is_admin=True).count(),
        }

    @staticmethod
    def toggle_admin(user):
        user.is_admin = not user.is_admin
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user):
        db.session.delete(user)
        db.session.commit()