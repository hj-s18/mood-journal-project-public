from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Diary(db.Model):
    __tablename__ = 'diaries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mood = db.Column(db.Integer, nullable=False)
    body = db.Column(db.Text, nullable=False)
    file_urls = db.Column(db.Text)