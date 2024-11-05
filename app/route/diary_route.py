from flask import *
from datetime import datetime, timedelta
from ..sql.diary_db import DiaryDAO

diary_bp = Blueprint('diary', __name__, url_prefix="/diary")

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
    # if "user_id" not in session:
    #     return redirect(url_for())
    # else:
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

        # 테스트
        user_id = 1

        diaries = DiaryDAO().get_list_diaries_with_date(user_id, year, month)       
        return render_template('diary.html', year=year, month=month, days_in_month=days_in_month, diaries=diaries)

# 특정 날짜에 대한 일기 작성 페이지 라우트
@diary_bp.route('/write/<int:day>', methods=["GET", "POST"])
def write_diary(day):
    # if "user_id" not in session:
    #     # return redirect(url_for())
    #     return
    # else:
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', datetime.now().month, type=int)

        diary_id = request.args.get('diary_id', None)
        _method = request.form.get('_method', 'ㅇㅇ')
        print(_method)


        # 권한 추가
        if request.method == 'GET':
            # formatted_date = datetime(year, month, int(day)).strftime('%Y-%m-%d')

            if diary_id:
                 diary = DiaryDAO().get_diary(diary_id)
            else:
                 diary = None

            return render_template('write_diary.html', year=year, month=month, day=day, diary=diary)

        elif _method == "upsert":
            user_id = 1
            # user_id = session['user_id']
            mood = request.form['mood']
            body = request.form['body']
            # file_urls = request.form['file_urls']
            formatted_date = datetime(year, month, int(day)).strftime('%Y-%m-%d')
            
            DiaryDAO().upsert_diary(user_id, mood, body, formatted_date, diary_id)

            # flash('일기가 성공적으로 저장되었습니다!', 'success')
            return redirect(url_for('diary.diary_home', year=year, month=month))

        elif _method == "delete":
            user_id = 1

            DiaryDAO().delete_diary(diary_id)
            return redirect(url_for('diary.diary_home', year=year, month=month))
        
