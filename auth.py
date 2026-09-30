import os
from functools import wraps
from urllib.parse import urlencode

from flask import redirect, url_for, session
from authlib.integrations.flask_client import OAuth


oauth = OAuth()


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


def init_auth(app):
    oauth.init_app(app)

    oauth.register(
        name="keycloak",
        client_id="flask-app",
        client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"),
        server_metadata_url=(
            "http://10.10.10.1:8180/"
            "realms/vpn-oauth-lab/.well-known/openid-configuration"
        ),
        client_kwargs={
            "scope": "openid profile email"
        }
    )

    @app.route("/login")
    def login():
        redirect_uri = url_for("auth_callback", _external=True)

        return oauth.keycloak.authorize_redirect(
            redirect_uri,
            prompt="login"
        )

    @app.route("/auth/callback")
    def auth_callback():
        token = oauth.keycloak.authorize_access_token()
        user = token.get("userinfo")

        session["user"] = user
        session["id_token"] = token.get("id_token")

        return redirect(url_for("home"))

    @app.route("/logout")
    def logout():
        id_token = session.get("id_token")

        session.clear()

        params = {
            "client_id": "flask-app",
            "post_logout_redirect_uri":
                "http://10.10.10.1:5000/login",
        }

        if id_token:
            params["id_token_hint"] = id_token

        logout_url = (
            "http://10.10.10.1:8180/"
            "realms/vpn-oauth-lab/protocol/openid-connect/logout?"
            + urlencode(params)
        )

        return redirect(logout_url)