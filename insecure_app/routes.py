from flask import Blueprint, render_template, request

from . import database

bp = Blueprint("pages", __name__)


@bp.route("/")
def index():
    return render_template("index.html", sql_queries=database.get_query_log())


@bp.route("/login", methods=("GET", "POST"))
def login():
    """
    The SQL query concatenates user input directly, allowing classic OR-based
    bypasses such as `' OR '1'='1`.
    """
    message = None
    user = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        raw_sql = (
            "SELECT id, username, role FROM users "
            f"WHERE username = '{username}' AND password = '{password}'"
        )

        user = database.unsafe_fetch_one(raw_sql)

        if user:
            message = f"Welcome back, {user['username']}! Your role is {user['role']}."
        else:
            message = "Login failed. Incorrect username or password."

    return render_template(
        "login.html",
        message=message,
        user=user,
        sql_queries=database.get_query_log(),
    )


@bp.route("/search")
def search():
    """
    The query can be extended with UNION SELECT to extract rows from other
    tables (for example: `' UNION SELECT username, password FROM users --`).
    """
    term = request.args.get("q", "")
    results = []

    if term:
        raw_sql = (
            "SELECT title, body FROM articles "
            f"WHERE title LIKE '%{term}%'
        )
        results = database.unsafe_fetch_all(raw_sql)

    return render_template(
        "search.html",
        term=term,
        results=results,
        sql_queries=database.get_query_log(),
    )
