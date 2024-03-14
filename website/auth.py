from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from .models import User

auth = Blueprint("auth", __name__)



@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Logged in!", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("password incorrect", category="danger")
                return redirect(url_for("auth.login"))
        else:
            flash("user don\'t exists", category="danger")
        
    else:
        return render_template("login.html")


@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_exist = User.query.filter_by(email=email).first()

        if user_exist:
            flash("Email already in use!!", category="danger")
            return redirect(url_for("auth.signup"))
        elif password1 != password2:
            flash("Password don\'t match", category="danger")
            return redirect(url_for("auth.signup"))
        else:
            # try:
            new_user = User(email=email, username=username, password=generate_password_hash(password1)) 
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)

            flash("user created", category="success")
            return redirect(url_for("views.home"))
            # except:
            #     flash("something went wrong! please try again.", category="danger")
            #     return redirect(url_for("auth.signup"))
    else:
        return render_template("signup.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("you have been logged out!!", category="success")
    return redirect(url_for("views.home"))