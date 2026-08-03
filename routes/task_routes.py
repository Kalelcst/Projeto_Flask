from flask import Blueprint, render_template, request, redirect, session, flash
from sqlalchemy import or_

from models import db, Todo
from web_auth import login_required

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

        if not content:
            flash("A tarefa não pode ficar vazia.", "danger")
            return redirect("/")

        new_task = Todo(
            content=content,
            user_id=user_id
        )

        db.session.add(new_task)
        db.session.commit()

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

        if not content:
            flash("A tarefa não pode ficar vazia.", "danger")
            return redirect(f"/update/{id}")

        task.content = content

        db.session.commit()

        flash("Tarefa atualizada com sucesso!", "success")

        return redirect("/")

    return render_template(
        "update.html",
        task=task
    )


# ======================================
# EXCLUIR
# ======================================
@task.route("/delete/<int:id>")
@login_required
def delete(id):

    user_id = session.get("user_id")

    task = Todo.query.filter_by(
        id=id,
        user_id=user_id
    ).first_or_404()

    db.session.delete(task)
    db.session.commit()

    flash("Tarefa excluída com sucesso!", "success")

    return redirect("/")


# ======================================
# MOVER NO KANBAN
# ======================================
@task.route("/move-task/<int:id>/<status>")
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

    task.status = status

    db.session.commit()

    flash("Status atualizado!", "success")

    return redirect("/")