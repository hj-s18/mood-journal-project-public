from flask import Blueprint, request, jsonify, current_app

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    current_app.logger.info("회원가입 요청")
    return jsonify({"message": "회원가입 완료"})