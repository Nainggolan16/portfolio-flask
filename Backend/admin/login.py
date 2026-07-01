from flask import render_template, request, redirect, session, flash
from sqlalchemy import text
from app import app, db

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        query = text("""
            SELECT *
            FROM users
            WHERE username = :username
            AND password = :password
        """)

        user = db.session.execute(
            query,
            {
                "username": username,
                "password": password
            }
        ).fetchone()

        if user:
            session["user_id"] = user.id
            session["username"] = user.username

            return redirect("/dashboard")

        flash("Username atau Password salah")

    return render_template("admin/login.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "admin/dashboard.html",
        username=session["username"]
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")