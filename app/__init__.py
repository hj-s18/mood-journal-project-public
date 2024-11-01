from flask import Flask
from .db import init_db
from .route import init_routes

def create_app():
    app = Flask(__name__)

    # 데이터베이스 설정    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:test1234!@localhost:3306/mood_journal_project'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    init_db(app)

    # 블루프린트 등록
    init_routes(app)

    return app