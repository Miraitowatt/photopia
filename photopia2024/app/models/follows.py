from .model import db
from datetime import datetime

class Follow(db.Model):
    __tablename__ = 'follows'
    __table_args__ = {'comment': '关注记录表'}
    
    follow_id = db.Column(db.Integer(), primary_key=True, autoincrement=True, comment='关注记录ID')
    follower_id = db.Column(db.Integer(), comment='关注者的用户ID')
    followed_id = db.Column(db.Integer(), comment='被关注者的用户ID')
    follow_time = db.Column(db.DateTime(), default=datetime.now, comment='关注时间')
    
    def __init__(self, follower_id, followed_id, follow_time=None):
        self.follower_id = follower_id
        self.followed_id = followed_id
        self.follow_time = follow_time or datetime.now()
        
    def __repr__(self):
        return "<Model Follow '{}'>".format(self.follower_id)
