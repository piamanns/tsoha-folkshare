from db import db

def get_all_tunes():
    sql = "SELECT t.id, t.name, t.created, u.username FROM tunes t, users u WHERE t.creator_id=u.id " \
          "AND t.visible=TRUE ORDER BY t.id DESC"
    return db.session.execute(sql).fetchall()

def get_latest_tunes():
    sql = "SELECT t.id, t.name, t.created, u.username FROM tunes t, users u WHERE t.creator_id=u.id " \
          "AND t.visible=TRUE ORDER BY t.id DESC LIMIT 10"
    return db.session.execute(sql).fetchall()

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

def get_all_categories(include_hidden=False):
    if include_hidden:
        sql = "SELECT id, name, visible FROM categories ORDER BY name" 
    else:
        sql = "SELECT id, name FROM categories WHERE visible=TRUE ORDER BY name"
    result = db.session.execute(sql)
    return result.fetchall()

def get_tune_categories(tune_id, include_name=True):
    if include_name:
        sql = "SELECT c.id, c.name FROM categories c, categories_tunes ct WHERE ct.tune_id=:tune_id " \
              "AND c.id=ct.category_id AND c.visible=TRUE"
    else:
        sql="SELECT c.id FROM categories c, categories_tunes ct WHERE ct.tune_id=:tune_id " \
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

def add_category(name, user_id):
    try:
        sql = "INSERT INTO categories (name, creator_id, visible) VALUES (:name, " \
              ":creator_id, TRUE) RETURNING name"
        result = db.session.execute(sql, {"name": name, "creator_id": user_id})
        db.session.commit()
        return result.fetchone()[0]
    except:
        return False

def set_category_visibility(categories):
    # Show selected
    cat_list = tuple(categories)
    sql = "UPDATE categories SET visible=TRUE WHERE id IN :list"
    db.session.execute(sql, {"list": cat_list})
    # Hide deselected
    sql = "UPDATE categories SET visible=FALSE WHERE id NOT IN :list"
    db.session.execute(sql, {"list": cat_list})
    db.session.commit()

def delete_category(category_id):
    sql = "DELETE FROM categories WHERE id=:category_id RETURNING name"
    result = db.session.execute(sql, {"category_id": category_id})
    db.session.commit()
    return result.fetchone()[0]