from flask import Blueprint, render_template
from datetime import datetime, timedelta

# Attendance 관련 Blueprint 생성 (url_prefix로 '/attendance' 경로 설정)
attendance_bp = Blueprint('attendance', __name__, url_prefix="/attendance")

# 이번 주의 요일과 날짜 계산 함수
def get_week_dates():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())  # 이번 주 월요일
    week_days = []
    
    for i in range(7):
        current_day = start_of_week + timedelta(days=i)
        week_days.append({
            'weekday': current_day.strftime('%A'),  # 요일 이름 (예: Monday)
            'date': current_day.strftime('%Y-%m-%d'),  # 날짜 (예: 2023-11-03)
            'attended': False  # 임시로 출석 여부는 False로 설정
        })
    
    return week_days

@attendance_bp.route('/')
def attendance_home():
    week_days = get_week_dates()  # 이번 주의 날짜와 요일 계산
    return render_template('attendance.html', week_days=week_days)
