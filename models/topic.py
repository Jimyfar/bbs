import time

from sqlalchemy import String, Integer, Column, Text, UnicodeText, Unicode

from models.base_model import SQLMixin, db
from models.like import Like
from models.user import User
from models.reply import Reply


class Topic(SQLMixin, db.Model):
    views = Column(Integer, nullable=False, default=0)
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    user_id = Column(Integer, nullable=False)
    board_id = Column(Integer, nullable=False)
    likes = Column(Integer, nullable=False, default=0)

    @classmethod
    def new(cls, form, user_id):
        form['user_id'] = user_id
        m = super().new(form)
        return m

    @classmethod
    def get(cls, id):
        m = cls.one(id=id)
        m.views += 1
        m.save()
        return m

    def user(self):
        u = User.one(id=self.user_id)
        return u

    def like(self, user_id):
        Like.new(self.id, user_id)
        self.likes += 1
        self.save()
        return self

    def liked(self, user_id):
        l = Like.one(topic_id=self.id, user_id=user_id)
        print('topic liked', user_id, self.id, l)
        if l is None:
            return False
        else:
            return True

    def replies(self):
        ms = Reply.all(topic_id=self.id)
        return ms

    def reply_count(self):
        count = len(self.replies())
        return count

    def last_reply(self):
        replies = Reply.all(topic_id=self.id)
        if len(replies) > 0:
            return replies[-1]
        else:
            return None

    @classmethod
    def all_order_by_view(cls, **kwargs):
        ms = cls.query.order_by(cls.views.desc()).filter_by(**kwargs).all()
        return ms