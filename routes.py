from flask import flash, redirect, render_template, request
from app import app
import users
import tunes
import comments
import categories as cats
import sys

@app.route("/")
def index():
    latest_tunes = tunes.get_latest_tunes()
    categories = cats.get_all_categories()
    return render_template("index.html", tunes=latest_tunes, categories=categories)

@app.route("/tune/<int:id>")
def tune(id):
    tune = tunes.get_tune(id)
    tune_categories = tunes.get_tune_categories(id)
    tune_comments = comments.get_tune_comments(id)
    #print(tune, file=sys.stderr)
    if not tune:
        return render_template("error.html", message="Kappaletta ei löytynyt.")
    return render_template("tune.html", tune=tune, categories=tune_categories, comments=tune_comments)

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
            return render_template("error.html", message="Käyttäjätunnuksen tulee olla 1-20 merkkiä pitkä.")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät olleet samoja molemmissa kentissä.")

        role = request.form["role"]
        if role not in ("1", "2"):
            return render_template("error.html", message="Virheellinen käyttäjärooli.")
        
        if not users.register(username, password1, role):
            return render_template("error.html", message="Käyttäjätunnuksen rekisteröinti epäonnistui. Palvelussa saattaa jo olla samanniminen käyttäjä!")
        return redirect("/")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Kirjautuminen epäonnistui.")
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/add_tune", methods = ["GET", "POST"])
def add_tune():
    user_id = users.user_id()

    if user_id == 0:
        return render_template("error.html", message="Kirjaudu sisään, jos haluat lisätä kappaleen.")

    if request.method == "GET":
        all_categories = cats.get_all_categories()
        return render_template("add_tune.html", categories=all_categories)

    if request.method == "POST":
        users.check_csrf(request.form["csrf_token"])

        name = request.form["name"]
        if len(name) < 1 or len(name) > 50:
            return render_template("error.html", message="Kappaleen nimen tulee olla 1-50 merkkiä pitkä.")
        notation = request.form["notation"]
        if len(notation) < 1 or len(notation) > 1500:
            return render_template("error.html", message="ABC-notaation tulee olla 1-1500 merkkiä pitkä.")  
        categories = request.form.getlist("category")
        # Escape row changes in notation data
        sanitized = notation.replace("\r\n","\\n")
        tune_id = tunes.add_tune(name, sanitized, categories, user_id)
        if not tune_id:
            return render_template("error.html", message="Kappaleen lisääminen epäonnistui.")
        return redirect("/tune/"+str(tune_id))
        
@app.route("/category/<int:id>")
def category(id):
    category = cats.get_category_info(id)
    if not category:
        return render_template("error.html", message="Kategoriaa ei löytynyt.")
    category_tunes = cats.get_category_tunes(id)
    return render_template("category.html", name=category.name, tunes=category_tunes)

@app.route("/add_category", methods = ["GET", "POST"])
def add_category():
    user_role = users.user_role()

    if user_role < 2:
        return render_template("error.html", message="Vain ylläpitäjä voi lisätä uusia kategorioita.")

    if request.method == "GET":
        # Get all categories, including hidden ones
        categories = cats.get_all_categories(True)
        return render_template("category_admin.html", categories=categories)
    
    if request.method == "POST":
        users.check_csrf(request.form["csrf_token"])
        user_id = users.user_id()

        name = request.form["name"]
        if len(name) < 1 or len(name) > 50:
            return render_template("error.html", message="Kategorian nimen tulee olla 1-50 merkkiä pitkä.")
        new_category = cats.add_category(name, user_id)
        if not new_category:
            return render_template("error.html", message="Kategorian lisääminen epäonnistui")
        else:
            flash("Kategoria "+str(new_category)+" lisättiin palveluun.")
        return redirect("/add_category")    

@app.route("/set_category_visibility", methods = ["POST"])
def set_category_visibility():
      users.check_csrf(request.form["csrf_token"])
      if users.user_role() < 2:
          return render_template("error.html", message="Vain ylläpitäjä voi muokata kategorioita.")  
   
      categories = request.form.getlist("category")
      cats.set_category_visibility(categories)
      flash("Muutokset kategorioiden näkyvyyteen tallennettiin.")
      return redirect("/add_category")

@app.route("/delete_category", methods = ["POST"])
def delete_category():
      users.check_csrf(request.form["csrf_token"])
      if users.user_role() < 2:
          return render_template("error.html", message="Vain ylläpitäjä voi poistaa kategorioita.")
      category_id = request.form["category_id"]      
      deleted_name = cats.delete_category(category_id)
      flash(f"Kategoria {deleted_name} poistettiin palvelusta.")
      return redirect("/add_category")

@app.route("/delete_tune/<int:id>", methods = ["POST"])
def delete_tune(id):
    users.check_csrf(request.form["csrf_token"])
    user_id = users.user_id()
    user_role = users.user_role()
    creator_id = tunes.get_creator(id)

    if user_id == creator_id or user_role >= 2:
        deleted_name = tunes.delete_tune(id)
        flash("Kappale "+str(deleted_name)+" poistettiin palvelusta.")
        return redirect("/")
    else:
        return render_template("error.html", message="Sinulla ei ole oikeuksia poistaa tätä kappaletta.")

@app.route("/update_tune/<int:id>", methods = ["GET", "POST"])
def update_tune(id):
    user_id = users.user_id()
    user_role = users.user_role()
    creator_id = tunes.get_creator(id)

    if user_id != creator_id and user_role < 2:
        return render_template("error.html", message="Sinulla ei ole oikeuksia muokata tätä kappaletta.")

    if request.method == "GET":
        tune = tunes.get_tune(id)
        notation = tune.notation
        with_linebreaks = notation.replace("\\n", "\r\n")
        tune_categories = tunes.get_tune_categories(id, False)
        tune_category_ids = []
        for tune_category in tune_categories:
            tune_category_ids.append(tune_category[0])
        categories = cats.get_all_categories()
        return render_template("update_tune.html", tune=tune, notation=with_linebreaks, tune_category_ids=tune_category_ids, categories=categories)          
 
    if request.method == "POST":
        users.check_csrf(request.form["csrf_token"])

        name = request.form["name"]
        if len(name) < 1 or len(name) > 50:
            return render_template("error.html", message="Kappaleen nimen tulee olla 1-50 merkkiä pitkä.")
        notation = request.form["notation"]
        if len(notation) < 1 or len(notation) > 1500:
            return render_template("error.html", message="ABC-notaation tulee olla 1-1500 merkkiä pitkä.")  
        categories = request.form.getlist("category")

        # Escape row changes in notation data
        sanitized = notation.replace("\r\n","\\n")
        tunes.update_tune(id, name, sanitized, categories)
        flash("Muutokset tallennettiin.")
        return redirect("/tune/"+str(id))

@app.route("/add_comment", methods = ["POST"])
def add_comment():
    users.check_csrf(request.form["csrf_token"])
    user_id = users.user_id()
    if user_id == 0:
        return render_template("error.html", message="Vain kirjautuneet käyttäjät voivat kommentoida kappaleita.")

    tune_id = request.form["tune_id"]
    comment = request.form["comment"]
    if len(comment) < 1 or len(comment) > 1000:
        return render_template("error.html", message="Kommentin tulee olla 1-1000 merkkiä pitkä.")
    commented_tune = comments.add_comment(user_id, tune_id, comment)
    flash("Kommenttisi lisättiin.")
    return redirect("/tune/"+str(commented_tune))

@app.route("/delete_comment/<int:id>", methods = ["POST"])
def delete_comment(id):
    users.check_csrf(request.form["csrf_token"])
    user_id = users.user_id()
    user_role = users.user_role()
    if user_id == 0 or user_role < 2:
        return render_template("error.html", message="Vain ylläpitäjä voi poistaa kommentteja.")
    
    commented_tune = comments.delete_comment(id)
    flash("Kommentti poistettiin.")
    return redirect("/tune/"+str(commented_tune))

@app.route("/search")
def search():
    query = request.args["query"]
    result = tunes.search_tunes(query)
    return render_template("search_result.html", result=result, query=query)
    
