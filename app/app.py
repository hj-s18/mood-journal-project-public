import logging
from flask import Flask
from .route.auth_route import auth_bp
from .route.attendance_route import attendance_bp
from .route.diary_route import diary_bp

def create_app():
    app = Flask(__name__)

    # 로깅 설정
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    # 블루프린트 등록
    app.register_blueprint(auth_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(diary_bp)

    return app