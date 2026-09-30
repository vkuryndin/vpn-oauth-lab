import os
import platform
import socket

from flask import Flask, render_template, session

from auth import init_auth, login_required


app = Flask(__name__)

app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "dev-secret-key"
)

init_auth(app)


@app.route("/")
@login_required
def home():
    return render_template("home.html")


@app.route("/page1")
@login_required
def page1():
    return render_template("page1.html")


@app.route("/page2")
@login_required
def page2():
    return render_template("page2.html")


@app.route("/info")
@login_required
def info():
    return render_template(
        "info.html",
        hostname=socket.gethostname(),
        os_name=platform.system(),
        os_version=platform.release(),
        python_version=platform.python_version()
    )


@app.route("/profile")
@login_required
def profile():
    return render_template(
        "profile.html",
        user=session["user"]
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )