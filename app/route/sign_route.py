from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.sql.user_db import UserDAO  # user_db 모듈에서 UserDAO 가져오기

signup = Blueprint('signup', __name__)

# 회원가입 폼을 보여주는 GET 요청 처리
@signup.route('/signup', methods=['GET'])
def signup_form():
    return render_template('signup.html')  # signup.html 템플릿 렌더링

# 회원가입 처리를 위한 POST 요청 처리
@signup.route('/signup', methods=['POST'])
def signup_user():
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')

    # 필수 필드 체크
    if not email or not password or not name:
        flash('모든 필드를 입력해야 합니다.')
        return redirect(url_for('signup.signup_form'))

    user_dao = UserDAO()
    try:
        result = user_dao.insert_user(email, password, name)
        flash(result)  # 성공 메시지 플래시
        return redirect(url_for('signup.signup_form'))  # 회원가입 완료 후 다시 폼으로 리다이렉트
    except Exception as e:
        flash(f'오류 발생: {str(e)}')  # 오류 메시지 플래시
        return redirect(url_for('signup.signup_form'))