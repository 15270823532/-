import datetime

from flask import Blueprint,request,session
from flask import render_template
from flask import redirect

from weibof.models import Weibo
from libs.orm import db

weibof_bp=Blueprint('weibof',__name__,url_prefix='/weibof')
weibof_bp.template_folder='./templates'
weibof_bp.static_folder='./static'


@weibof_bp.route('/display')
def display():
    weibos = Weibo.query.order_by(Weibo.created_time.desc()).all()
    return render_template('display.html', weibos=weibos)

@weibof_bp.route('/post', methods=("POST", "GET"))
def post():
    if request.method=='POST':
        title=request.form.get('title')
        content=request.form.get('content')
        now=datetime.datetime.now()

        weibo=Weibo(title=title,content=content,created_time=now)
        db.session.add(weibo)
        db.session.commit()
        return redirect('/weibof/read?wid=%s' % weibo.id)
    else:
        return render_template('post.html')

@weibof_bp.route('/read')
def read():
    wid=int(request.args.get('wid'))
    weibo=Weibo.query.get(wid)
    return render_template('read.html',weibo=weibo)

# @weibof_bp.route('/alter')
# def alter():
#     return render_template('alter.html')

@weibof_bp.route('/delete')
def delete():
    wid=int(request.args.get('wid'))
    Weibo.query.filter_by(id=wid).delete()
    db.session.commit()
    return redirect('weibof/display')