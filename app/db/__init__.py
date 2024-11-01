from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy 객체 생성
db = SQLAlchemy()

# 모델 임포트
from .user import User
from .diary import Diary
from .attendance import Attendance

def init_db(app):
    db.init_app(app)
    
    with app.app_context():
        db.create_all()