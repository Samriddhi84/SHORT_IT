# 🔗 URL Shortener

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0%2B-green)](https://flask.palletsprojects.com/)

A simple, efficient URL shortener with QR code generation and visit tracking.

## 📋 Contents
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#️-installation)
- [Usage](#-usage)
- [Code Structure](#-code-structure)
- [Contributing](#-contributing)
- [License](#-license)

## 🌟 Features
- URL shortening with custom aliases
- QR code generation
- User authentication
- Visit tracking
- User-friendly dashboard

## 📸 Screenshots

| Home Page | Dashboard |
|:---------:|:---------:|
| ![Home Page](screenshots/home_page.png) | ![Dashboard](screenshots/dashboard.png) |
| *Create short links* | *Manage your URLs* |

## 🛠️ Installation
```bash
git clone https://github.com/Samriddhi84/SHORT_IT.git
cd url-shortener
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
flask run
```
Visit `http://localhost:5000` in your browser.

## 🚀 Usage
1. Register/Login
2. Enter a long URL (with optional custom alias)
3. Get your shortened URL and QR code
4. Track visits in your dashboard

## 🧠 Code Structure

### Main Application ([app.py](https://github.com/Samriddhi84/SHORT_IT/blob/main/app.py))
```python
@app.route("/<path:var>/qr/")
def qr(var):
    var = var.lower()
    base_url = request.url_root
    user_data = session.get("user_data", db.user_data["default_user"])
    
    if var in user_data["urls"]:
        full_url = f"{base_url}{var}"
        img = generate_qr_code(full_url)
        session["b64"] = img
        session["alias"] = var
        flash(f"Use {full_url}/qr to visit this page")
        return redirect("/final")
    else:
        return redirect("/")
```

### Home Page ([templates/index.html](https://github.com/Samriddhi84/SHORT_IT/blob/main/templates/index.html))
```html
{% extends "base.html" %}
{% block title %}SHORT-IT{% endblock %}

{% block body %}
<div class="container">
    <form action="{{ url_for('shorten') }}" method="post">
        <input type="url" name="url" class="form-control" placeholder="Enter URL to shorten" required>
        <input type="text" name="alias" class="form-control" placeholder="Custom alias (optional)">
        <div class="form-check">
            <input type="checkbox" id="useAlias" name="useAlias" class="form-check-input">
            <label for="useAlias">Generate random alias if unavailable</label>
        </div>
        <button type="submit" class="btn btn-primary">Shorten URL</button>
    </form>
</div>
{% endblock %}
```

### QR Code Page ([templates/final.html](https://github.com/Samriddhi84/SHORT_IT/blob/main/templates/final.html))
```html
{% extends "base.html" %}
{% block title %}SHORT-IT - QR Code{% endblock %}

{% block body %}
<div class="container">
    <div class="form-group">
        <input type="text" class="form-control" value="{{ link }}" readonly>
    </div>
    <div class="qr-code">
        <img src="data:image/png;base64,{{ data }}" alt="QR Code">
    </div>
    <a href="{{ url_for('index') }}" class="btn btn-primary">Back to Home</a>
</div>
{% endblock %}
```

## 🔒 Security
- Secure password handling
- Session management
- Input validation

## 🤝 Contributing
We welcome contributions! Please feel free to submit a Pull Request.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/Samriddhi84/SHORT_IT/blob/main/LICENSE) file for details.

---

<p align="center">
  <a href="mailto:ssamriddhi47@gmail.com">📧 Contact</a> | 
  <a href="https://github.com/Samriddhi84/SHORT_IT/issues">🐛 Issues</a>
</p>
