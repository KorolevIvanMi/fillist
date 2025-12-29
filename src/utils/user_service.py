from database import myDataBase
import utils.requests as rq
from functools import wraps

def is_log_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = myDataBase()
        act_user = rq.get_active_user(db.con)
        print(act_user)
        if act_user == []:
            print("нет авторизованных пользователей!")
            return None
        else:
            return func(*args, **kwargs)
    return wrapper
