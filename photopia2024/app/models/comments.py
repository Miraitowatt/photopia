from .model import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'
    __table_args__ = {'comment': '评论记录表'}

    comment_id = db.Column(db.Integer(), primary_key=True, autoincrement=True, comment='评论ID')
    user_id = db.Column(db.Integer(), comment='用户ID')
    commented_id = db.Column(db.Integer(), comment='被评论的对象ID')
    comment_content = db.Column(db.Text(), comment='评论内容')
    comment_time = db.Column(db.DateTime(), default=datetime.now, comment='评论时间')

    def __init__(self, user_id, commented_id, comment_content, comment_time=datetime.now()):
        self.user_id = user_id
        self.commented_id = commented_id
        self.comment_content = comment_content
        self.comment_time = comment_time

    def __repr__(self):
        return "<Model Comments '{}'>".format(self.comment_content)
