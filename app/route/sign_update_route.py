from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.sql.user_db import UserDAO

# 회원정보 수정 블루프린트 생성
update_bp = Blueprint('update', __name__)

# 회원정보 수정 폼을 보여주는 GET 요청 처리
@update_bp.route('/auth/update', methods=['GET'])
def update_form():
    # 세션에서 사용자 ID를 가져옴
    user_id = session.get('user_id')
    
    if not user_id:
        flash('사용자 ID가 제공되지 않았습니다.')
        return redirect(url_for('login.login_form'))  # 로그인 페이지로 리다이렉트
    
    user_dao = UserDAO()
    
    try:
        user_info = user_dao.get_user_by_id(user_id)  # 해당 사용자의 정보 조회
        if not user_info:
            flash('사용자를 찾을 수 없습니다.')
            return redirect(url_for('login.login_form'))  # 사용자가 없으면 로그인 페이지로 리다이렉트
        
        return render_template('update.html', user=user_info)  # 수정 폼에 기존 정보 전달
    
    except Exception as e:
        flash(f'오류 발생: {str(e)}')
        return redirect(url_for('login.login_form'))

# 회원정보 수정을 위한 POST 요청 처리
@update_bp.route('/auth/update', methods=['POST'])
def update_user():
    # 세션에서 사용자 ID를 가져옴
    user_id = session.get('user_id')
    
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')

    if not email or not password or not name or not user_id:
        flash('모든 필드를 입력해야 합니다.')
        return redirect(url_for('update.update_form'))  # 필드가 비어있으면 다시 수정 폼으로 리다이렉트

    user_dao = UserDAO()
    
    try:
        result = user_dao.update_user(user_id, email, password, name)  # 사용자 정보 업데이트
        flash(result)
        return redirect(url_for('update.update_form'))  # 업데이트 후 다시 폼으로 리다이렉트
    
    except Exception as e:
        flash(f'오류 발생: {str(e)}')
        return redirect(url_for('update.update_form'))