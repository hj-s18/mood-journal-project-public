from flask import Blueprint, request, jsonify, current_app

auth_bp = Blueprint('auth', __name__)


# sign_route.py 만들면서 라우팅 경로 충돌 나서 일단 주석 해놨어요.

# @auth_bp.route('/signup', methods=['GET', 'POST'])
# def signup():
#     current_app.logger.info("회원가입 요청")
#     return jsonify({"message": "회원가입 완료"})