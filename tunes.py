from db import db

def get_all_tunes(limit=None):
    sql = "SELECT t.id, t.name, t.created, u.username FROM tunes t, users u WHERE t.creator_id=u.id " \
          "AND t.visible=TRUE ORDER BY t.id DESC LIMIT :limit"
    result = db.session.execute(sql, {"limit": limit})
    return result.fetchall()

def get_tune(id):
    sql = "SELECT t.id, t.name, t.notation, t.created, t.creator_id, t.updated, u.username " \
          "FROM tunes t, users u WHERE t.id=:id AND t.creator_id=u.id AND t.visible=TRUE"
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

def update_tune(id, name, notation, categories):
    sql = "UPDATE tunes SET name=:name, notation=:notation, updated=NOW() WHERE id=:id"
    db.session.execute(sql, {"id": id, "name": name, "notation": notation})
    cat_list = tuple(categories)
    sql = "DELETE FROM categories_tunes WHERE tune_id=:tune_id AND category_id NOT IN :list"
    db.session.execute(sql, {"tune_id": id, "list": cat_list})
    sql = "INSERT INTO categories_tunes (category_id, tune_id) SELECT c.id, t.id FROM categories c, tunes t " \
          "WHERE c.id IN :list AND t.id=:tune_id ON CONFLICT (category_id, tune_id) DO NOTHING"
    db.session.execute(sql, {"tune_id": id, "list": cat_list})
    db.session.commit()

def delete_tune(id):
    sql = "DELETE FROM tunes WHERE id=:id RETURNING name"
    result = db.session.execute(sql, {"id": id})
    db.session.commit()
    return result.fetchone()[0]

def get_creator(id):
    sql = "SELECT creator_id FROM tunes WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()[0]

def get_tune_categories(tune_id, include_name=True):
    if include_name:
        sql = "SELECT c.id, c.name FROM categories c, categories_tunes ct WHERE ct.tune_id=:tune_id " \
              "AND c.id=ct.category_id AND c.visible=TRUE"
    else:
        sql="SELECT c.id FROM categories c, categories_tunes ct WHERE ct.tune_id=:tune_id " \
            "AND c.id=ct.category_id AND c.visible=TRUE"
    result = db.session.execute(sql, {"tune_id": tune_id})
    return result.fetchall()

def search_tunes(query):
    sql = "SELECT t.id, t.name, t.created, u.username FROM tunes t, users u WHERE t.name ILIKE :query " \
          "AND t.creator_id=u.id AND t.visible=TRUE"
    result = db.session.execute(sql, {"query": "%"+query+"%"})
    return result.fetchall()
    