from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.sql.user_db import UserDAO

login_bp = Blueprint('login', __name__)

# 로그인 폼을 보여주는 GET 요청 처리
@login_bp.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')  # login.html 템플릿 렌더링

# 로그인 처리를 위한 POST 요청 처리
@login_bp.route('/login', methods=['POST'])
def login_user():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('모든 필드를 입력해야 합니다.')
        return redirect(url_for('login.login_form'))

    user_dao = UserDAO()
    
    try:
        user_info = user_dao.get_user_by_email(email)  # 이메일로 사용자 정보 조회
        
        if not user_info or user_info['password'] != password:  # 비밀번호 일치 여부 확인 (해싱 안 한 경우)
            flash('잘못된 이메일 또는 비밀번호입니다.')
            return redirect(url_for('login.login_form'))

        # 로그인 성공 시 세션에 사용자 정보 저장 (예: 사용자 ID)
        session['user_id'] = user_info['id']
        flash(f'{user_info["name"]}님 환영합니다!')
        
        return redirect(url_for('home.home'))  # 로그인 후 home 페이지로 리다이렉트
    
    except Exception as e:
        flash(f'오류 발생: {str(e)}')
        return redirect(url_for('login.login_form'))