from datetime import datetime, timedelta
from flask import session
from app.sql.db_connect import DBConnect

def check_achievements(user_id):
    attendance_streak = get_attendance_streak(user_id)
    if attendance_streak >= 7:
        award_achievement(user_id, '7리소스')
    if attendance_streak >= 15:
        award_achievement(user_id, '십오야')
    if attendance_streak >= 31:
        award_achievement(user_id, '배스킨라빈스')

    total_logins = get_total_logins(user_id)
    if total_logins >= 50:
        award_achievement(user_id, 'Total 50 Logins')
    if total_logins >= 100:
        award_achievement(user_id, 'Total 100 Logins')

    diary_streak = get_diary_streak(user_id)
    if diary_streak >= 7:
        award_achievement(user_id, 'Weekly Diary Streak')
    if diary_streak >= 30:
        award_achievement(user_id, 'Monthly Diary Streak')

    total_diaries = get_total_diaries(user_id)
    if total_diaries >= 10:
        award_achievement(user_id, '10 Diaries Written')
    if total_diaries >= 50:
        award_achievement(user_id, '50 Diaries Written')

    if has_written_all_emotions(user_id):
        award_achievement(user_id, 'Empathetic Soul')

def get_attendance_streak(user_id):
    db = DBConnect.get_db()
    cursor = db.cursor()
    today = datetime.today().date()
    cursor.execute("""
        SELECT date FROM attendance 
        WHERE user_id = %s AND date <= %s
        ORDER BY date DESC
    """, (user_id, today))
    
    streak_count = 0
    for record in cursor.fetchall():
        if record[0] == today - timedelta(days=streak_count):
            streak_count += 1
        else:
            break
    
    cursor.close()
    db.close()
    return streak_count

def get_total_logins(user_id):
    db = DBConnect.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE user_id = %s", (user_id,))
    total_logins = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return total_logins

def get_diary_streak(user_id):
    db = DBConnect.get_db()
    cursor = db.cursor()
    today = datetime.today().date()
    cursor.execute("""
        SELECT date FROM diaries 
        WHERE user_id = %s AND date <= %s
        ORDER BY date DESC
    """, (user_id, today))
    
    streak_count = 0
    for record in cursor.fetchall():
        if record[0] == today - timedelta(days=streak_count):
            streak_count += 1
        else:
            break
    
    cursor.close()
    db.close()
    return streak_count

def get_total_diaries(user_id):
    db = DBConnect.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM diaries WHERE user_id = %s", (user_id,))
    total_diaries = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return total_diaries

def has_written_all_emotions(user_id):
    db = DBConnect.get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT DISTINCT mood FROM diaries WHERE user_id = %s
    """, (user_id,))
    
    emotions_written = {row[0] for row in cursor.fetchall()}
    required_emotions = {1, 2, 3, 4}
    
    cursor.close()
    db.close()
    return required_emotions.issubset(emotions_written)

def award_achievement(user_id, achievement_name):
    db = DBConnect.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM achievements WHERE name = %s", (achievement_name,))
    achievement = cursor.fetchone()
    if achievement:
        achievement_id = achievement[0]
        cursor.execute("""
            SELECT * FROM user_achievements 
            WHERE user_id = %s AND achievement_id = %s AND is_achieved = TRUE
        """, (user_id, achievement_id))
        already_achieved = cursor.fetchone()
        if not already_achieved:
            cursor.execute("""
                INSERT INTO user_achievements (user_id, achievement_id, is_achieved, achieved_at) 
                VALUES (%s, %s, TRUE, NOW())
            """, (user_id, achievement_id))
            db.commit()
            session['new_achievement'] = achievement_name

    cursor.close()
    db.close()
