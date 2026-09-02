from flask import Blueprint, render_template, request, redirect, session, flash

from models import Todo
from web_auth import login_required
from services.task_service import TaskService

task = Blueprint("task", __name__)


# ======================================
# LISTAR + BUSCAR + CRIAR
# ======================================
@task.route("/", methods=["GET", "POST"])
@login_required
def index():

    user_id = session.get("user_id")

    if request.method == "POST":

        content = request.form["content"].strip()
        priority = request.form.get("priority", "media")

        if not content:
            flash("A tarefa não pode ficar vazia.", "danger")
            return redirect("/")

        TaskService.create_task(user_id, content, priority)

        flash("Tarefa criada com sucesso!", "success")

        return redirect("/")

    search = request.args.get("search", "").strip()

    query = Todo.query.filter_by(user_id=user_id)

    if search:
        query = query.filter(
            Todo.content.ilike(f"%{search}%")
        )

    tasks = query.order_by(Todo.date_created.desc()).all()

    return render_template(
        "index.html",
        tasks=tasks,
        search=search
    )


# ======================================
# EDITAR
# ======================================
@task.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):

    user_id = session.get("user_id")

    task = Todo.query.filter_by(
        id=id,
        user_id=user_id
    ).first_or_404()

    if request.method == "POST":

        content = request.form["content"].strip()
        priority = request.form.get("priority", task.priority)

        if not content:
            flash("A tarefa não pode ficar vazia.", "danger")
            return redirect(f"/update/{id}")

        TaskService.update_task(task, content, priority)

        flash("Tarefa atualizada com sucesso!", "success")

        return redirect("/")

    return render_template(
        "update.html",
        task=task
    )


# ======================================
# EXCLUIR
# ======================================
@task.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):

    user_id = session.get("user_id")

    task = Todo.query.filter_by(
        id=id,
        user_id=user_id
    ).first_or_404()

    TaskService.delete_task(task)

    flash("Tarefa excluída com sucesso!", "success")

    return redirect("/")


# ======================================
# MOVER NO KANBAN
# ======================================
@task.route("/move-task/<int:id>/<status>", methods=["POST"])
@login_required
def move_task(id, status):

    user_id = session.get("user_id")

    if status not in ["todo", "doing", "done"]:
        flash("Status inválido.", "danger")
        return redirect("/")

    task = Todo.query.filter_by(
        id=id,
        user_id=user_id
    ).first_or_404()

    TaskService.move_task(task, status)

    flash("Status atualizado!", "success")

    return redirect("/")