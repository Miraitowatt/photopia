from .model import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'comment': '用户信息表'}
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    user_name = db.Column(db.String(255), nullable=False, comment='用户登录名')
    password = db.Column(db.String(255), nullable=False, comment='用户密码')
    name = db.Column(db.String(255), nullable=False, comment='用户昵称')
    birthday = db.Column(db.DateTime, comment='用户生日')
    gender = db.Column(db.Boolean, default=True, comment='用户性别，True为男性，False为女性')
    photo = db.Column(db.String(255), default='https://ts1.cn.mm.bing.net/th/id/R-C.232904c2ee9450d3afabd2c553477793?rik=Wrs6xV46pcnU%2fg&riu=http%3a%2f%2fwww.sucaijishi.com%2fuploadfile%2f2016%2f0203%2f20160203022635285.png&ehk=qK8HIsKsLMdhbBUdvvlQJnmEw7K%2fpbcfFp5ZrHO2F9w%3d&risl=&pid=ImgRaw&r=0', comment='用户头像URL')
    power = db.Column(db.Integer, comment='用户权限等级')
    self_description = db.Column(db.Text, comment='用户自我描述')
    email = db.Column(db.String(255), comment='用户邮箱')
    register_time = db.Column(db.DateTime, comment='用户注册时间')
    last_login = db.Column(db.DateTime, default=datetime.now, comment='用户最后登录时间')
    
    def __init__(self, user_name, name, password, birthday=None, gender=None, photo=None, power=1, self_description=None, email=None, register_time=datetime.now(), last_login=None):
        self.user_name = user_name
        self.password = password
        self.birthday = birthday
        self.gender = gender
        self.photo = photo
        self.power = power
        self.name = name
        self.self_description = self_description
        self.email = email
        self.register_time = register_time or datetime.now()
        self.last_login = last_login

    def __repr__(self):
        return f"<Model USERS '{self.name}'>"
