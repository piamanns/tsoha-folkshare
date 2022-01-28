from flask import render_template, request
from app import app
from db import db
import users

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

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            return "<p>Käyttäjätunnuksen tulee olla 1-20 merkkiä pitkä</p>"

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return "<p>Salasanat eivät olleet samoja molemmissa kentissä</p>"

        role = request.form["role"]
        if role not in ("1", "2"):
            return "<p><Virheellinen käyttäjärooli/p>"
        
        if not users.register(username, password1, role):
            return "<p>Rekisteröinti epäonnistui</p>"
        return "<p>Rekisteröinti onnistui!</p>"
