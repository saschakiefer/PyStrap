from flask import Flask, redirect, render_template, request, session, Response
from flask.json import jsonify
from requests_oauthlib import OAuth2Session
import os


# URLs
GITHUB_LOGON_LINK = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_EXCHANGE_LINK = "https://github.com/login/oauth/access_token"

STRAP_ISSUES_URL_DEFAULT = "https://github.com/saschakiefer/strap/issues/new"

GITHUB_CLIENT_ID = os.environ["GITHUB_CLIENT_ID"]
GITHUB_CLIENT_SECRET = os.environ["GITHUB_CLIENT_SECRET"]

APP_SECRET = b"\x12\x0be\xc9\xc16\xa2@\xc6\xf8\xe1\x81z\x8cf\xca\x83\x9a\x8cv\xad\xfe\xb6\x8a?\x86\xdd\xe5g\x819\xd6"

app = Flask(__name__)
app.secret_key = APP_SECRET


@app.route("/")
def root_route():
    session.pop("user_data", None)
    session.pop("token", None)

    return render_template("index.html", strap_issue_url=STRAP_ISSUES_URL_DEFAULT)


@app.route("/strap.sh")
def strap_sh():
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

        return redirect("/auth/github/logon")

    # remove to user data from the session
    user_data = session["user_data"]

    with open("./bin/strap.sh") as f:
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
    session.pop("user_data", None)
    session.pop("mode", None)
    session.pop("token", None)

    response = Response(script_data, status=200, mimetype=mime_type)
    return response


@app.route("/auth/github/logon")
def github_logon():
    github_session = OAuth2Session(GITHUB_CLIENT_ID, scope="read:user")
    authorization_url, state = github_session.authorization_url(GITHUB_LOGON_LINK)

    # State is used to prevent CSRF, keep this for later.
    session["oauth_state"] = state
    return redirect(authorization_url)


@app.route("/auth/github/callback")
def github_callback():
    code = request.args["code"]

    github_session = OAuth2Session(GITHUB_CLIENT_ID, state=session["oauth_state"])
    token = github_session.fetch_token(
        GITHUB_TOKEN_EXCHANGE_LINK, client_secret=GITHUB_CLIENT_SECRET, code=code
    )["access_token"]

    session["user_data"] = github_session.get("https://api.github.com/user").json()
    session["token"] = token

    return redirect("/strap.sh")
