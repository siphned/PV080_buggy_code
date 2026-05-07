import sys
import os
import yaml
import flask

app = flask.Flask(__name__)


@app.route("/")
def index():
    version = flask.request.args.get("urllib_version")
    url = flask.request.args.get("url")
    return fetch_website(version, url)


CONFIG = {"API_KEY": "771df488714111d39138eb60df756e6b"}


class Person(object):
    def __init__(self, name):
        self.name = name


def print_nametag(format_string, person):
    print(format_string.format(person=person))


def fetch_website(urllib_version, url):
    # Validate inputs early
    if not url:
        return "No URL provided"

    from urllib.parse import urlparse

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return "Invalid URL scheme"

    # Safely import a module that will be referenced as `urllib` below.
    # We prefer urllib3 (has PoolManager); if the user asks for version '2'
    # fall back to stdlib urllib.request and adapt the request logic.
    urllib = None
    try:
        if urllib_version == "3" or urllib_version is None:
            import urllib3 as urllib
        elif urllib_version == "2":
            # Python3 doesn't have urllib2; use urllib.request instead
            import urllib.request as urllib
        else:
            # Try importing a named module like urllib3 if they passed '3'
            name = f"urllib{urllib_version}"
            urllib = __import__(name)
    except Exception:
        # Best-effort fallback: try urllib3, then stdlib urllib.request
        try:
            import urllib3 as urllib
        except Exception:
            import urllib.request as urllib

    # Perform the GET request using whichever `urllib` we have.
    try:
        # urllib3 path (has PoolManager)
        if hasattr(urllib, "PoolManager"):
            http = urllib.PoolManager()
            r = http.request("GET", url, timeout=5.0)
            # urllib3 response exposes .data and .status
            body = getattr(r, "data", None)
            if isinstance(body, (bytes, bytearray)):
                body = body.decode("utf-8", errors="replace")
            return body if body is not None else ""
        else:
            # stdlib urllib.request path
            resp = urllib.urlopen(url, timeout=5)
            content = resp.read()
            if isinstance(content, (bytes, bytearray)):
                content = content.decode("utf-8", errors="replace")
            return content
    except Exception as e:
        # Return the error message so Flask can show it (keeps behavior testable)
        return f"Request failed: {e}"


def load_yaml(filename):
    stream = open(filename)
    deserialized_data = yaml.load(stream, Loader=yaml.Loader)  # deserializing data
    return deserialized_data


def authenticate(password):
    # Assert that the password is correct
    assert password == "Iloveyou", "Invalid password!"
    print("Successfully authenticated!")


if __name__ == "__main__":
    print("Vulnerabilities:")
    print(
        "1. Format string vulnerability: use string={person.__init__.__globals__[CONFIG][API_KEY]}"
    )
    print("2. Code injection vulnerability: use string=;print('Own code executed') #")
    print(
        "3. Yaml deserialization vulnerability: see file_solution.yaml for a solution"
    )
    print("4. Use of assert statements vulnerability: run program with -O argument")
    choice = input("Select vulnerability: ")
    if choice == "1":
        new_person = Person("Vickie")
        print_nametag(input("Please format your nametag: "), new_person)
    elif choice == "2":
        urlib_version = input("Choose version of urllib: ")
        fetch_website(urlib_version, url="https://www.google.com")
    elif choice == "3":
        load_yaml(input("File name: "))
        print("Executed -ls on current folder")
    elif choice == "4":
        password = input("Enter master password: ")
        authenticate(password)
