from flask import Blueprint, render_template, request, redirect, session, flash

from models import db, User
from web_auth import login_required

user = Blueprint("user", __name__)


# ======================================
# PERFIL
# ======================================
@user.route("/users")
@login_required
def users():

    user_id = session.get("user_id")

    user = User.query.get_or_404(user_id)

    return render_template(
        "users.html",
        users=[user]
    )


# ======================================
# EDITAR PERFIL
# ======================================
@user.route("/user/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_user(id):

    user_id = session.get("user_id")

    if user_id != id:
        flash("Acesso negado.", "danger")
        return redirect("/users")

    user = User.query.get_or_404(id)

    if request.method == "POST":

        name = request.form["name"].strip()
        email = request.form["email"].strip()

        if not name:
            flash("Nome é obrigatório.", "danger")
            return redirect(f"/user/update/{id}")

        if not email:
            flash("Email é obrigatório.", "danger")
            return redirect(f"/user/update/{id}")

        existing_user = User.query.filter(
            User.email == email,
            User.id != id
        ).first()

        if existing_user:
            flash("Este email já está cadastrado.", "danger")
            return redirect(f"/user/update/{id}")

        user.name = name
        user.email = email

        db.session.commit()

        session["user_name"] = user.name

        flash("Perfil atualizado com sucesso!", "success")

        return redirect("/users")

    return render_template(
        "update_user.html",
        user=user
    )



@user.route("/user/delete/<int:id>", methods=["POST"])
@login_required
def delete_user(id):

    user_id = session.get("user_id")

    if id != user_id:
        flash("Acesso negado.", "danger")
        return redirect("/users")

    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    session.clear()

    flash(
        "Sua conta foi excluída com sucesso.",
        "success"
    )

    return redirect("/register")