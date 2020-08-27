import random

from flask import session,redirect
from functools import wraps



def login_required(view_fun):
    @wraps(view_fun)
    def check_session(*args,**kwargs):
        uid=session.get('uid')
        if not uid:
            return redirect('/user/login')
        else:
            return view_fun(*args,**kwargs)
    # check_session.__name__ = view_fun.__name__
    return check_session

def random_hz_str(length):
    words=[chr(random.randint(20000,30000)) for i in range(length)]
    return ''.join(words)


