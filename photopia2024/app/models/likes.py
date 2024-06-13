from .model import db
from datetime import datetime
from sqlalchemy import CheckConstraint

class Like(db.Model):
    __tablename__ = 'likes'
    __table_args__ = {'comment': '点赞记录表'}
    
    like_id = db.Column(db.Integer(), primary_key=True, autoincrement=True,comment="点赞记录ID")
    user_id = db.Column(db.Integer(),comment='点赞用户ID')
    liked_id = db.Column(db.Integer(),comment='被赞作品ID')
    like_time = db.Column(db.DateTime(), default = datetime.now(),comment='点赞时间')
    like_type = db.Column(db.Integer(),comment='点赞类型:1-作品点赞,2-评论点赞')

    __table_args__ = (
        CheckConstraint('like_type IN (1, 2)', name='check_like_type'),
    )
    
    def __init__(self, user_id, liked_id, like_time,like_type):
        self.user_id = user_id
        self.liked_id = liked_id
        self.like_time = like_time
        self.like_type = like_type

        
    def __repr__(self):
        return "<Model LIKES '{}'>".format(self.like_id)