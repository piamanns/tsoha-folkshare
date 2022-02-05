from db import db

def get_all_tunes():
    sql = "SELECT t.id, t.name, t.created, u.username FROM tunes t, users u WHERE t.creator_id=u.id " \
          "AND t.visible=TRUE ORDER BY t.id DESC"
    return db.session.execute(sql).fetchall()

def get_tune(id):
    sql = "SELECT t.name, t.notation, t.created, u.username FROM tunes t, users u WHERE t.id=:id " \
          "AND t.creator_id=u.id AND t.visible=TRUE"
    return db.session.execute(sql, {"id":id}).fetchone()

def add_tune(name, notation, categories, user_id):
    try:  
        sql = "INSERT INTO tunes (name, notation, created, creator_id, visible) VALUES (:name, " \
              ":notation, NOW(), :user_id, TRUE) RETURNING id"
        result = db.session.execute(sql, {"name": name, "notation": notation, "user_id": user_id})
        tune_id = result.fetchone()[0]
        for category in categories:
            sql = "INSERT INTO categories_tunes (category_id, tune_id) VALUES (:category_id, " \
                  ":tune_id)"
            db.session.execute(sql, {"category_id": category, "tune_id": tune_id})
        db.session.commit()
        return tune_id
    except:
        return False

def get_all_categories():
    sql = "SELECT id, name FROM categories WHERE visible=TRUE"
    result = db.session.execute(sql)
    return result.fetchall()

def get_tune_categories(tune_id):
    sql = "SELECT c.id, c.name FROM categories c, categories_tunes ct WHERE ct.tune_id=:tune_id " \
          "AND c.id=ct.category_id AND c.visible=TRUE"
    result = db.session.execute(sql, {"tune_id": tune_id})
    return result.fetchall()

def get_category(category_id):
    sql = "SELECT name FROM categories WHERE id=:category_id AND visible=TRUE"
    result = db.session.execute(sql, {"category_id": category_id})
    return result.fetchone()

def get_category_tunes(category_id):
    sql = "SELECT t.id, t.name, t.created, u.username " \
          "FROM categories_tunes ct JOIN categories c ON ct.category_id=c.id " \
          "JOIN tunes t ON ct.tune_id=t.id JOIN users u ON t.creator_id=u.id " \
          "WHERE ct.category_id=:category_id AND c.visible=TRUE AND t.visible=TRUE ORDER BY t.name ASC"	
    result = db.session.execute(sql, {"category_id": category_id})
    return result.fetchall()
        