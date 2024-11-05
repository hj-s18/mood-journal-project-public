from flask import Blueprint, render_template, session, redirect, url_for
from app.sql.db_connect import DBConnect

achievements_bp = Blueprint('achievements', __name__, url_prefix="/achievements")

@achievements_bp.route('/')
def achievements_home():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    db = DBConnect.get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT a.name, a.description 
        FROM achievements a 
        JOIN user_achievements ua ON a.id = ua.achievement_id
        WHERE ua.user_id = %s AND ua.is_achieved = TRUE
    """, (user_id,))
    achievements = cursor.fetchall()

    new_achievement = session.pop('new_achievement', None)

    cursor.close()
    db.close()

    return render_template('achievements.html', achievements=achievements, new_achievement=new_achievement)
