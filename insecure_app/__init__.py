from pathlib import Path

from flask import Flask, g

from . import database
from .routes import bp as pages_blueprint


def create_app(test_config=None):
    """Create Flask app."""
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE_PATH=Path(__file__).resolve().parent / "data" / "insecure.db",
    )

    if test_config is not None:
        app.config.update(test_config)

    @app.before_request
    def initialize_query_log():
        """Reset per-request SQL log."""
        g.sql_queries = []

    app.teardown_appcontext(database.close_connection)
    app.register_blueprint(pages_blueprint)
    app.add_url_rule("/", endpoint="index")

    return app
