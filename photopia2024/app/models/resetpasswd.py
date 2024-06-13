from .model import db
from datetime import datetime

class PasswordResetCode(db.Model):
    __tablename__ = 'resetpasswd'
    __table_args__ = {'comment': '重置密码表'}
    
    reset_id = db.Column(db.Integer(), primary_key=True, autoincrement=True, comment='重置密码请求ID')
    user_id = db.Column(db.Integer(), comment='用户ID')
    reset_date = db.Column(db.DateTime(), default=datetime.now, comment='请求重置密码的日期时间')
    old_passwd = db.Column(db.String(255), comment='用户原密码')
    new_passwd = db.Column(db.String(255), comment='用户新密码')

    def __init__(self, user_id, old_passwd, new_passwd, reset_date=datetime.now()):
        self.user_id = user_id
        self.reset_date = reset_date
        self.old_passwd = old_passwd
        self.new_passwd = new_passwd
        
    def __repr__(self):
        return "<Model PasswordResetCode '{}'>".format(self.reset_date)
