from flask import render_template, request, redirect, session, flash
from sqlalchemy import text

from app import app, db
from Backend.admin.upload import upload_image


# ==========================================================
# PROJECTS
# ==========================================================

@app.route("/projects", methods=["GET", "POST"])
def projects():

    if "user_id" not in session:
        return redirect("/login")

    # ======================================================
    # TAMBAH PROJECT
    # ======================================================

    if request.method == "POST":

        judul = request.form["judul"]
        deskripsi = request.form["deskripsi"]
        tags = request.form["tags"]

        foto = request.files.get("gambar")

        gambar_url = None

        if foto and foto.filename != "":
            gambar_url = upload_image(
                foto,
                folder="portfolio/projects"
            )

        query = text("""
            INSERT INTO projects
            (
                judul,
                deskripsi,
                tags,
                gambar_url
            )
            VALUES
            (
                :judul,
                :deskripsi,
                :tags,
                :gambar_url
            )
        """)

        db.session.execute(
            query,
            {
                "judul": judul,
                "deskripsi": deskripsi,
                "tags": tags,
                "gambar_url": gambar_url
            }
        )

        db.session.commit()

        flash("Project berhasil ditambahkan.")

        return redirect("/projects")

    query = text("""
        SELECT *
        FROM projects
        ORDER BY id DESC
    """)

    data_projects = db.session.execute(query).fetchall()

    return render_template(
        "admin/projects.html",
        projects=data_projects
    )


# ==========================================================
# DELETE PROJECT
# ==========================================================

@app.route("/projects/delete/<int:id>")
def delete_project(id):

    if "user_id" not in session:
        return redirect("/login")

    query = text("""
        DELETE
        FROM projects
        WHERE id=:id
    """)

    db.session.execute(
        query,
        {
            "id": id
        }
    )

    db.session.commit()

    flash("Project berhasil dihapus.")

    return redirect("/projects")


# ==========================================================
# EDIT PROJECT
# ==========================================================

@app.route("/projects/edit/<int:id>", methods=["GET", "POST"])
def edit_project(id):

    if "user_id" not in session:
        return redirect("/login")

    query = text("""
        SELECT *
        FROM projects
        WHERE id=:id
    """)

    project = db.session.execute(
        query,
        {
            "id": id
        }
    ).fetchone()

    # ======================================================
    # UPDATE
    # ======================================================

    if request.method == "POST":

        judul = request.form["judul"]
        deskripsi = request.form["deskripsi"]
        tags = request.form["tags"]

        foto = request.files.get("gambar")

        # jika upload baru
        if foto and foto.filename != "":
            gambar_url = upload_image(
                foto,
                folder="portfolio/projects"
            )
        else:
            gambar_url = project.gambar_url

        query = text("""
            UPDATE projects
            SET
                judul=:judul,
                deskripsi=:deskripsi,
                tags=:tags,
                gambar_url=:gambar_url
            WHERE id=:id
        """)

        db.session.execute(
            query,
            {
                "judul": judul,
                "deskripsi": deskripsi,
                "tags": tags,
                "gambar_url": gambar_url,
                "id": id
            }
        )

        db.session.commit()

        flash("Project berhasil diperbarui.")

        return redirect("/projects")

    query = text("""
        SELECT *
        FROM projects
        ORDER BY id DESC
    """)

    data_projects = db.session.execute(query).fetchall()

    return render_template(
        "admin/projects.html",
        project=project,
        projects=data_projects
    )