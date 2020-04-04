from flask import Flask
import os


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev")

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)

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
