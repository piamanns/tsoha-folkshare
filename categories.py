from db import db

def add_category(name, user_id):
    try:
        sql = "INSERT INTO categories (name, creator_id, visible) VALUES (:name, " \
              ":creator_id, TRUE) RETURNING name"
        result = db.session.execute(sql, {"name": name, "creator_id": user_id})
        db.session.commit()
        return result.fetchone()[0]
    except:
        return False

def delete_category(category_id):
    sql = "DELETE FROM categories WHERE id=:category_id RETURNING name"
    result = db.session.execute(sql, {"category_id": category_id})
    db.session.commit()
    return result.fetchone()[0]

def set_category_visibility(categories):
    # Show selected
    cat_list = tuple(categories)
    sql = "UPDATE categories SET visible=TRUE WHERE id IN :list"
    db.session.execute(sql, {"list": cat_list})
    # Hide deselected
    sql = "UPDATE categories SET visible=FALSE WHERE id NOT IN :list"
    db.session.execute(sql, {"list": cat_list})
    db.session.commit()

def get_all_categories(include_hidden=False):
    if include_hidden:
        sql = "SELECT id, name, visible FROM categories ORDER BY name" 
    else:
        sql = "SELECT id, name FROM categories WHERE visible=TRUE ORDER BY name"
    result = db.session.execute(sql)
    return result.fetchall()

def get_category_info(category_id):
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
