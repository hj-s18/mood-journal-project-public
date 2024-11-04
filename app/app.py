import logging
from flask import Flask
from .route.auth_route import auth_bp
from .route.sign_route import signup
from .route.sign_update_route import update_bp
from .route.login_route import login_bp
from .route.home_route import home_bp
from .route.delete_route import delete_bp
from .route.logout_route import logout_bp

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
    
    app.register_blueprint(update_bp)
    
    app.register_blueprint(login_bp)
    
    app.register_blueprint(home_bp)

    app.register_blueprint(delete_bp)
    
    app.register_blueprint(logout_bp)
    
    return app