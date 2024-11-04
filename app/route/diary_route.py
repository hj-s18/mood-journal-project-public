from flask import Blueprint, render_template, request
from datetime import datetime, timedelta

# Diary 관련 Blueprint 생성 (url_prefix로 '/diary' 경로 설정)
diary_bp = Blueprint('diary', __name__, url_prefix="/diary")

# 년월에 맞는 날짜 리스트 생성 함수
def generate_dates(year, month):
    first_day = datetime(year, month, 1)
    if month == 12:
        last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    
    # 모든 날짜 리스트 생성 (정수형 일(day)만 반환)
    return [(first_day + timedelta(days=i)).day for i in range((last_day - first_day).days + 1)]

# 일기 페이지 라우트
@diary_bp.route('/')
def diary_home():
    # GET 요청에서 연도와 월을 가져옵니다.
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)

    # 월이 0 이하일 때: 이전 해의 12월로 이동
    if month < 1:
        year -= 1
        month = 12
    # 월이 13 이상일 때: 다음 해의 1월로 이동
    elif month > 12:
        year += 1
        month = 1

    # 해당 년월의 날짜 리스트 생성 (정수형 일(day)만 반환)
    days_in_month = generate_dates(year, month)

    return render_template('diary.html', year=year, month=month, days_in_month=days_in_month)

# 특정 날짜에 대한 일기 작성 페이지 라우트
@diary_bp.route('/write/<day>')
def write_diary(day):
    # 현재 연도와 월을 가져옵니다.
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)

    print(year)
    print(month)

    return render_template('write_diary.html', year=year, month=month, day=day)
