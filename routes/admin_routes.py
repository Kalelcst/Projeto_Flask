from flask import Blueprint, render_template, redirect, flash, session

from models import User, Todo
from web_auth import login_required, admin_required
from services.admin_service import AdminService

admin = Blueprint("admin", __name__)


@admin.route("/admin/dashboard")
@login_required
@admin_required
def dashboard():

    stats = AdminService.get_dashboard_stats()

    return render_template(
        "admin_dashboard.html",
        total_users=stats["total_users"],
        total_tasks=stats["total_tasks"],
        todo_tasks=stats["todo_tasks"],
        doing_tasks=stats["doing_tasks"],
        done_tasks=stats["done_tasks"],
        admin_users=stats["admin_users"]
    )


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


@admin.route("/admin/user/delete/<int:id>", methods=["POST"])
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

    AdminService.delete_user(user)

    flash(
        "Usuário excluído com sucesso!",
        "success"
    )

    return redirect("/admin/users")


@admin.route("/admin/user/toggle-admin/<int:id>", methods=["POST"])
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

    AdminService.toggle_admin(user)

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