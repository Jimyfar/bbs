#!/usr/bin/env python3
import time

from flask import Flask

import secret
import config
from models.base_model import db

from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.user import main as user_routes
from routes.board import main as board_routes
from routes.message import main as mail_routes
from routes.reset import main as reset_routes
from routes.setting import main as setting_routes
from utils import log


def count(input):
    # log('count using jinja filter')
    if input is None:
        return 0
    return len(input)


def format_time(unix_timestamp):
    # enum Year():
    #     2013
    #     13
    # f = Year.2013
    f = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(unix_timestamp)
    formatted = time.strftime(f, value)
    return formatted


def time_between_now(unix_timestamp):
    """
    计算到现在间隔了多少时间，如果超过一年，就是 x 年前，如果超过一个月，就是 x 个月前，以此类推到 x 秒前。
    :param unix_timestamp:
    :return:
    """
    now = int(time.time())
    now_dict = time_dict(now)
    t_dict = time_dict(unix_timestamp)
    # log('t_dict and now_dict', t_dict, now_dict)
    year_from_now = now_dict['year'] - t_dict['year']
    month_from_now = now_dict['month'] - t_dict['month']
    day_from_now = now_dict['day'] - t_dict['day']
    hour_from_now = now_dict['hour'] - t_dict['hour']
    minute_from_now = now_dict['minute'] - t_dict['minute']
    second_from_now = now_dict['second'] - t_dict['second']

    if year_from_now > 0:
        return str(year_from_now) + "年前"
    if month_from_now > 0:
        return str(month_from_now) + "个月前"
    if day_from_now > 0:
        return str(day_from_now) + "天前"
    if hour_from_now > 0:
        return str(hour_from_now) + "小时前"
    if minute_from_now > 1:
        return str(minute_from_now) + "分钟前"
    if second_from_now > 0:
        return str(second_from_now) + "秒前"


def time_dict(unix_timestamp):
    """
    使用字典存储时间
    {'year': 2019, 'month': 6, 'day': 18, 'hour': 8, 'minute': 56, 'second': 14}
    :param unix_timestamp:
    :return:
    """
    t = format_time(unix_timestamp)
    # 2019-06-18 00:43:41
    date_of_time = t.split(' ')[0].split('-')
    clock_of_time = t.split(' ')[1].split(':')
    time_dict = dict(
        year=int(date_of_time[0]),
        month=int(date_of_time[1]),
        day=int(date_of_time[2]),
        hour=int(clock_of_time[0]),
        minute=int(clock_of_time[1]),
        second=int(clock_of_time[2]),
    )
    return time_dict


def configured_app():
    # web framework
    # web application
    # __main__
    app = Flask(__name__)
    # 设置 secret_key 来使用 flask 自带的 session
    # 这个字符串随便你设置什么内容都可以
    app.secret_key = secret.secret_key

    uri = 'mysql+pymysql://root:{}@localhost/bbs?charset=utf8mb4'.format(
        secret.database_password
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    register_routes(app)
    return app


def register_routes(app):
    """
    在 flask 中，模块化路由的功能由 蓝图（Blueprints）提供
    蓝图可以拥有自己的静态资源路径、模板路径（现在还没涉及）
    用法如下
    """
    # 注册蓝图
    # 有一个 url_prefix 可以用来给蓝图中的每个路由加一个前缀

    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(mail_routes, url_prefix='/mail')
    app.register_blueprint(reset_routes, url_prefix='/reset')
    app.register_blueprint(setting_routes, url_prefix='/setting')
    app.register_blueprint(user_routes, url_prefix='/user')

    app.template_filter()(count)
    app.template_filter()(format_time)
    app.template_filter()(time_between_now)


# 运行代码
if __name__ == '__main__':
    app = configured_app()
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    # 自动 reload jinja
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost' ,
        port=3000,
        threaded=True,
    )
    app.run(**config)
