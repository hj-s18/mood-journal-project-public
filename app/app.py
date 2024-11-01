import logging
from flask import Flask
from .route.auth_route import auth_bp
from .route.sign_route import signup


def create_app():
    app = Flask(__name__)
    
    # secret_key 설정 (임의의 문자열로 설정)
    app.secret_key = 'your_secret_key_here' 
    # 고유하고 비밀스러운 문자열로 변경하세요
    
    # 로깅 설정
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    # 블루프린트 등록
    app.register_blueprint(auth_bp)
    
    app.register_blueprint(signup)

    return app