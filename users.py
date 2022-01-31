from db import db
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, role) VALUES (:username, :password, :role)"
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role})
        db.session.commit()
    except:
        return False
    return login(username, password)

def login(username, password):
    sql = "SELECT id, username, password, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user.password, password):
        return False
    session["user_id"] = user.id
    session["user_name"] = user.username
    return True

def logout():
    del session["user_id"]
    del session["user_name"]

def user_id():
    return session.get("user_id", 0)
