from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.like import Like
from models.topic import Topic
from routes import *

from models.message import Messages

main = Blueprint('mail', __name__)


@main.route("/add", methods=["POST"])
def add():
    form = request.form.to_dict()
    u = current_user()
    receiver_name = form['receiver_name']
    r = User.one(username=receiver_name)
    receiver_id = r.id
    # 发邮件
    Messages.send(
        title=form['title'],
        content=form['content'],
        sender_id=u.id,
        receiver_id=receiver_id,
        type=form['type'],
    )

    return redirect(url_for('.index'))


@main.route('/')
def index():
    u = current_user()

    send = Messages.all(sender_id=u.id, type='private_letter')
    received = Messages.all(receiver_id=u.id, type='private_letter')

    t = render_template(
        'mail/index.html',
        user=u,
        send=send,
        received=received,
    )
    return t


@main.route('/view/<int:id>')
def view(id):
    message = Messages.one(id=id)
    u = current_user()
    # if u.id == mail.receiver_id or u.id == mail.sender_id:
    if u.id in [message.receiver_id, message.sender_id]:
        return render_template('mail/detail.html', message=message)
    else:
        return redirect(url_for('.index'))


@main.route('/at_me')
def at_me():
    u = current_user()

    received = Messages.all(receiver_id=u.id, type='at_me')

    t = render_template(
        'mail/at_me.html',
        user=u,
        received=received,
    )
    return t


@main.route('/reply_me')
def reply_me():
    u = current_user()

    received = Messages.all(receiver_id=u.id, type='reply_me')

    t = render_template(
        'mail/reply_me.html',
        user=u,
        received=received,
    )
    return t


@main.route('/like_me')
def like_me():
    u = current_user()

    received = Messages.all(receiver_id=u.id, type='like_me')

    t = render_template(
        'mail/like_me.html',
        user=u,
        received=received,
    )
    return t


