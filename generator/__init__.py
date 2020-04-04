from flask import Flask
import os


def set_config_from_env(app, name):
    if name in os.environ:
        app.config.from_mapping(name=os.environ[name])
        print(name + " was set from environment variable")
    else:
        print(name + " was not found in the environment variables")


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev")

    app.config.from_pyfile("config.py", silent=True)

    if test_config is None:
        app.config.from_pyfile("secrets.py", silent=True)

        # Override if possible from env variables
        set_config_from_env(app, "GITHUB_CLIENT_ID")
        set_config_from_env(app, "GITHUB_CLIENT_SECRET")
        set_config_from_env(app, "APP_SECRET")

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register blueprints
    from . import auth, strap

    app.register_blueprint(auth.bp)

    app.register_blueprint(strap.bp)
    app.add_url_rule("/", endpoint="index")

    return app
