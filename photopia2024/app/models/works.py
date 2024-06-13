from .model import db
from sqlalchemy import CheckConstraint

class Artworks(db.Model):
    __tablename__ = 'works'
    __table_args__ = (
        CheckConstraint('artwork_type IN (1, 2, 3, 4, 5)', name='check_artwork_type'),
        {'comment': '图片作品信息表'}
    )

    artwork_id = db.Column(db.Integer(), primary_key=True, autoincrement=True, comment='作品ID')
    artwork_name = db.Column(db.String(255), comment='作品名称')
    artwork_description = db.Column(db.Text(), comment='作品描述')
    artwork_time = db.Column(db.DateTime(), comment='作品发布时间')
    artwork_type = db.Column(db.Integer(), comment='摄影类型:1-风光,2-人文,3-人像,4-静物,5-其他')
    user_id = db.Column(db.Integer(), comment='发布用户ID')
    artwork_picture = db.Column(db.String(255), nullable=False, comment='图片的URL')  # 确保图片URL不为空
    keyword1 = db.Column(db.Text(), comment='关键词1')
    keyword2 = db.Column(db.Text(), comment='关键词2')
    keyword3 = db.Column(db.Text(), comment='关键词3')
    keyword4 = db.Column(db.Text(), comment='关键词4')
    keyword5 = db.Column(db.Text(), comment='关键词5')

    def __init__(self, artwork_name, artwork_description, artwork_time, artwork_type, user_id, artwork_picture, keyword1, keyword2, keyword3, keyword4, keyword5):
        self.artwork_name = artwork_name
        self.artwork_description = artwork_description
        self.artwork_time = artwork_time
        self.artwork_type = artwork_type
        self.user_id = user_id
        self.artwork_picture = artwork_picture
        self.keyword1 = keyword1
        self.keyword2 = keyword2
        self.keyword3 = keyword3
        self.keyword4 = keyword4
        self.keyword5 = keyword5

    def __repr__(self):
        return f"<Model Artworks '{self.artwork_name}'>"
