from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.sql.user_db import UserDAO

# 회원 탈퇴 블루프린트 생성
delete_bp = Blueprint('delete', __name__)

# 회원 탈퇴 폼을 보여주는 GET 요청 처리
@delete_bp.route('/auth/delete', methods=['GET'])
def delete_form():
    # 세션에서 사용자 ID를 가져옴
    user_id = session.get('user_id')
    
    if not user_id:
        flash('로그인이 필요합니다.')
        return redirect(url_for('login.login_form'))  # 로그인 페이지로 리다이렉트
    
    return render_template('delete.html')  # 회원 탈퇴 확인 폼 렌더링

# 회원 탈퇴 처리를 위한 POST 요청 처리
@delete_bp.route('/auth/delete', methods=['POST'])
def delete_user():
    # 세션에서 사용자 ID를 가져옴
    user_id = session.get('user_id')
    
    if not user_id:
        flash('로그인이 필요합니다.')
        return redirect(url_for('login.login_form'))  # 로그인 페이지로 리다이렉트

    user_dao = UserDAO()
    
    try:
        # 데이터베이스에서 사용자 삭제
        result = user_dao.delete_user(user_id)
        
        # 세션에서 사용자 정보 삭제 (로그아웃 처리)
        session.pop('user_id', None)
        
        flash('회원 탈퇴가 완료되었습니다.')
        return redirect(url_for('signup.signup_form'))  # 회원가입 페이지로 리다이렉트
    
    except Exception as e:
        flash(f'오류 발생: {str(e)}')
        return redirect(url_for('delete.delete_form'))