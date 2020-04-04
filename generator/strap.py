from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    Blueprint,
    current_app,
    Response,
    url_for,
)
from requests_oauthlib import OAuth2Session
import os

bp = Blueprint("strap", __name__)


@bp.route("/")
def index():
    session.clear()

    return render_template(
        "index.html", strap_issue_url=current_app.config["STRAP_ISSUES_URL_DEFAULT"]
    )


@bp.route("/strap.sh")
def strap():
    """
    At the beginning we check for user data in the session. If they
    are not present, we start a logon flow to github, to make sure, we
    get an access token (since nothing is persisted, we do that every
    time). The OAuth callback URL also reads the user data and sets it
    to a cookie for one redirect. This ends here again, where the data
    are used to generate the script file for download. After that the
    data are removed from the cookie again.
    """
    if "user_data" not in session:
        # preserve the requested mode
        if "text" in request.args:
            session["mode"] = "text"
        else:
            session["mode"] = "file"

        return redirect(url_for("auth.login"))

    # remove to user data from the session
    user_data = session["user_data"]

    with open("./generator/static/strap.sh") as f:
        script_data = f.read()

    # Fill some data
    script_data = script_data.replace(
        "# STRAP_GIT_NAME=", "STRAP_GIT_NAME='" + user_data["name"] + "'"
    )
    script_data = script_data.replace(
        "# STRAP_GIT_EMAIL=", "STRAP_GIT_EMAIL='" + user_data["email"] + "'"
    )

    script_data = script_data.replace(
        "# STRAP_GITHUB_USER=", "STRAP_GITHUB_USER='" + user_data["login"] + "'"
    )

    script_data = script_data.replace(
        "# STRAP_GITHUB_TOKEN=", "STRAP_GITHUB_TOKEN='" + session["token"] + "'"
    )

    if session["mode"] == "text":
        mime_type = "text/plain"
    else:
        mime_type = "application/octet-stream"

    # Clean up the cookie, so that nothing is persisted on the client
    session.clear()

    response = Response(script_data, status=200, mimetype=mime_type)
    return response
