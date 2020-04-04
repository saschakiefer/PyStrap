from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    Blueprint,
    current_app,
    url_for,
)

from flask.json import jsonify
from requests_oauthlib import OAuth2Session
import os


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login")
def login():
    github_session = OAuth2Session(
        current_app.config["GITHUB_CLIENT_ID"], scope="read:user"
    )
    authorization_url, state = github_session.authorization_url(
        current_app.config["GITHUB_LOGON_LINK"]
    )

    # State is used to prevent CSRF, keep this for later.
    session["oauth_state"] = state
    return redirect(authorization_url)


@bp.route("/callback")
def callback():
    code = request.args["code"]

    github_session = OAuth2Session(
        current_app.config["GITHUB_CLIENT_ID"], state=session["oauth_state"]
    )
    token = github_session.fetch_token(
        current_app.config["GITHUB_TOKEN_EXCHANGE_LINK"],
        client_secret=current_app.config["GITHUB_CLIENT_SECRET"],
        code=code,
    )["access_token"]

    session["user_data"] = github_session.get(
        current_app.config["GITHUB_USER_LINK"]
    ).json()
    session["token"] = token

    return redirect(url_for("strap.strap"))
