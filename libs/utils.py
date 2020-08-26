from flask import session,redirect



def login_required(view_fun):
    def check_session(*args,**kwargs):
        uid=session.get('uid')
        if not uid:
            return redirect('/user/login')
        else:
            return view_fun(*args,**kwargs)
    check_session.__name__ = view_fun.__name__
    return check_session
