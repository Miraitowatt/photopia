from .model import db

class Places(db.Model):
    __tablename__ = 'places'
    __table_args__ = {'comment': '地点信息表'}

    place_id = db.Column(db.Integer(), primary_key=True, autoincrement=True, comment='地点ID')
    place_name = db.Column(db.Text(), comment='具体地点')
    place_x = db.Column(db.Float(10), comment='经度')
    place_y = db.Column(db.Float(10), comment='维度')
    place_img = db.Column(db.String(), comment='图片的URL')

    def __init__(self, place_name, place_province, place_city, place_x, place_y, place_picture):
        self.place_name = place_name
        self.place_x = place_x
        self.place_y = place_y
        self.place_img = place_img

    def __repr__(self):
        return "<Model Places '{}'>".format(self.place_name)
