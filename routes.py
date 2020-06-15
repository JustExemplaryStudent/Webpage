from app import app, db
from flask import render_template, url_for, redirect, request, session, flash, get_flashed_messages
from models import User


def is_username_available(username):
    user = User.query.filter_by(username=username).first()
    return user is None


def register_user(username, password):
    user = User(username=username)
    user.set_password_hash(password)
    db.session.add(user)
    db.session.commit()


def get_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return None
    if user.check_password(password):
        return user
    else:
        return None

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/profile')
def profile():
    if "is_logged" in session and session["is_logged"]:
        return render_template("profile.html")
    flash("You need to be logged in, to view this page.")
    return redirect(url_for("login"))


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        failed = False
        username = request.form["username"]
        if not is_username_available(username):
            failed = True
            flash("Username already taken!")
        if not request.form["password"] == request.form["password_check"]:
            failed = True
            flash("Password missmatch.")
        if not failed:
            register_user(username, request.form["password"])
            return redirect(url_for('index'))
    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = get_user(username, password)
        if user is not None:
            session["user"] = user
            session["is_logged"] = True
        else:
            flash("Incorrect username or password.")
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop("is_logged", None)
    session.pop("user", None)
    return render_template("logout.html")
