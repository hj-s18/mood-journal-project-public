from flask import Blueprint, redirect, url_for, session, flash

# 로그아웃 블루프린트 생성
logout_bp = Blueprint('logout', __name__)

# 로그아웃 처리를 위한 POST 요청 처리
@logout_bp.route('/logout', methods=['POST'])
def logout():
    # 세션에서 사용자 정보 삭제 (로그아웃 처리)
    session.pop('user_id', None)
    
    # 로그아웃 성공 메시지 플래시
    flash('로그아웃 되었습니다.')
    
    # 로그인 페이지로 리다이렉트
    return redirect(url_for('login.login_form'))