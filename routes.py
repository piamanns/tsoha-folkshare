from flask import render_template
from app import app
from db import db

@app.route("/")
def index():
    sql = "SELECT id, name, created FROM tunes ORDER BY id DESC"
    result = db.session.execute(sql)
    tunes = result.fetchall()
    return render_template("index.html", tunes=tunes)

@app.route("/tune/<int:id>")
def tune(id):
    sql = "SELECT id, name, notation, created FROM tunes WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    tune = result.fetchone()
    return render_template("tune.html", tune=tune)