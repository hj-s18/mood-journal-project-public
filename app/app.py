import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask
from .route.auth_route import auth_bp
from .route.home_route import home_bp
from .route.attendance_route import attendance_bp
from .route.diary_route import diary_bp
from .route.achievements_route import achievements_bp
from datetime import datetime

def create_app():
    app = Flask(__name__)
    
    # secret_key 설정 (임의의 문자열로 설정)
    app.secret_key = 'your_secret_key_here' 
    # 고유하고 비밀스러운 문자열로 변경하세요
        
    # 로깅 설정
    logger = logging.getLogger("logging_file")
    file_handler = TimedRotatingFileHandler(
        f"logs/logging_file_{datetime.now().strftime('%Y-%m-%d')}.log",     # 로그 파일 경로
        when="midnight",                # 매일 자정에 새로운 로그 파일 생성
        interval=1,                     # 1일마다 파일 생성
        backupCount=7                   # 7개의 백업 파일 유지
    )
    
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(process)d %(message)s")
    file_handler.setFormatter(formatter)
    
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.DEBUG)
    

    # 블루프린트 등록
    app.register_blueprint(auth_bp)    
    app.register_blueprint(home_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(diary_bp)
    app.register_blueprint(achievements_bp)

    return app
