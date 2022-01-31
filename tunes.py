from db import db

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
