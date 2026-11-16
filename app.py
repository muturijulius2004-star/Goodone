
import os
from flask import (
    Flask, render_template, request,
    redirect, url_for, session
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

app = Flask(__name__)

# Change this secret before deploying online.
app.secret_key = os.environ.get(
    "SECRET_KEY", "novatech-development-secret-change-me"
)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE") == "1"
)

# Ten temporary test accounts.
# Passwords are hashed before authentication checks.
TEST_ACCOUNTS = {
    "Martin01": "Test@4821",
    "Erick02": "Test@5932",
    "Kevin03": "Test@6143",
    "Brian04": "Test@7254",
    "Daniel05": "Test@8365",
    "James06": "Test@9476",
    "Peter07": "Test@1587",
    "Alex08": "Test@2698",
    "David09": "Test@3719",
    "John10": "Test@4820"
}

ACCOUNTS = {
    username: generate_password_hash(password)
    for username, password in TEST_ACCOUNTS.items()
}


@app.route("/")
def home():
    if not session.get("authenticated"):
        return redirect(url_for("login"))

    return render_template(
        "index.html",
        username=session.get("username")
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    if session.get("authenticated"):
        return redirect(url_for("home"))

    error = None

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        stored_hash = ACCOUNTS.get(username)

        if stored_hash and check_password_hash(
            stored_hash, password
        ):
            session.clear()
            session["authenticated"] = True
            session["username"] = username

            return redirect(url_for("home"))

        error = "Invalid username or password. Please try again."

    return render_template("login.html", error=error)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
