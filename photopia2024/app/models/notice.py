from .model import db
from datetime import datetime

class Notice(db.Model):
    __tablename__ = 'notice'
    __table_args__ = {'comment': '公告信息表'}

    notice_id = db.Column(db.Integer(), primary_key=True, autoincrement=True, comment='公告ID')
    user_id = db.Column(db.Integer(), comment='发布公告的用户ID')
    notice_name = db.Column(db.Text(), nullable=False, comment='公告标题')
    notice_content = db.Column(db.Text(), nullable=False, comment='公告内容')
    notice_time = db.Column(db.DateTime(), default=datetime.now, comment='公告发布时间')
    notice_picture = db.Column(db.String(255), nullable=False, comment='图片的URL')  # 确保图片URL不为空

    def __init__(self, user_id, notice_name, notice_content, notice_time=None):
        self.user_id = user_id
        self.notice_name = notice_name
        self.notice_content = notice_content
        self.notice_time = notice_time if notice_time is not None else datetime.now()
        self.notice_picture = notice_picture
    def __repr__(self):
        return f"<Model Notice '{self.notice_name}'>"
