# _*_ coding: utf-8 _*_

import time
from app import db
from app.models import SMS_Receive
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
import datetime
from flask import render_template, request, current_app, redirect, url_for
from . import main
from .forms import PostForm


@main.route('/')
def index():
    title = '首 页'
    keyword = '在线短信接收,sms_receive,短信接收,短信验证码接收'
    description = '本平台可以在线接收短信，接收短信验证码，显示迅速，与国外类似短信验证码接收更快捷。'
    msg_count = db.session.query(sqlalchemy.func.count(SMS_Receive.id)).scalar()
    last_time = db.session.query(SMS_Receive).order_by(SMS_Receive.SMS_ReceiveTime.desc()).first().SMS_ReceiveTime
    start_time = datetime.datetime.now()
    # 计算时差
    ms = (start_time - last_time).seconds
    if ms >= 86400:
        days = ms // 86400
        time_info = '%d天' % (days)
    elif ms >= 3600:
        hour = ms // 3600
        time_info = "%d小时" % (hour)
    elif ms >= 60:
        minute = ms // 60
        time_info = '%d分钟' % (minute)
    else:
        time_info = '%d秒' % (ms)
    return render_template("index.html", name=title, keywords=keyword, description=description,
                           SMS_Count=msg_count, timeInfo=time_info, current_time=start_time)


@main.route('/SMSContent')
def SMSContent():
    title = '首 页'
    keyword = '在线短信接收,sms_receive,短信接收,短信验证码接收'
    description = '本平台可以在线接收短信，接收短信验证码，显示迅速，与国外类似短信验证码接收更快捷。'
    # 选择最新4条短信内容
    font_list_four = db.session.query(SMS_Receive).order_by(SMS_Receive.SMS_ReceiveTime.desc()).limit(4)
    # 如果没有数据，默认显示第一页
    page = request.args.get('page', 1, type=int)
    # 选最剩余短信内容
    pagination = db.session.query(SMS_Receive).from_self() \
        .order_by(SMS_Receive.SMS_ReceiveTime.desc()) \
        .paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    surplus = pagination.items
    return render_template("sms_content.html", name=title, keywords=keyword, description=description,
                           list_four=font_list_four, list_surplus=surplus, pagination=pagination)


@main.route('/SMSServer', methods=['POST'])
def SMSServer():
    address = request.values.get('address', 0)
    get_date = str(request.values.get('date', 0))
    # 转换时间
    tl = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(get_date[0:10])))
    msg = request.values.get('msg', 0)
    type = request.values.get('type', 0)
    content = SMS_Receive(PhoneNumber=address, Content=msg, Type=type, SMS_ReceiveTime=tl)
    try:
        db.session.add(content)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return '1'
    else:
        return '0'


@main.route('/article/<num>', methods=['GET'])
def article(num):
    return


@main.route('/article/edit/<num>', methods=['GET', 'POST'])
def edit(num):
    return


@main.route('/article/post', methods=['GET', 'POST'])
def post():
    form = PostForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('post.html', form=form)
