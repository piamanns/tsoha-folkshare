from flask import redirect, render_template, request
from app import app
import users
import tunes
import sys

@app.route("/")
def index():
    all_tunes = tunes.get_all_tunes()
    return render_template("index.html", tunes=all_tunes)

@app.route("/tune/<int:id>")
def tune(id):
    tune = tunes.get_tune(id)
    categories = tunes.get_tune_categories(id)
    print(tune, file=sys.stderr)
    return render_template("tune.html", name=tune[0], notation=tune[1], categories=categories)

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
    user_id = users.user_id()
    if user_id == 0:
        return "<p>Kirjaudu sisään, jos haluat lisätä kappaleen</p>"

    if request.method == "GET":
        all_categories = tunes.get_all_categories()
        return render_template("add.html", categories=all_categories)

    if request.method == "POST":
        name = request.form["name"]
        notation = request.form["notation"]
        categories = request.form.getlist("category")
        tune_id = tunes.add_tune(name, notation, categories, user_id)
        if not tune_id:
            return "<p>Kappaleen lisääminen epäonnistui</p>"
        return redirect("/tune/"+str(tune_id))
        
    

