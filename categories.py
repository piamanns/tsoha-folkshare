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

def get_all_categories_count(include_hidden=False):
    if include_hidden:
        sql = "SELECT c.id, c.name, c.visible, COUNT(ct.tune_id) FROM categories c LEFT JOIN categories_tunes ct " \
              "ON c.id=ct.category_id GROUP BY c.id ORDER BY name"
    else:
        sql = "SELECT c.id, c.name, COUNT(ct.tune_id) FROM categories c LEFT JOIN categories_tunes ct " \
              "ON c.id=ct.category_id WHERE c.visible=TRUE GROUP BY c.id ORDER BY name"            
    return db.session.execute(sql).fetchall()         

def get_category_info(category_id, include_hidden=False):
    if include_hidden:
        sql = "SELECT c.name, c.visible, COUNT(ct.tune_id) FROM categories c LEFT JOIN categories_tunes ct ON c.id=ct.category_id "\
            "WHERE c.id=:category_id GROUP BY c.name, c.visible"
    else:  
        sql = "SELECT c.name, COUNT(ct.tune_id) FROM categories c LEFT JOIN categories_tunes ct ON c.id=ct.category_id "\
            "WHERE c.id=:category_id AND c.visible=TRUE GROUP BY c.name"
    result = db.session.execute(sql, {"category_id": category_id})
    return result.fetchone()

def get_category_tunes(category_id):
    sql = "SELECT t.id, t.name, t.created, u.username " \
          "FROM categories_tunes ct JOIN categories c ON ct.category_id=c.id " \
          "JOIN tunes t ON ct.tune_id=t.id JOIN users u ON t.creator_id=u.id " \
          "WHERE ct.category_id=:category_id AND t.visible=TRUE ORDER BY t.name ASC"	
    result = db.session.execute(sql, {"category_id": category_id})
    return result.fetchall()
