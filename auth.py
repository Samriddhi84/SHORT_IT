import datetime

from flask import Blueprint, render_template, request, redirect, flash, session, url_for
import util as db
from flask import app

auth_bp = Blueprint("auth", __name__)

@auth_bp.app_errorhandler(404)
def page_not_found(e):
    return redirect(url_for("auth.login"))


@auth_bp.app_template_filter("to_datetime")
def to_datetime(value):
    if isinstance(value, str):
        dt = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
        return dt.strftime("%B %d, %Y at %I:%M %p") 
    return value


@auth_bp.app_template_filter("format_url")
def format_url(value):
    # return base_url + "/" + value

    return request.root_url + value


def login_required(f):
    """Wrapper to check if the user is logged in."""
    from functools import wraps

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("auth.login"))  # Redirect to the login page
        return f(*args, **kwargs)

    return wrapper


@auth_bp.route("/")
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session.get("logged_in"):
            return redirect(url_for("auth.home"))
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if db.validate_password(username, password):
            session["logged_in"], session["user_data"] = db.get_user(username)
            print(session["user_data"])
            return redirect(url_for("auth.home"))
        flash("Invalid username or password", "error")
        return redirect(url_for("auth.login"))


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        found, _ = db.get_user(username)
        if found:
            flash("User already exists", "error")
            return redirect(url_for("auth.register"))
        db.save_user(username, name, password)
        session["logged_in"], session["user_data"] = db.get_user(username)
        return redirect(url_for("auth.home"))


@auth_bp.route("/home", methods=["GET", "POST"])  # type: ignore
@login_required
def home():
    if request.method == "GET":
        print(session["user_data"])
        return render_template("home.html", user_data=session["user_data"])
    return redirect("/")
