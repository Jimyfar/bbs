from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.message import Messages
from models.reply import Reply
from routes import *

from models.topic import Topic
from models.board import Board


main = Blueprint('topic', __name__)


@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
        top10_ms = Topic.all_order_by_view()[:10]
    else:
        ms = Topic.all(board_id=board_id)
        top10_ms = Topic.all_order_by_view(board_id=board_id)[:10]
    token = new_csrf_token()
    bs = Board.all()
    return render_template("topic/index.html", ms=ms, token=token, bs=bs, bid=board_id, user=current_user(), top10_ms=top10_ms)


@main.route('/<int:id>')
def detail(id):
    u = current_user()
    m = Topic.get(id)
    # 传递 topic 的所有 reply 到 页面中
    liked = m.liked(u.id)
    return render_template("topic/detail.html", topic=m, user=u, liked=liked, id=m.id)


@main.route("/delete")
@csrf_required
def delete():
    u = current_user()
    created = 'created_topic_{}'.format(u.id)
    replied = 'replied_topic_{}'.format(u.id)
    cache.delete(created, replied)

    id = int(request.args.get('id'))
    print('删除 topic 用户是', u, id)
    t = Topic.one(id=id)
    for r in t.replies():
        Reply.delete(r.id)

    Topic.delete(id)
    return redirect(url_for('.index'))


@main.route("/new")
def new():
    board_id = int(request.args.get('board_id'))
    bs = Board.all()
    # return render_template("topic/new.html", bs=bs, bid=board_id)
    token = new_csrf_token()
    return render_template("topic/new.html", bs=bs, token=token, bid=board_id)


@main.route("/like")
def like():
    u = current_user()
    id = int(request.args.get('id'))
    t = Topic.one(id=id)
    print('like tid', t.id)
    t.like(u.id)
    send_like_me(u, t.user(), request.referrer, t.title)
    return redirect(url_for('.detail', id=t.id))


@main.route("/add", methods=["POST"])
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    Topic.new(form, user_id=u.id)
    return redirect(url_for('.index'))


def send_like_me(sender, receiver, topic_link, topic_title):
    print('send_reply_me', sender, receiver, topic_title)
    content = topic_link

    title = '{} 点赞了你的 {}'.format(sender.username, topic_title)
    Messages.send(
        title=title,
        content=content,
        sender_id=sender.id,
        receiver_id=receiver.id,
        type='like_me',
    )