from flask import Blueprint, render_template, request

from . import database

bp = Blueprint("pages", __name__)


@bp.route("/")
def index():
    return render_template("index.html", sql_queries=database.get_query_log())


@bp.route("/login", methods=("GET", "POST"))
def login():
    message = None
    user = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        user = database.execute_safe(
            "SELECT id, username, role FROM users WHERE username = ? AND password = ?",
            (username, password),
            fetchone=True,
        )

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
    term = request.args.get("q", "")
    results = []

    if term:
        results = database.execute_safe(
            "SELECT title, body FROM articles WHERE title LIKE ?",
            (f"%{term}%",),
        )

    return render_template(
        "search.html",
        term=term,
        results=results,
        sql_queries=database.get_query_log(),
    )
