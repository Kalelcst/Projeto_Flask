from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import check_password_hash

from services.user_service import UserService

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():

    if session.get("user_id"):
        return redirect("/")

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = UserService.get_by_email(email)

        if user and check_password_hash(user.password, password):

            session["user_id"] = user.id
            session["user_name"] = user.name
            session["is_admin"] = user.is_admin

            flash(f"Bem-vindo, {user.name}!", "success")
            return redirect("/")

        flash("Email ou senha inválidos.", "danger")
        return redirect("/login")

    return render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():

    if session.get("user_id"):
        return redirect("/")

    if request.method == "POST":

        name = request.form["name"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]

        if not name:
            flash("Nome é obrigatório.", "danger")
            return redirect("/register")

        if not email:
            flash("Email é obrigatório.", "danger")
            return redirect("/register")

        if not password:
            flash("Senha é obrigatória.", "danger")
            return redirect("/register")

        if len(password) < 6:
            flash(
                "A senha deve possuir pelo menos 6 caracteres.",
                "danger"
            )
            return redirect("/register")

        existing_user = UserService.get_by_email(email)

        if existing_user:
            flash("Este email já está cadastrado.", "danger")
            return redirect("/register")

        UserService.create_user(name, email, password)

        flash(
            "Conta criada com sucesso! Faça login.",
            "success"
        )

        return redirect("/login")

    return render_template("register.html")


@auth.route("/logout")
def logout():

    session.clear()

    flash(
        "Logout realizado com sucesso.",
        "info"
    )

    return redirect("/login")