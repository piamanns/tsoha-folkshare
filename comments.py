from db import db

def add_comment(user_id, tune_id, comment):
    sql = "INSERT INTO comments (creator_id, tune_id, comment, created, visible) " \
          "VALUES (:user_id, :tune_id, :comment, NOW(), TRUE) RETURNING tune_id"
    result = db.session.execute(sql, {"user_id": user_id, "tune_id": tune_id, "comment": comment})
    db.session.commit()
    return result.fetchone()[0]

def get_tune_comments(tune_id):
    sql = "SELECT c.id, c.comment, c.created, u.username FROM comments c, users u WHERE c.tune_id=:tune_id " \
          "AND c.creator_id=u.id ORDER BY c.id"
    result = db.session.execute(sql, {"tune_id": tune_id})
    return result.fetchall()

def delete_comment(comment_id):
    sql = "DELETE FROM comments WHERE id=:comment_id RETURNING tune_id"
    result = db.session.execute(sql, {"comment_id": comment_id})
    db.session.commit()
    return result.fetchone()[0]
    