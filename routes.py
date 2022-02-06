from flask import flash, redirect, render_template, request
from app import app
import users
import tunes
import sys

@app.route("/")
def index():
    latest_tunes = tunes.get_latest_tunes()
    categories = tunes.get_all_categories()
    return render_template("index.html", tunes=latest_tunes, categories=categories)

@app.route("/tune/<int:id>")
def tune(id):
    tune = tunes.get_tune(id)
    categories = tunes.get_tune_categories(id)
    #print(tune, file=sys.stderr)
    return render_template("tune.html", tune=tune, categories=categories)

@app.route("/tune")
def all_tunes():
    all_tunes = tunes.get_all_tunes()
    return render_template("all_tunes.html", tunes=all_tunes)

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
        users.check_csrf(request.form["csrf_token"])

        name = request.form["name"]
        if len(name) < 1 or len(name) > 50:
            return "<p>Kappaleen nimen tulee olla 1-50 merkkiä pitkä.</p>"
        notation = request.form["notation"]
        if len(notation) < 1 or len(notation) > 1500:
            return "<p>ABC-notaation tulee olla 1-1500 merkkiä pitkä.</p>"  
        categories = request.form.getlist("category")
        tune_id = tunes.add_tune(name, notation, categories, user_id)
        if not tune_id:
            return "<p>Kappaleen lisääminen epäonnistui</p>"
        return redirect("/tune/"+str(tune_id))
        
@app.route("/category/<int:id>")
def category(id):
    category = tunes.get_category(id)
    if not category:
        return "<p>Virheellinen kategoria</p>"
    category_tunes = tunes.get_category_tunes(id)
    return render_template("category.html", name=category.name, tunes=category_tunes)

@app.route("/add_category", methods = ["GET", "POST"])
def add_category():
    user_role = users.user_role()

    if user_role < 2:
        return "<p>Vain ylläpitäjä voi lisätä uusia kategorioita</p>"

    if request.method == "GET":
        categories = tunes.get_all_categories()
        return render_template("add_category.html", categories=categories)
    
    if request.method == "POST":
        users.check_csrf(request.form["csrf_token"])
        user_id = users.user_id()

        name = request.form["name"]
        if len(name) < 1 or len(name) > 50:
            return "<p>Kategorian nimen tulee olla 1-50 merkkiä pitkä.</p>"
        new_category = tunes.add_category(name, user_id)
        if not new_category:
            return "<p>Kategorian lisääminen epäonnistui</p>"
        else:
            flash("Kategoria "+str(new_category)+" lisättiin palveluun.")
        return redirect("/add_category")
        

