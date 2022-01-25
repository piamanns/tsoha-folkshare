from flask import render_template
from app import app
from db import db

@app.route("/")
def index():
    sql = "SELECT * FROM songs ORDER BY id DESC"
    result = db.session.execute(sql)
    song = result.fetchone()
    return render_template("index.html", song=song)