from .model import db
from datetime import datetime

class Collect(db.Model):
    __tablename__ = 'collects'
    __table_args__ = {'comment': '收藏记录表'}
    
    collect_id = db.Column(db.Integer(), primary_key=True, autoincrement=True,comment='收藏记录ID')
    user_id = db.Column(db.Integer(),comment='收藏用户ID')
    collected_id = db.Column(db.Integer(),comment='被赞作品ID')
    collect_time = db.Column(db.DateTime(), default = datetime.now(),comment='收藏时间')
    
    def __init__(self, user_id, collected_id, collect_time):
        self.user_id = user_id
        self.collected_id = collected_id
        self.collect_time = collect_time
        
        
    def __repr__(self):
        return "<Model COLLECTS '{}'>".format(self.collect_id)