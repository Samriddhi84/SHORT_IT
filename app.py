from flask import Flask, redirect, render_template, request, flash, session
import qrcode
import base64
from io import BytesIO
import json
import time
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")  # Use a strong key in production

# Configuration for JSON file and expiration
JSON_FILE = "links.json"
EXPIRATION_TIME = 24 * 60 * 60  # 24 hours in seconds

def load_links():
    """Load links from the JSON file."""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    return {}

def save_links(links):
    """Save links to the JSON file."""
    with open(JSON_FILE, "w") as file:
        json.dump(links, file, indent=4)

def clean_expired_links():
    """Remove links that are older than the expiration time."""
    links = load_links()
    current_time = time.time()
    links = {alias: data for alias, data in links.items() if current_time - data["timestamp"] < EXPIRATION_TIME}
    save_links(links)

def get_base_url(request):
    """Generate the base URL dynamically based on the request."""
    scheme = request.scheme
    host = request.host
    return f"{scheme}://{host}"

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return redirect("/")

@app.route("/")
def home():
    """Render the home page."""
    return render_template("main.html")

@app.route("/shubh/information/<var>/")
def all(var):
    """Display or delete information based on the URL."""
    clean_expired_links()
    links = load_links()
    if var == "secret":
        return render_template("table2.html", data=links.items())
    else:
        if var in links:
            del links[var]
            save_links(links)
            flash("Link deleted successfully!")
        return redirect("/")

@app.route("/<path:var>/qr/")
def qr(var):
    """Generate a QR code for the given URL alias."""
    clean_expired_links()
    links = load_links()
    var = var.lower()
    base_url = get_base_url(request)
    if var in links:
        full_url = f"{base_url}/{var}"
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
    clean_expired_links()
    links = load_links()
    var = var.lower()
    if var in links:
        return redirect(links[var]["url"])
    else:
        return redirect("/")

@app.route("/short/", methods=["GET"])
def short():
    """Handle URL shortening requests."""
    if request.method == "GET":
        url = request.args.get("url")
        alias = request.args.get("alias")
        if not url or not alias:
            flash("ERROR INVALID URL/ALIAS")
            return redirect("/")

        alias = alias.replace(" ", "").lower()
        links = load_links()

        if alias in links or alias in ["short", "final"]:
            flash("Alias Already Exists")
        elif any(char in alias for char in "@!#$%^&*()'\".,/\\; ~ + -"):
            flash("Invalid Alias")
        else:
            links[alias] = {
                "url": url,
                "timestamp": time.time()
            }
            save_links(links)

            base_url = get_base_url(request)
            full_url = f"{base_url}/{alias}"
            img = generate_qr_code(full_url)
            session["b64"] = img
            session["alias"] = alias
            flash(f"USE {full_url}/qr TO VISIT THIS PAGE")
        return redirect("/final")
    return redirect("/")

@app.route("/final/")
def final():
    """Render the final page with QR code."""
    alias = session.get("alias")
    img_str = session.get("b64")
    if not alias:
        return redirect("/")
    base_url = get_base_url(request)
    return render_template("final.html", link=f"{base_url}/{alias}", data=img_str)

def generate_qr_code(data):
    """Generate a QR code and return it as a base64 encoded string."""
    img = qrcode.make(data)
    buffered = BytesIO()
    img.save(buffered, format="png")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

if __name__ == "__main__":
    app.run(
        host="0.0.0.0", 
        port=int(os.environ.get("PORT", 5000))
    )
