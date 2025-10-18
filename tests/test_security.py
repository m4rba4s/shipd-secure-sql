from insecure_app import create_app
from test_injections import (
    demonstrate_login_bypass,
    demonstrate_login_success,
    demonstrate_search_success,
    demonstrate_union_leak,
)


def test_login_injection_blocked():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        result = demonstrate_login_bypass(client)
        assert result["succeeded"] is False
        assert all("params=" in entry for entry in result["queries"])


def test_login_success():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        result = demonstrate_login_success(client)
        assert result["succeeded"] is True


def test_union_injection_blocked():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        result = demonstrate_union_leak(client)
        assert result["leaked"] is False
        assert all("params=" in entry for entry in result["queries"])


def test_search_success():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        result = demonstrate_search_success(client)
        assert result["found"] is True
