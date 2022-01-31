from flask import redirect, render_template, request
from app import app
from db import db
import users
import tunes

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
        return redirect("/")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return "<p>Kirjautuminen epäonnistui</p>"
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/add", methods = ["GET", "POST"])
def add():
    if request.method == "GET":
        sql = 'SELECT id, name FROM categories WHERE visible=TRUE'
        result = db.session.execute(sql)
        categories = result.fetchall()
        return render_template("add.html", categories=categories)

    if request.method == "POST":
        name = request.form["name"]
        notation = request.form["notation"]
        category = request.form.getlist("category")
        tune_id = tunes.add_tune(name, notation, category)
        if not tune_id:
            return "<p>Kappaleen lisääminen epäonnistui</p>"
        return redirect("/tune/"+str(tune_id))
        
    

