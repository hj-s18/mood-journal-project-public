from flask import Blueprint, request, render_template, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

from app.sql.user_db import UserDAO

# 로그인 폼과 로그인을 처리하는 GET/POST 통합 라우트
@auth_bp.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'GET':
        # GET 요청: 로그인 폼 렌더링
        return render_template('login.html')

    elif request.method == 'POST':
        # POST 요청: 로그인 처리
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('모든 필드를 입력해야 합니다.')
            return redirect(url_for('auth.login_user'))

        user_dao = UserDAO()

        try:
            user_info = user_dao.get_user_by_email(email)  # 이메일로 사용자 정보 조회

            if not user_info or user_info['password'] != password:  # 비밀번호 일치 여부 확인
                flash('잘못된 이메일 또는 비밀번호입니다.')
                return redirect(url_for('auth.login_user'))

            # 로그인 성공 시 세션에 사용자 정보 저장 (예: 사용자 ID)
            session['user_id'] = user_info['id']
            session['user_name'] = user_info['name']

            # 환영 메시지를 플래시로 추가
            flash(f'{user_info["name"]}님 환영합니다!')

            return redirect(url_for('diary.diary_home'))  # 로그인 후 diary 페이지로 리다이렉트

        except Exception as e:
            flash(f'오류 발생: {str(e)}')
            return redirect(url_for('auth.login_user'))
        
# 로그아웃 처리를 위한 POST 요청 처리
@auth_bp.route('/logout', methods=['POST'])
def logout():
    # 세션에서 사용자 정보 삭제 (로그아웃 처리)
    session.pop('user_id', None)
    
    # 로그아웃 성공 메시지 플래시
    flash('로그아웃 되었습니다.')
    
    # 로그인 페이지로 리다이렉트
    return redirect(url_for('auth.login_user'))

# 회원가입 폼과 회원가입 처리를 위한 GET/POST 통합 라우트
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup_user():
    if request.method == 'GET':
        # GET 요청: 회원가입 폼 렌더링
        return render_template('signup.html')

    elif request.method == 'POST':
        # POST 요청: 회원가입 처리
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        # 필수 필드 체크
        if not email or not password or not name:
            flash('모든 필드를 입력해야 합니다.')
            return redirect(url_for('auth.signup_user'))

        user_dao = UserDAO()
        try:
            result = user_dao.insert_user(email, password, name)
            flash(result)  # 성공 메시지 플래시
            return redirect(url_for('auth.login_user'))  # 회원가입 완료 후 로그인 페이지로 리다이렉트
        except Exception as e:
            flash(f'오류 발생: {str(e)}')  # 오류 메시지 플래시
            return redirect(url_for('auth.signup_user'))

# 회원정보 수정 폼과 회원정보 수정을 위한 GET/POST 통합 라우트
@auth_bp.route('/update', methods=['GET', 'POST'])
def update_user():
    # 세션에서 사용자 ID를 가져옴
    user_id = session.get('user_id')
    
    if not user_id:
        flash('사용자 ID가 제공되지 않았습니다.')
        return redirect(url_for('auth.login_user'))  # 로그인 페이지로 리다이렉트
    
    user_dao = UserDAO()

    if request.method == 'GET':
        # GET 요청: 회원정보 수정 폼 렌더링
        try:
            user_info = user_dao.get_user_by_id(user_id)  # 해당 사용자의 정보 조회
            if not user_info:
                flash('사용자를 찾을 수 없습니다.')
                return redirect(url_for('auth.login_user'))  # 사용자가 없으면 로그인 페이지로 리다이렉트
            
            return render_template('update.html', user=user_info)  # 수정 폼에 기존 정보 전달
        
        except Exception as e:
            flash(f'오류 발생: {str(e)}')
            return redirect(url_for('auth.login_user'))

    elif request.method == 'POST':
        # POST 요청: 회원정보 수정 처리
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        if not email or not password or not name:
            flash('모든 필드를 입력해야 합니다.')
            return redirect(url_for('auth.update_user'))  # 필드가 비어있으면 다시 수정 폼으로 리다이렉트

        try:
            result = user_dao.update_user(user_id, email, password, name)  # 사용자 정보 업데이트
            flash(result)
            return redirect(url_for('auth.update_user'))  # 업데이트 후 다시 폼으로 리다이렉트
        
        except Exception as e:
            flash(f'오류 발생: {str(e)}')
            return redirect(url_for('auth.update_user'))
        
# 회원 탈퇴 폼과 회원 탈퇴 처리를 위한 GET/POST 통합 라우트
@auth_bp.route('/delete', methods=['GET', 'POST'])
def delete_user():
    # 세션에서 사용자 ID를 가져옴
    user_id = session.get('user_id')
    
    if not user_id:
        flash('로그인이 필요합니다.')
        return redirect(url_for('auth.login_user'))  # 로그인 페이지로 리다이렉트
    
    user_dao = UserDAO()

    if request.method == 'GET':
        # GET 요청: 회원 탈퇴 확인 폼 렌더링
        return render_template('delete.html')

    elif request.method == 'POST':
        # POST 요청: 회원 탈퇴 처리
        try:
            # 데이터베이스에서 사용자 삭제
            result = user_dao.delete_user(user_id)
            
            # 세션에서 사용자 정보 삭제 (로그아웃 처리)
            session.pop('user_id', None)
            
            flash('회원 탈퇴가 완료되었습니다.')
            return redirect(url_for('diary.diary_home'))  # 다이러리 홈 페이지로 리다이렉트
        
        except Exception as e:
            flash(f'오류 발생: {str(e)}')
            return redirect(url_for('auth.delete_user'))  # 오류 발생 시 다시 폼으로 리다이렉트