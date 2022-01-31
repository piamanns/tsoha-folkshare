from db import db

def get_all_tunes():
    sql = "SELECT id, name, created FROM tunes ORDER BY id DESC"
    return db.session.execute(sql).fetchall()

def get_tune(id):
    sql = "SELECT name, notation FROM tunes WHERE id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()

def add_tune(name, notation, categories, user_id):
    try:  
        sql = "INSERT INTO tunes (name, notation, created, creator_id) VALUES (:name, \
        :notation, NOW(), :user_id) RETURNING id"
        result = db.session.execute(sql, {"name": name, "notation": notation, "user_id": user_id})
        tune_id = result.fetchone()[0]
        for category in categories:
            sql = "INSERT INTO categories_tunes (category_id, tune_id) VALUES (:category_id, \
            :tune_id)"
            db.session.execute(sql, {"category_id": category, "tune_id": tune_id})
        db.session.commit()
        return tune_id
    except:
        return False

def get_all_categories():
    sql = 'SELECT id, name FROM categories WHERE visible=TRUE'
    result = db.session.execute(sql)
    return result.fetchall()

def get_tune_categories(tune_id):
    sql = 'SELECT c.name FROM categories c, categories_tunes ct WHERE ct.tune_id=:tune_id \
          AND c.id=ct.category_id AND c.visible=TRUE'
    result = db.session.execute(sql, {"tune_id": tune_id})
    return result.fetchall()