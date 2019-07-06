from sqlalchemy import create_engine

import secret
from app import configured_app
from models.base_model import db
from models.board import Board
from models.reply import Reply
from models.topic import Topic
from models.user import User
from models.like import Like


def reset_database():
    # 现在 mysql root 默认用 socket 来验证而不是密码
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(
        secret.database_password
    )
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS bbs')
        c.execute('CREATE DATABASE bbs CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE bbs')

    db.metadata.create_all(bind=e)


def generate_fake_date():
    # 用户
    form = dict(
        username='密码123',
        password='123',
        image='/images/1.jpg'
    )
    u1 = User.register(form)

    form = dict(
        username='密码1234',
        password='1234',
        image='/images/2.png'
    )
    u2 = User.register(form)
    form = dict(
        username='密码abc',
        password='abc',
        image='/images/4.jpg'
    )
    u3 = User.register(form)

    # 板块
    form1 = dict(
        title='吐槽'
    )
    b1 = Board.new(form1)

    form2 = dict(
        title='水区'
    )
    b2 = Board.new(form2)

    form3 = dict(
        title='干货'
    )
    b3 = Board.new(form3)

    # 话题内容
    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()
    topic_form1 = dict(
        title='吐槽 demo',
        board_id=b1.id,
        content=content
    )
    topic_form2 = dict(
        title='水区 demo',
        board_id=b2.id,
        content=content
    )
    topic_form3 = dict(
        title='干货 demo',
        board_id=b3.id,
        content=content
    )

    for i in range(1):
        print('begin topic <{}>'.format(i))
        t1 = Topic.new(topic_form1, u1.id)
        t2 = Topic.new(topic_form2, u2.id)
        t3 = Topic.new(topic_form3, u3.id)
        t4 = Topic.new(topic_form1, u1.id)
        t5 = Topic.new(topic_form2, u2.id)
        t6 = Topic.new(topic_form3, u3.id)
        t7 = Topic.new(topic_form1, u1.id)
        t8 = Topic.new(topic_form2, u2.id)
        t9 = Topic.new(topic_form3, u3.id)

        reply_form = dict(
            content="""
| 表格 | 表格 |
| -    |  -   |
| 表格 | 表格 |
                    """,
        )
        for i in range(3):
            reply_form['topic_id'] = i + 2
            Reply.new(reply_form, u1.id)
            Reply.new(reply_form, u2.id)
            Reply.new(reply_form, u3.id)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_date()
