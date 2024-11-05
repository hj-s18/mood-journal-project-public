from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from app.sql.db_connect import DBConnect
import pymysql
from app.sql.achievements_db import check_achievements

attendance_bp = Blueprint('attendance', __name__, url_prefix="/attendance")

@attendance_bp.route('/')
def attendance_home():
    user_id = session.get('user_id', 1)
    week_days = get_week_dates(user_id)
    all_attended = all(day['attended'] for day in week_days)
    today_date = datetime.today().date()
    today_attendance = any(day['date'] == today_date.strftime('%Y-%m-%d') and day['attended'] for day in week_days)
    return render_template('attendance.html', week_days=week_days, all_attended=all_attended, today_attendance=today_attendance)

@attendance_bp.route('/mark', methods=['POST'])
def mark_attendance():
    user_id = session.get('user_id', 1)
    attendance_date = datetime.today().date()

    try:
        db = DBConnect.get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM attendance WHERE user_id = %s AND date = %s", (user_id, attendance_date))
        attendance = cursor.fetchone()
        if not attendance:
            cursor.execute("INSERT INTO attendance (user_id, date) VALUES (%s, %s)", (user_id, attendance_date))
            db.commit()
        cursor.close()
    except Exception as e:
        print("DB Error:", e)
    finally:
        db.close()

    check_achievements(user_id)
    return redirect(url_for('attendance.attendance_home'))

def get_week_dates(user_id=None):
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    week_days = []
    
    try:
        db = DBConnect.get_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        for i in range(7):
            current_day = start_of_week + timedelta(days=i)
            if user_id:
                cursor.execute("SELECT * FROM attendance WHERE user_id = %s AND date = %s", (user_id, current_day.date()))
                attendance = cursor.fetchone()
            else:
                attendance = None

            week_days.append({
                'weekday': current_day.strftime('%A'),
                'date': current_day.strftime('%Y-%m-%d'),
                'attended': bool(attendance)
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
