
from functools import wraps
import inspect

def is_log_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from database import myDataBase
        import utils.requests as rq

        db = myDataBase()
        act_user = rq.get_active_user(db.con)
        
        if act_user == []:
            print("нет авторизованных пользователей!")
            if hasattr(args[0], "spawn_warning"):
                args[0].spawn_warning()
            return []
        
        sig = inspect.signature(func)
        params = sig.parameters
        
        if 'current_user' in params:
            kwargs['current_user'] = act_user[0]['user_id']
        
        return func(*args, **kwargs)
    return wrapper
