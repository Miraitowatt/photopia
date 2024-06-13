from .model import db

class Devices(db.Model):
    __tablename__ = 'devices'
    __table_args__ = {'comment': '设备信息表'}

    device_id = db.Column(db.Integer(), primary_key=True, autoincrement=True, comment='设备ID')
    device_name = db.Column(db.Text(), comment='设备名称')
    device_brand = db.Column(db.Text(), comment='设备品牌')
    device_score = db.Column(db.Integer(), comment='设备评分')
    device_dr = db.Column(db.Float(), comment='动态范围')
    device_iso = db.Column(db.Float(), comment='最大ISO')
    device_type = db.Column(db.Text(), comment='设备类型')
    device_picture = db.Column(db.String(255), comment='设备图片的URL')
    device_url = db.Column(db.String(255), comment='设备购买的URL')


    def __init__(self, device_name, device_description, device_brand, device_type, device_price, device_url):
        self.device_name = device_name
        self.device_dr = device_dr
        self.device_iso = device_iso
        self.device_score = device_score
        self.device_brand = device_brand
        self.device_type = device_type
        self.device_picture = device_picture
        self.device_url = device_url

    def __repr__(self):
        return "<Model Devices '{}'>".format(self.device_name)
