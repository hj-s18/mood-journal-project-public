from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import pymysql
from app.sql.db_connect import DBConnect  # DB 연결 클래스 가져오기 

# Attendance 관련 Blueprint 생성
attendance_bp = Blueprint('attendance', __name__, url_prefix="/attendance")

# 이번 주의 요일과 날짜 계산 함수
def get_week_dates(user_id=None):
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())  # 이번 주 월요일
    week_days = []
    
    try:
        db = DBConnect.get_db()  # DB 연결 시도
        cursor = db.cursor(pymysql.cursors.DictCursor)

        for i in range(7):
            current_day = start_of_week + timedelta(days=i)
            if user_id:
                cursor.execute("""
                    SELECT * FROM attendance 
                    WHERE user_id = %s AND date = %s
                """, (user_id, current_day.date()))
                attendance = cursor.fetchone()
            else:
                attendance = None  # 사용자 ID가 없을 때는 출석 정보가 없는 상태로 설정

            week_days.append({
                'weekday': current_day.strftime('%A'),
                'date': current_day.strftime('%Y-%m-%d'),
                'attended': bool(attendance)  # 출석 여부 확인
            })
        
        cursor.close()
    except Exception as e:
        print("DB Error:", e)
        for i in range(7):
            current_day = start_of_week + timedelta(days=i)
            week_days.append({
                'weekday': current_day.strftime('%A'),
                'date': current_day.strftime('%Y-%m-%d'),
                'attended': False
            })
    finally:
        db.close()
    
    return week_days

# 출석 체크 페이지 라우트
@attendance_bp.route('/')
def attendance_home():
    user_id = session.get('user_id', 1)  # 테스트용으로 임시 user_id 할당
    week_days = get_week_dates(user_id)  # 이번 주의 날짜와 요일 계산

    # 이번 주 출석 여부 확인
    all_attended = all(day['attended'] for day in week_days)

    # 오늘 출석 여부 확인
    today_date = datetime.today().date()
    today_attendance = any(day['date'] == today_date.strftime('%Y-%m-%d') and day['attended'] for day in week_days)

    return render_template('attendance.html', week_days=week_days, all_attended=all_attended, today_attendance=today_attendance)

# 오늘 출석 처리 라우트
@attendance_bp.route('/mark', methods=['POST'])
def mark_attendance():
    user_id = session.get('user_id', 1)  # 임시로 user_id를 1로 설정하여 테스트
    attendance_date = datetime.today().date()  # 오늘 날짜로 출석 체크

    try:
        db = DBConnect.get_db()
        print("Database connected successfully")
        cursor = db.cursor()

        # 이미 출석했는지 확인
        cursor.execute("""
            SELECT * FROM attendance 
            WHERE user_id = %s AND date = %s
        """, (user_id, attendance_date))
        attendance = cursor.fetchone()
        print("Attendance check query executed")

        if not attendance:
            print("No attendance record found. Inserting new record.")
            cursor.execute("""
                INSERT INTO attendance (user_id, date) VALUES (%s, %s)
            """, (user_id, attendance_date))
            db.commit()
            print("New attendance record committed to the database")
        
        cursor.close()
    except Exception as e:
        print("DB Error:", e)
    finally:
        db.close()

    return redirect(url_for('attendance.attendance_home'))
