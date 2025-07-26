from extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    exercises = db.relationship('ExerciseLog', backref='user', lazy=True)
    calories = db.relationship('CalorieLog', backref='user', lazy=True)
    water_logs = db.relationship('WaterLog', backref='user', lazy=True)
    measurements = db.relationship('BodyMeasurement', backref='user', lazy=True)
    goals = db.relationship('Goal', backref='user', lazy=True)
    plans = db.relationship('WorkoutPlan', backref='user', lazy=True)

    def set_password(self, pw):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, pw)

class ExerciseLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Float)
    duration = db.Column(db.Float)
    calories = db.Column(db.Float)
    video_url = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class CalorieLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calories = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class WaterLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount_ml = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class BodyMeasurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float)
    body_fat = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    target_date = db.Column(db.Date)
    achieved = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class WorkoutPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    schedule = db.Column(db.Text)  # JSON schedule
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
