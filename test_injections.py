
import re
import urllib.parse

from insecure_app import create_app


def extract_queries(html: str):
    candidates = re.findall(r"<code>(.*?)</code>", html, flags=re.DOTALL)
    return [item for item in candidates if "params=" in item]


def _or_payload():
    pieces = ["'", " OR ", "'1'='1"]
    return "".join(pieces)


def _union_payload():
    pieces = ["'", " UNION SELECT username, password FROM users --"]
    return "".join(pieces)


def demonstrate_login_bypass(client):
    payload = {"username": "ghost", "password": _or_payload()}
    response = client.post("/login", data=payload, follow_redirects=True)
    html = response.get_data(as_text=True)
    queries = extract_queries(html)
    succeeded = "Welcome back" in html
    return {"succeeded": succeeded, "queries": queries}


def demonstrate_login_success(client):
    payload = {"username": "admin", "password": "supersecret"}
    response = client.post("/login", data=payload, follow_redirects=True)
    html = response.get_data(as_text=True)
    queries = extract_queries(html)
    succeeded = "Welcome back" in html
    return {"succeeded": succeeded, "queries": queries}


def demonstrate_union_leak(client):
    encoded = urllib.parse.quote(_union_payload(), safe="")
    response = client.get(f"/search?q={encoded}")
    html = response.get_data(as_text=True)
    queries = extract_queries(html)
    leaked = "supersecret" in html
    return {"leaked": leaked, "queries": queries}


def demonstrate_search_success(client):
    response = client.get("/search?q=Flask")
    html = response.get_data(as_text=True)
    queries = extract_queries(html)
    found = "Understanding Flask" in html
    return {"found": found, "queries": queries}


def main():
    app = create_app({"TESTING": True})
    client = app.test_client()
    assert demonstrate_login_bypass(client)["succeeded"] is False
    assert demonstrate_union_leak(client)["leaked"] is False
    assert demonstrate_login_success(client)["succeeded"] is True
    assert demonstrate_search_success(client)["found"] is True


if __name__ == "__main__":
    main()
