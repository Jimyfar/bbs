import time

from sqlalchemy import Column, Integer, UnicodeText

from models.base_model import db, SQLMixin
from models.user import User


class Like(SQLMixin, db.Model):
    topic_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    def user(self):
        u = User.one(id=self.user_id)
        return u

    @classmethod
    def new(cls, topic_id, user_id):
        form = dict(
            topic_id=topic_id,
            user_id=user_id
        )
        m = super().new(form)
        return m


