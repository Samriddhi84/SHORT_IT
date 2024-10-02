# import re
# from flask import redirect, request, Flask, session, render_template, url_for, flash
# from functools import wraps
# from flask.cli import F
import datetime

# app = Flask(__name__)

# app.secret_key = "Random"
# import json

# # session = app.ses
# import util as db


# @app.template_filter("to_datetime")
# def to_datetime(value):
#     if isinstance(value, str):
#         # Parse the date string to a datetime object
#         dt = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
#         return dt.strftime("%B %d, %Y at %I:%M %p")  # Format the datetime as desired
#     return value


# # wrapper to check if user is logged in
# def login_required(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         print(session)
#         if not session.get("logged_in"):
#             return redirect(url_for("login"))
#         return f(*args, **kwargs)

#     return wrapper


# @app.route("/")  # type: ignore
# @app.route("/login", methods=["GET", "POST"])  # type: ignore
# def login():

#     if request.method == "GET":
#         if session.get("logged_in"):
#             return redirect(url_for("home")), 302

#         return render_template("login.html")
#     else:
#         if not session.get("logged_in"):
#             username = request.form.get(
#                 "username"
#             )  # not using request.form["username"] to avoid KeyError
#             print(username)
#             password = request.form.get("password")
#             print(password)
#             if not username or not password:
#                 flash("Invalid username or password", "error")
#                 return redirect(location=url_for("login")), 302
#             if db.validate_password(username, password):
#                 session["logged_in"], session["user_data"] = db.get_user(username)
#                 return redirect(location=url_for("home")), 302
#             else:
#                 flash("Invalid username or password", "error")
#                 return redirect(location=url_for("login")), 302

#         return redirect(location=url_for("home")), 302


# @app.route("/logout", methods=["GET"])  # type: ignore
# def logout():
#     if session.get("logged_in"):
#         session.clear()
#     return redirect(url_for("login")), 302


# @app.route("/register", methods=["GET", "POST"])  # type: ignore
# def register():
#     if request.method == "GET":
#         return render_template("register.html")
#     else:
#         username = request.form.get("username")
#         password = request.form.get("password")
#         name = request.form.get("name")
#         if not username or not password or not name:
#             return "Invalid username, password or name", 400
#         if db.get_user(username):
#             return "User already exists", 400
#         db.save_user(username, name, password)
#         session["logged_in"] = True
#         session["user_data"] = db.get_user(username)
#         return redirect(url_for("home")), 302
#         # return redirect(url_for("login")), 302


# @app.route("/home", methods=["GET", "POST"])  # type: ignore
# @login_required
# def home():
#     if request.method == "GET":
#         print(session["user_data"])
#         return render_template("home.html", user_data=session["user_data"])
#     return redirect("/")
#     # else:
#     #     alias = request.form.get("alias")
#     #     url = request.form.get("url")
#     #     if not alias or not url:
#     #         return "Invalid alias or url", 400
#     #     db.save_url(session["user_data"]["email"], alias, url)
#     #     return redirect(url_for("home")), 302
#     # else:
#     #     name, username, password = (
#     #         request.form.get("name"),
#     #         request.form.get("username"),
#     #         request.form.get("password"),
#     #     )
#     #     print(name, username, password)
#     #     print(request.form)
#     #     if not name or not username or not password:
#     #         return "Invalid user data", 400
#     #     user_data_updated = db.update_user(username, name, password)

#     # if not user_data_updated:
#     #     return "Invalid user data", 400
#     # user_data_updated = json.loads(user_data_updated)
#     # if not isinstance(user_data_updated, dict):
#     #     return "Invalid user data", 400
#     # if not all(
#     #     key in user_data_updated for key in ["name", "email", "password", "urls"]
#     # ):
#     #     return "Invalid user data", 400
#     # db.update_user(
#     #     user_data_updated["email"],
#     #     user_data_updated["name"],
#     #     user_data_updated["password"],
#     # )
#     # for alias, url in user_data_updated["urls"].items():
#     #     db.save_url(user_data_updated["email"], alias, url)
#     # status, session["user_data"] = db.get_user(username)
#     # print(status, session["user_data"])
#     # if not status:
#     #     return "Invalid user data", 400

#     # return redirect(url_for("home")), 302


# # @app.route("/edit_url", methods=["POST"])
# # @login_required
# # def edit_url():
# #     alias = request.form.get("alias")
# #     new_alias = request.form.get(key="new_alias")
# #     new_url = request.form.get("url")

# #     if not alias or not new_alias or not new_url:
# #         return "Invalid data", 400

# #     # Update the user's URL entry
# #     if alias in session["user_data"]["urls"]:
# #         session["user_data"]["urls"][new_alias] = {
# #             "url": new_url,
# #             "created_at": session["user_data"]["urls"][alias]["created_at"],
# #             "visits": session["user_data"]["urls"][alias]["visits"],
# #         }
# #         if new_alias != alias:
# #             del session["user_data"]["urls"][alias]

# #     return redirect(url_for("home")), 302


# def get_url(alias):
#     found, url = db.get_url(alias)

#     if found:
#         return redirect(url), 302
#     else:
#         return "Alias not found", 404


# @app.route("/session_data", methods=["GET"])  # type: ignore
# def session_data():
#     return str(session), 200


# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Blueprint, render_template, request, redirect, flash, session, url_for
import util as db
from flask import app

auth_bp = Blueprint("auth", __name__)


# 404 error handler
@auth_bp.app_errorhandler(404)
def page_not_found(e):
    return redirect(url_for("auth.login"))


@auth_bp.app_template_filter("to_datetime")
def to_datetime(value):
    if isinstance(value, str):
        # Parse the date string to a datetime object
        dt = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
        return dt.strftime("%B %d, %Y at %I:%M %p")  # Format the datetime as desired
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
        # if db.get_user(username):
        #     flash("User already exists", "error")
        #     return redirect(url_for("auth.register"))
        # db.save_user(username, name, password)
        session["logged_in"], session["user_data"] = db.get_user(username)
        return redirect(url_for("auth.home"))


@auth_bp.route("/home", methods=["GET", "POST"])  # type: ignore
@login_required
def home():
    if request.method == "GET":
        print(session["user_data"])
        return render_template("home.html", user_data=session["user_data"])
    return redirect("/")
