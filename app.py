# from flask import Flask, redirect, render_template, request, flash, session
# import qrcode
# import base64
# from io import BytesIO
# import os
# from util import (
#     save_user,
#     get_user,
#     update_user,
#     delete_user,
#     save_url,
#     get_url,
#     update_url,
#     delete_url,
#     validate_password,
# )

# app = Flask(__name__)
# app.secret_key = os.environ.get(
#     "SECRET_KEY", "default_secret_key"
# )  # Use a strong key in production


# @app.errorhandler(404)
# def page_not_found(e):
#     """Handle 404 errors."""
#     return redirect("/")


# @app.route("/")
# def home():
#     """Render the home page."""
#     return render_template("main.html")


# @app.route("/register", methods=["POST"])
# def register():
#     """Handle user registration."""
#     email = request.form.get("email")
#     name = request.form.get("name")
#     password = request.form.get("password")
#     success, message = save_user(email, name, password)
#     flash(message)
#     return redirect("/")


# @app.route("/login", methods=["POST"])
# def login():
#     """Handle user login."""
#     email = request.form.get("email")
#     password = request.form.get("password")
#     if validate_password(email, password):
#         session["user_email"] = email
#         flash("Login successful!")
#     else:
#         flash("Invalid email or password.")
#     return redirect("/")


# @app.route("/logout")
# def logout():
#     """Handle user logout."""
#     session.pop("user_email", None)
#     flash("Logged out successfully.")
#     return redirect("/")


# @app.route("/short/", methods=["POST"])
# def short():
#     """Handle URL shortening requests."""
#     url = request.form.get("url")
#     alias = request.form.get("alias")
#     email = session.get("user_email")

#     if not email:
#         flash("You must be logged in to shorten a URL.")
#         return redirect("/")

#     if not url or not alias:
#         flash("ERROR INVALID URL/ALIAS")
#         return redirect("/")

#     alias = alias.replace(" ", "").lower()

#     if save_url(email, alias, url):
#         flash(f"URL shortened successfully to {alias}.")
#     else:
#         flash("Alias already exists or is invalid.")

#     return redirect("/")


# @app.route("/<path:var>/qr/")
# def qr(var):
#     """Generate a QR code for the given URL alias."""
#     var = var.lower()
#     base_url = request.url_root
#     user = get_user(session.get("user_email"))

#     if user and var in user[1]["urls"]:
#         full_url = f"{base_url}{var}"
#         img = generate_qr_code(full_url)
#         session["b64"] = img
#         session["alias"] = var
#         flash(f"USE {full_url}/qr TO VISIT THIS PAGE")
#         return redirect("/final")
#     else:
#         return redirect("/")


# @app.route("/<path:var>/")
# def start(var):
#     """Redirect to the URL associated with the alias."""
#     var = var.lower()
#     user = get_user(session.get("user_email"))

#     if user and var in user[1]["urls"]:
#         return redirect(user[1]["urls"][var]["url"])
#     else:
#         return redirect("/")


# @app.route("/final/")
# def final():
#     """Render the final page with QR code."""
#     alias = session.get("alias")
#     img_str = session.get("b64")
#     if not alias:
#         return redirect("/")
#     base_url = request.url_root
#     return render_template("final.html", link=f"{base_url}/{alias}", data=img_str)


# def generate_qr_code(data):
#     """Generate a QR code and return it as a base64 encoded string."""
#     img = qrcode.make(data)
#     buffered = BytesIO()
#     img.save(buffered, format="png")
#     return base64.b64encode(buffered.getvalue()).decode("utf-8")


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

from flask import Flask, redirect, render_template, request, flash, session, url_for
import qrcode
import base64
from io import BytesIO
import os
import util as db  # Assuming this is your util module
from auth import auth_bp  # Import the authentication blueprint

app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY", "default_secret_key"
)  # Use a strong key in production

# Register the authentication blueprint
app.register_blueprint(auth_bp, url_prefix="/dashboard")


@app.route("/")
def index():
    """Render the home page."""
    return render_template("index.html")


# def login_required(f):
#     """Wrapper to check if the user is logged in."""
#     from functools import wraps

#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         if not session.get("logged_in"):
#             return redirect(url_for("auth.login"))  # Redirect to the login page
#         return f(*args, **kwargs)

#     return wrapper


# @app.errorhandler(404)
# def page_not_found(e):
#     """Handle 404 errors."""
#     return redirect("/")


# @app.route("/home", methods=["GET"])
# @login_required
# def home():
#     return render_template("home.html", user_data=session.get("user_data"))


@app.route("/short", methods=["POST"])
def short():
    """Handle URL shortening requests."""
    url = request.form.get("url")
    alias = request.form.get("alias")
    random_alias = request.form.get("useAlias")

    print(random_alias)

    # Determine the email based on login status
    email = (
        session["user_data"]["email"] if session.get("logged_in") else "default_user"
    )

    if not url or not alias:
        flash("ERROR INVALID URL/ALIAS")
        return redirect("/")

    alias = alias.replace(" ", "").lower()

    status, _ = db.save_url(email, alias, url)
    print(_)

    if status:
        flash(f"URL shortened successfully to {alias}.")
        session["user_data"] = db.get_user(email)[1]
        return redirect(url_for("qr", var=alias))

    else:
        if random_alias:
            alias = db.create_alias(url)
            status, _ = db.save_url(email, alias, url)
            if status:
                flash(f"URL shortened successfully to {alias}.")
                session["user_data"] = db.get_user(email)[1]
                return redirect(url_for("qr", var=alias))
            else:
                flash("Alias already exists or is invalid.")

    return redirect("/")

    # if db.save_url(email, alias, url):
    #     flash(f"URL shortened successfully to {alias}.")
    # else:
    #     flash("Alias already exists or is invalid.")

    # return redirect("/")
    return redirect(url_for("qr", var=alias))


@app.route("/<path:var>/qr/")
def qr(var):
    """Generate a QR code for the given URL alias."""
    var = var.lower()
    base_url = request.url_root
    user_data = session.get("user_data", db.user_data["default_user"])
    print(user_data)
    if var in user_data["urls"]:
        full_url = f"{base_url}{var}"
        img = generate_qr_code(full_url)
        session["b64"] = img
        session["alias"] = var
        flash(f"USE {full_url}/qr TO VISIT THIS PAGE")
        return redirect("/final")
    else:
        return redirect("/")


@app.route("/<path:var>/")
def start(var):
    """Redirect to the URL associated with the alias."""
    var = var.lower()
    user_data = session.get("user_data", db.user_data["default_user"])

    if var in user_data["urls"]:
        # Increment the visit count
        user_data["urls"][var]["visits"] += 1
        db.save_data(user_data=user_data)
        session["user_data"] = user_data

        return redirect(user_data["urls"][var]["url"])
    else:
        return redirect("/")


@app.route("/final/")
def final():
    """Render the final page with QR code."""
    alias = session.get("alias")
    img_str = session.get("b64")
    if not alias:
        return redirect("/")
    base_url = request.url_root
    return render_template("final.html", link=f"{base_url}/{alias}", data=img_str)


def generate_qr_code(data):
    """Generate a QR code and return it as a base64 encoded string."""
    img = qrcode.make(data)
    buffered = BytesIO()
    img.save(buffered, format="png")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=int(os.environ.get("PORT", 5000)))
