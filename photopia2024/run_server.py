import os
from app.router import app
from app.models.model import db

app.secret_key = os.urandom(24)
print(app.secret_key)
with app.app_context():
    # 创建数据库表
    db.create_all()
app.run(host='0.0.0.0', port=3309, debug=True)
