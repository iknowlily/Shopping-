from functools import wraps

from models import db
from flask import session, g,redirect


def required_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return redirect('/')
        sql = f"select * from user_ORM where id={user_id}"
        db.cursor.execute(sql)
        user = db.cursor.fetchone()
        if not user:
            return {
                'status': 'failure',
                'message': 'The user not exist.'
            }
        g.user = user  # If previously logged in, load user data into the g object
        ret = func(*args, **kwargs)
        return ret

    return wrapper
