from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from config import Config

app = Flask(
    __name__,
    template_folder="Frontend",
    static_folder="Frontend"
)

app.config.from_object(Config)

from Backend.admin.upload import init_cloudinary
init_cloudinary(app)

# import cloudinary

# cfg = cloudinary.config()

# print("Cloud :", cfg.cloud_name)
# print("Key   :", cfg.api_key)
# print("Secret:", cfg.api_secret)

db = SQLAlchemy(app)


# ======================================================
# LANDING PAGE
# ======================================================

@app.route("/")
def home():

    profile = db.session.execute(text("""
        SELECT *
        FROM users
        ORDER BY id ASC
        LIMIT 1
    """)).fetchone()

    skills = db.session.execute(
        text("SELECT * FROM skills ORDER BY id ASC")
    ).fetchall()

    experiences = db.session.execute(
        text("SELECT * FROM experiences ORDER BY id ASC")
    ).fetchall()

    projects = db.session.execute(
        text("SELECT * FROM projects ORDER BY id ASC")
    ).fetchall()

    return render_template(
        "utama/utama.html",
        profile=profile,
        skills=skills,
        experiences=experiences,
        projects=projects
    )


# ======================================================
# TEST DATABASE
# ======================================================

@app.route("/test-db")
def test_db():
    try:
        db.session.execute(text("SELECT 1"))
        return "✅ Koneksi TiDB Berhasil!"
    except Exception as e:
        return f"❌ Error Database : {e}"


# ======================================================
# IMPORT ROUTES
# ======================================================

from Backend.admin.login import *
from Backend.admin.skills import *
from Backend.admin.experience import *
from Backend.admin.projects import *
from Backend.admin.profiles import *


# ======================================================
# RUN APP
# ======================================================

if __name__ == "__main__":
    app.run(debug=True)


import resend

resend.api_key = app.config["RESEND_API_KEY"]

from Backend.admin.contact import *