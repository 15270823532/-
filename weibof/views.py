import datetime,math

from flask import Blueprint, request, session
from flask import render_template
from flask import redirect, abort

from weibof.models import Weibo
from libs.orm import db
from libs.utils import login_required

weibof_bp = Blueprint('weibof', __name__, url_prefix='/weibof')
weibof_bp.template_folder = './templates'
weibof_bp.static_folder = './static'


@weibof_bp.route('/display', methods=("POST", "GET"))
def display():
    # '''首页展示'''
    if request.method == 'POST':
        try:
            NO=int(request.form.get('NO'))
            return redirect(f'/weibof/display?page={NO}')
        except Exception as e:
            return abort(403)
    else:
        page = int(request.args.get('page', 1))
        per_page = 30
        offset = per_page * (page - 1)
        weibos=Weibo.query.order_by(Weibo.update_time.desc()).limit(per_page).offset(offset)
        # '''获取最大的页码'''
        max_page=math.ceil(Weibo.query.count()/per_page)

        if page<=3:
            start,end=1,min(7,max_page)
        elif page>(max_page-3):
            start,end=max_page-6,max_page
        else:
            start=page-3
            end=page+3
        pages=range(start,end+1)
        return render_template('display.html', weibos=weibos,pages=pages,page=page,max_page=max_page)


@weibof_bp.route('/post', methods=("POST", "GET"))
@login_required
def post():
    if request.method == 'POST':
        uid = session['uid']
        content = request.form.get('content', '').strip()
        now = datetime.datetime.now()
        '''检测微博内容是否为空'''
        if not content:
            return render_template('post.heml', err='微博内容不允许为空')

        weibo = Weibo(uid=uid, content=content, create_time=now, update_time=now)
        db.session.add(weibo)
        db.session.commit()
        # return redirect('/weibof/read?wid=%s' % weibo.id)
    else:
        return render_template('post.html')


@weibof_bp.route('/read')
def read():
    wid = int(request.args.get('wid'))
    weibo = Weibo.query.get(wid)
    return render_template('read.html', weibo=weibo)


@weibof_bp.route('/alter', methods=("POST", "GET"))
@login_required
def alter():
    '''修改微博'''
    if request.method == "POST":
        wid = int(request.form.get('wid'))
        content = request.form.get('content', '').strip()
        now = datetime.datetime.now()
        '''检查微博内容是否为空'''
        weibo = Weibo.query.get(wid)
        if not content:
            return render_template('alter.html', weibo=weibo, err='微博内容不允许为空')
        if weibo.uid != session['uid']:
            abort(403)
        '''更新微博内容'''
        Weibo.query.filter_by(id=wid).update({'content': content, 'update_time': now})
        db.session.commit()
        return redirect(f'/weibof/read?wid={wid}')
    else:
        wid = int(request.args.get('wid'))
        weibo = Weibo.query.get(wid)
        return render_template('alter.html', weibo=weibo)


@weibof_bp.route('/delete')
@login_required
def delete():
    '''删除微博'''
    wid = int(request.args.get('wid'))
    '''检查是否是在删除自己的微博'''
    weibo = Weibo.query.get(wid)
    if weibo.uid == session['uid']:
        db.session.delete(weibo)
        db.session.commit()
        return redirect('/weibof/display')
    else:
        abort(403)
