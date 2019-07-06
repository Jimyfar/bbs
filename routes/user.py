from flask import (
    render_template,
    Blueprint,
)

from models.user import User
from models.topic import Topic
from models.reply import Reply
from utils import log

main = Blueprint('user', __name__)


@main.route("/<string:username>")
def index(username):
    user = User.one(username=username)
    created_topics = Topic.all_order_by_desc_time(user_id=user.id)
    replies = Reply.all_order_by_desc_time(user_id=user.id)
    # replies.sort(key=lambda r: r.created_time, reverse=True)
    # 通过 reply 查找参与过的 topic 会有重复，所以使用 set 避免加入重复的 topic
    participated_topics_set = set()
    participated_topics = []
    for r in replies:
        t = Topic.one(id=r.topic_id)
        if t not in participated_topics_set:
            participated_topics_set.add(t)
            participated_topics.append(t)
    # 对结果进行时间降序排序
    # topics.sort(key=lambda t: t.created_time, reverse=True)
    log('participated_topics', participated_topics)

    return render_template("user.html",
                           created_topics=created_topics,
                           participated_topics=participated_topics,
                           user=user)

