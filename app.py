from flask import Flask, render_template, redirect, url_for, session
import platform
import socket

import os
from authlib.integrations.flask_client import OAuth
from functools import wraps
from urllib.parse import urlencode

app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

oauth = OAuth(app)

oauth.register(
    name="keycloak",
    client_id="flask-app",
    client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    server_metadata_url="http://10.10.10.1:8180/realms/vpn-oauth-lab/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid profile email"
    }
)
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view

@app.route("/")
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
@app.route("/login")
def login():
    redirect_uri = url_for("auth_callback", _external=True)
    return oauth.keycloak.authorize_redirect(redirect_uri)


@app.route("/auth/callback")
def auth_callback():
    token = oauth.keycloak.authorize_access_token()
    user = token.get("userinfo")

    session["user"] = user
    session["id_token"] = token.get("id_token")

    return redirect(url_for("home"))

@app.route("/profile")
@login_required
def profile():
    return render_template(
        "profile.html",
        user=session["user"]
    )
@app.route("/logout")
def logout():
    id_token = session.get("id_token")

    session.clear()

    params = {
        "post_logout_redirect_uri": "http://10.10.10.1:5000/",
    }

    if id_token:
        params["id_token_hint"] = id_token

    logout_url = (
        "http://10.10.10.1:8180/"
        "realms/vpn-oauth-lab/protocol/openid-connect/logout?"
        + urlencode(params)
    )

    return redirect(logout_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)