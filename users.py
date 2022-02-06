from db import db
from flask import session, abort
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

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
    session["user_role"] = user.role
    session["csrf_token"] = secrets.token_hex(16)
    return True

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["user_role"]
    del session["csrf_token"]

def user_id():
    return session.get("user_id", 0)

def user_role():
    return session.get("user_role", 0)

def check_csrf(form_token):
    if session["csrf_token"] != form_token:
        abort(403)
