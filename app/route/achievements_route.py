from flask import Blueprint, render_template, session, redirect, url_for
from app.sql.db_connect import DBConnect

achievements_bp = Blueprint('achievements', __name__, url_prefix="/achievements")

@achievements_bp.route('/')
def achievements_home():
    # 로그인한 사용자의 ID 가져오기
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    db = DBConnect.get_db()
    cursor = db.cursor()  # DictCursor 제거

    # 유저가 달성한 업적 가져오기
    cursor.execute("""
        SELECT a.name, a.description, ua.achieved_at
        FROM achievements a
        JOIN user_achievements ua ON a.id = ua.achievement_id
        WHERE ua.user_id = %s AND ua.is_achieved = TRUE
    """, (user_id,))
    achievements = cursor.fetchall()

    cursor.close()
    db.close()

    # 데이터를 템플릿에 전달
    return render_template('achievements.html', achievements=achievements)
