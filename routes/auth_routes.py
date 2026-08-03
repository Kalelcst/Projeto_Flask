from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User

auth = Blueprint("auth", __name__)


# =========================
# Login
# =========================
@auth.route("/login", methods=["GET", "POST"])
def login():

    if session.get("user_id"):
        return redirect("/")

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            session["user_id"] = user.id
            session["user_name"] = user.name
            session["is_admin"] = user.is_admin

            flash(f"Bem-vindo, {user.name}!", "success")
            return redirect("/")

        flash("Email ou senha inválidos.", "danger")
        return redirect("/login")

    return render_template("login.html")


# =========================
# Cadastro
# =========================
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

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Este email já está cadastrado.", "danger")
            return redirect("/register")

        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()

        flash(
            "Conta criada com sucesso! Faça login.",
            "success"
        )

        return redirect("/login")

    return render_template("register.html")


# =========================
# Logout
# =========================
@auth.route("/logout")
def logout():

    session.clear()

    flash(
        "Logout realizado com sucesso.",
        "info"
    )

    return redirect("/login")