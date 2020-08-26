from flask import Blueprint, request,session
from flask import render_template
from flask import redirect

from user.models import User
from libs.orm import db
from libs.utils import login_required

user_bp = Blueprint('user', __name__, url_prefix='/user')
user_bp.template_folder = './templates'
user_bp.static_folder='./static'


@user_bp.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        gender=request.form.get('gender')
        city=request.form.get('city')

        user=User(username=username,password=password,gender=gender,city=city)
        db.session.add(user)
        db.session.commit()
        return redirect('/user/login')
    return render_template('register.html')


@user_bp.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            user=User.query.filter_by(username=username).one()
        except Exception:
            db.session.rollback()
            return '用户名不存在'

        if password and user.password==password:
            session['uid']=user.id
            session['username']=user.username
            return redirect('/weibof/display')
        else:
            return '密码错误'
    else:
        return render_template('login.html')


@user_bp.route('/info')
@login_required
def info():
    uid=session['uid']
    user=User.query.get(uid)
    return render_template('info.html',user=user)

@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


