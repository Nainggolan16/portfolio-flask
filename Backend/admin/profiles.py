from flask import render_template, request, redirect, session, flash
from sqlalchemy import text

from app import app, db
from Backend.admin.upload import upload_image


@app.route("/akun", methods=["GET", "POST"])
def akun():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    query = text("""
        SELECT *
        FROM users
        WHERE id = :id
    """)

    user = db.session.execute(
        query,
        {"id": user_id}
    ).fetchone()

    if request.method == "POST":

        action = request.form.get("action")

        # ==================================================
        # UPDATE PROFILE
        # ==================================================

        if action == "update_profile":

            nama_lengkap = request.form["nama_lengkap"]
            nama_panggilan = request.form["nama_panggilan"]
            tempat_lahir = request.form["tempat_lahir"]
            tanggal_lahir = request.form["tanggal_lahir"]
            email = request.form["email"]
            telepon = request.form["telepon"]
            universitas = request.form["universitas"]
            fakultas = request.form["fakultas"]
            program_studi = request.form["program_studi"]
            semester = request.form["semester"]
            alamat = request.form["alamat"]

            # ==========================================
            # Upload Foto Cloudinary
            # ==========================================

            foto = request.files.get("foto_profil")

            if foto and foto.filename != "":
                foto_profil = upload_image(
                    foto,
                    folder="portfolio/profile"
                )
            else:
                foto_profil = user.foto_profil

            query = text("""
                UPDATE users
                SET
                    nama_lengkap = :nama_lengkap,
                    nama_panggilan = :nama_panggilan,
                    tempat_lahir = :tempat_lahir,
                    tanggal_lahir = :tanggal_lahir,
                    email = :email,
                    telepon = :telepon,
                    universitas = :universitas,
                    fakultas = :fakultas,
                    program_studi = :program_studi,
                    semester = :semester,
                    alamat = :alamat,
                    foto_profil = :foto_profil
                WHERE id = :id
            """)

            db.session.execute(
                query,
                {
                    "nama_lengkap": nama_lengkap,
                    "nama_panggilan": nama_panggilan,
                    "tempat_lahir": tempat_lahir,
                    "tanggal_lahir": tanggal_lahir,
                    "email": email,
                    "telepon": telepon,
                    "universitas": universitas,
                    "fakultas": fakultas,
                    "program_studi": program_studi,
                    "semester": semester,
                    "alamat": alamat,
                    "foto_profil": foto_profil,
                    "id": user_id
                }
            )

            db.session.commit()

            flash("Profil berhasil diperbarui.")

            return redirect("/akun")

        # ==================================================
        # UPDATE PASSWORD
        # ==================================================

        elif action == "update_password":

            password_lama = request.form["password_lama"]
            password_baru = request.form["password_baru"]
            konfirmasi_password = request.form["konfirmasi_password"]

            if password_lama != user.password:
                flash("Password lama salah.")
                return redirect("/akun")

            if password_baru != konfirmasi_password:
                flash("Konfirmasi password tidak cocok.")
                return redirect("/akun")

            query = text("""
                UPDATE users
                SET password = :password
                WHERE id = :id
            """)

            db.session.execute(
                query,
                {
                    "password": password_baru,
                    "id": user_id
                }
            )

            db.session.commit()

            flash("Password berhasil diperbarui.")

            return redirect("/akun")

    # ==================================================
    # LOAD PAGE
    # ==================================================

    user = db.session.execute(
        query,
        {"id": user_id}
    ).fetchone()

    return render_template(
        "admin/profiles.html",
        user=user
    )