from flask import render_template, request, redirect, session
from sqlalchemy import text
from app import app, db
from Backend.admin.upload import upload_image


@app.route("/skills", methods=["GET", "POST"])
def skills():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        nama_skill = request.form["nama_skill"]

        icon = ""

        if "icon" in request.files and request.files["icon"].filename != "":
            icon = upload_image(
                request.files["icon"],
                "skills"
            )

        query = text("""
            INSERT INTO skills (
                nama_skill,
                icon
            )
            VALUES (
                :nama_skill,
                :icon
            )
        """)

        db.session.execute(
            query,
            {
                "nama_skill": nama_skill,
                "icon": icon
            }
        )

        db.session.commit()

        return redirect("/skills")

    query = text("""
        SELECT *
        FROM skills
        ORDER BY id DESC
    """)

    data_skills = db.session.execute(query).fetchall()

    return render_template(
        "admin/skills.html",
        skills=data_skills,
        skill=None
    )


@app.route("/skills/delete/<int:id>")
def delete_skill(id):

    if "user_id" not in session:
        return redirect("/login")

    query = text("""
        DELETE FROM skills
        WHERE id=:id
    """)

    db.session.execute(
        query,
        {
            "id": id
        }
    )

    db.session.commit()

    return redirect("/skills")


@app.route("/skills/edit/<int:id>", methods=["GET", "POST"])
def edit_skill(id):

    if "user_id" not in session:
        return redirect("/login")

    query = text("""
        SELECT *
        FROM skills
        WHERE id=:id
    """)

    skill = db.session.execute(
        query,
        {
            "id": id
        }
    ).fetchone()

    if request.method == "POST":

        nama_skill = request.form["nama_skill"]

        icon = skill.icon

        if "icon" in request.files and request.files["icon"].filename != "":
            icon = upload_image(
                request.files["icon"],
                "skills"
            )

        query = text("""
            UPDATE skills
            SET
                nama_skill=:nama_skill,
                icon=:icon
            WHERE id=:id
        """)

        db.session.execute(
            query,
            {
                "nama_skill": nama_skill,
                "icon": icon,
                "id": id
            }
        )

        db.session.commit()

        return redirect("/skills")

    query = text("""
        SELECT *
        FROM skills
        ORDER BY id DESC
    """)

    data_skills = db.session.execute(query).fetchall()

    return render_template(
        "admin/skills.html",
        skill=skill,
        skills=data_skills
    )