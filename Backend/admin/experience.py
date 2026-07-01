from flask import render_template, request, redirect, session
from sqlalchemy import text
from app import app, db


@app.route("/experience", methods=["GET", "POST"])
def experience():

	if "user_id" not in session:
		return redirect("/login")

	if request.method == "POST":

		periode = request.form["periode"]
		jabatan = request.form["jabatan"]
		perusahaan = request.form["perusahaan"]
		deskripsi = request.form["deskripsi"]

		query = text("""
			INSERT INTO experiences (
				periode,
				jabatan,
				perusahaan,
				deskripsi
			)
			VALUES (
				:periode,
				:jabatan,
				:perusahaan,
				:deskripsi
			)
		""")

		db.session.execute(
			query,
			{
				"periode": periode,
				"jabatan": jabatan,
				"perusahaan": perusahaan,
				"deskripsi": deskripsi
			}
		)

		db.session.commit()

		return redirect("/experience")

	query = text("SELECT * FROM experiences")

	data_experiences = db.session.execute(query).fetchall()

	return render_template(
		"admin/experience.html",
		experiences=data_experiences
	)


@app.route("/experience/delete/<int:id>")
def delete_experience(id):

	if "user_id" not in session:
		return redirect("/login")

	query = text("""
		DELETE FROM experiences
		WHERE id = :id
	""")

	db.session.execute(
		query,
		{
			"id": id
		}
	)

	db.session.commit()

	return redirect("/experience")


@app.route("/experience/edit/<int:id>", methods=["GET", "POST"])
def edit_experience(id):

	if "user_id" not in session:
		return redirect("/login")

	if request.method == "POST":

		periode = request.form["periode"]
		jabatan = request.form["jabatan"]
		perusahaan = request.form["perusahaan"]
		deskripsi = request.form["deskripsi"]

		query = text("""
			UPDATE experiences
			SET
				periode = :periode,
				jabatan = :jabatan,
				perusahaan = :perusahaan,
				deskripsi = :deskripsi
			WHERE id = :id
		""")

		db.session.execute(
			query,
			{
				"periode": periode,
				"jabatan": jabatan,
				"perusahaan": perusahaan,
				"deskripsi": deskripsi,
				"id": id
			}
		)

		db.session.commit()

		return redirect("/experience")

	query = text("""
		SELECT *
		FROM experiences
		WHERE id = :id
	""")

	experience = db.session.execute(
		query,
		{"id": id}
	).fetchone()

	query = text("SELECT * FROM experiences")
	data_experiences = db.session.execute(query).fetchall()

	return render_template(
		"admin/experience.html",
		experience=experience,
		experiences=data_experiences
	)
