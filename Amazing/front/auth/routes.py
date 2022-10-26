from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from front import bcrypt, db

from front.auth.forms import (
    LoginForm,
    RegisterForm,
    RequestPasswordResetForm,
    ResetPasswordForm,
)
from front.models import Products, Reviews, Users

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST", "GET"])
def register():
    if not current_user.is_authenticated:

        form = RegisterForm()

        if form.validate_on_submit():

            user = Users()

            user.set_username(form.username.data)
            user.set_email(form.email.data)
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()

            flash("Account created successfully.", category="success")

            return render_template("loading.html", destination="login")

        return render_template("register.html", title="Register", form=form)

    return render_template("loading.html", destination="home")


@auth.get("/activate/<path:token>")
def activate(token):
    user = Users.query.filter_by(token=token).first()
    if user.is_activated == False:
        user.is_activated = True
        user.token = None
        db.session.commit()
        return render_template("loading.html", destination="activated")
    return render_template("loading.html", destination="already_activated")


@auth.get("/activated")
def activated():
    return render_template("activated.html")


@auth.route("/login", methods=["POST", "GET"])
def login():
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                flash("Logged in as %s." % user.username, "success")
                next_page = request.args.get("next")
                return (
                    redirect(next_page) if next_page else redirect(url_for("main.home"))
                )
            else:
                flash("Login unsuccessful. Please check email and password.", "danger")
        return render_template("login.html", title="Login", form=form)

    return redirect(url_for("main.home"))


@auth.route("/reset_password", methods=["POST", "GET"])
def reset_request():
    if current_user.is_authenticated:
        return render_template("login.html", destination="home")
    form = RequestPasswordResetForm()
    if form.validate_on_submit():

        user = Users.query.filter_by(email=form.email.data).first()

        user.send_reset_email()

        flash("Instructions have been sent to your email address.", "success")
        return render_template("loading.html", destination="login")
    return render_template("reset_request.html", title="Reset Password", form=form)


@auth.route("/reset_password/<token>", methods=["POST", "GET"])
def reset_password(token):
    if current_user.is_authenticated:
        return render_template("loading.html", destination="home")
    user = Users.verify_reset_token(token)
    if not user:
        flash("Token expired.", "warning")
        return render_template("loading.html", destination="reset_password")
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.commit()

        flash("Your password has been reset correctly.", category="success")

        return render_template("loading.html", destination="login")
    return render_template(
        "reset_password.html", title="Reset your password", form=form, pfp=user.pfp
    )


@auth.route("/change_password", methods=["POST", "GET"])
@login_required
def change_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.new_password.data).decode(
            "utf-8"
        )
        current_user.password = hashed_pwd
        db.session.commit()

        flash("Your password has been changed correctly.", category="success")

        return render_template("loading.html", destination="login")
    return render_template(
        "reset_password.html", title="Reset your password", form=form
    )


@auth.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.loading", destination="catalog"))
