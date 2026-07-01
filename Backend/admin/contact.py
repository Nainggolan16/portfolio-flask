from flask import request, redirect, flash
from app import app
import resend


@app.route("/contact", methods=["POST"])
def contact():

    nama = request.form["nama"]
    email = request.form["email"]
    subject = request.form["subject"]
    pesan = request.form["pesan"]

    resend.Emails.send({
        "from": "Portfolio <onboarding@resend.dev>",
        "to": ["682024109@student.uksw.edu"],
        "subject": subject,
        "html": f"""
        <h2>Pesan Baru dari Portfolio</h2>

        <p><b>Nama :</b> {nama}</p>

        <p><b>Email :</b> {email}</p>

        <p><b>Pesan :</b></p>

        <p>{pesan}</p>
        """
    })

    flash("Pesan berhasil dikirim.")

    return redirect("/")