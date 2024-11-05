from datetime import datetime, timedelta
import pymysql
from app.sql.db_connect import DBConnect

def check_achievements(user_id):
    today = datetime.today().date()

    # 로그인 연속 출석 확인
    attendance_streak = get_attendance_streak(user_id, today)
    if attendance_streak == 7:
        award_achievement(user_id, 'Weekly Login Streak')
    elif attendance_streak == 30:
        award_achievement(user_id, 'Monthly Login Streak')

    # 일기 작성 연속 기록 확인
    diary_streak = get_diary_streak(user_id, today)
    if diary_streak == 7:
        award_achievement(user_id, 'Weekly Diary Streak')
    elif diary_streak == 30:
        award_achievement(user_id, 'Monthly Diary Streak')

def get_attendance_streak(user_id, end_date):
    db = DBConnect.get_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # 연속 출석 일수를 계산하는 쿼리
    cursor.execute("""
        SELECT COUNT(*) AS streak_count
        FROM (
            SELECT date, 
                   @streak := IF(@prev_date = DATE_SUB(date, INTERVAL 1 DAY), @streak + 1, 1) AS streak,
                   @prev_date := date
            FROM attendance, (SELECT @streak := 0, @prev_date := NULL) AS vars
            WHERE user_id = %s AND date <= %s
            ORDER BY date DESC
        ) AS subquery
        WHERE streak = @streak
    """, (user_id, end_date))
    
    result = cursor.fetchone()
    streak_count = result['streak_count'] if result else 0

    cursor.close()
    db.close()
    return streak_count

def get_diary_streak(user_id, end_date):
    db = DBConnect.get_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # 일기 작성 연속 일수를 계산하는 쿼리
    cursor.execute("""
        SELECT COUNT(*) AS streak_count
        FROM (
            SELECT date, 
                   @streak := IF(@prev_date = DATE_SUB(date, INTERVAL 1 DAY), @streak + 1, 1) AS streak,
                   @prev_date := date
            FROM diaries, (SELECT @streak := 0, @prev_date := NULL) AS vars
            WHERE user_id = %s AND date <= %s
            ORDER BY date DESC
        ) AS subquery
        WHERE streak = @streak
    """, (user_id, end_date))
    
    result = cursor.fetchone()
    streak_count = result['streak_count'] if result else 0

    cursor.close()
    db.close()
    return streak_count

def award_achievement(user_id, achievement_name):
    db = DBConnect.get_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # 업적 ID 가져오기
    cursor.execute("SELECT id FROM achievements WHERE name = %s", (achievement_name,))
    achievement = cursor.fetchone()
    if not achievement:
        print(f"Achievement '{achievement_name}' not found in database.")
        return

    achievement_id = achievement['id']

    # 사용자가 이미 이 업적을 달성했는지 확인
    cursor.execute("""
        SELECT * FROM user_achievements 
        WHERE user_id = %s AND achievement_id = %s AND is_achieved = TRUE
    """, (user_id, achievement_id))
    already_achieved = cursor.fetchone()

    if not already_achieved:
        cursor.execute("""
            INSERT INTO user_achievements (user_id, achievement_id, achieved_date, is_achieved) 
            VALUES (%s, %s, %s, TRUE)
        """, (user_id, achievement_id, datetime.today().date()))
        db.commit()
        print(f"Achievement '{achievement_name}' awarded to user {user_id}.")
    else:
        print(f"User {user_id} already has achievement '{achievement_name}'.")

    cursor.close()
    db.close()
