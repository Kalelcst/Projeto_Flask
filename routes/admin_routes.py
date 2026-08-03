from flask import Blueprint, render_template, redirect, flash, session

from models import db, User, Todo
from web_auth import login_required, admin_required

admin = Blueprint("admin", __name__)


# =========================
# Dashboard
# =========================
@admin.route("/admin/dashboard")
@login_required
@admin_required
def dashboard():

    total_users = User.query.count()

    total_tasks = Todo.query.count()

    todo_tasks = Todo.query.filter_by(status="todo").count()

    doing_tasks = Todo.query.filter_by(status="doing").count()

    done_tasks = Todo.query.filter_by(status="done").count()

    admin_users = User.query.filter_by(is_admin=True).count()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_tasks=total_tasks,
        todo_tasks=todo_tasks,
        doing_tasks=doing_tasks,
        done_tasks=done_tasks,
        admin_users=admin_users
    )


# =========================
# Lista de usuários
# =========================
@admin.route("/admin/users")
@login_required
@admin_required
def users():

    users = User.query.all()

    users_data = []

    for user in users:

        total_tasks = Todo.query.filter_by(
            user_id=user.id
        ).count()

        completed_tasks = Todo.query.filter_by(
            user_id=user.id,
            status="done"
        ).count()

        users_data.append({
            "user": user,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks
        })

    return render_template(
        "admin_users.html",
        users_data=users_data
    )


# =========================
# Excluir usuário
# =========================
@admin.route("/admin/user/delete/<int:id>")
@login_required
@admin_required
def delete_user(id):

    user = User.query.get_or_404(id)

    if user.id == session.get("user_id"):
        flash(
            "Você não pode excluir sua própria conta.",
            "danger"
        )
        return redirect("/admin/users")

    db.session.delete(user)
    db.session.commit()

    flash(
        "Usuário excluído com sucesso!",
        "success"
    )

    return redirect("/admin/users")


# =========================
# Tornar / remover admin
# =========================
@admin.route("/admin/user/toggle-admin/<int:id>")
@login_required
@admin_required
def toggle_admin(id):

    user = User.query.get_or_404(id)

    if user.id == session.get("user_id"):
        flash(
            "Você não pode alterar seu próprio nível de acesso.",
            "danger"
        )
        return redirect("/admin/users")

    user.is_admin = not user.is_admin

    db.session.commit()

    if user.is_admin:
        flash(
            "Usuário promovido para administrador.",
            "success"
        )
    else:
        flash(
            "Administrador removido.",
            "info"
        )

    return redirect("/admin/users")