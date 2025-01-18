from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum('patient', 'doctor', 'admin', name='user_type'), nullable=False)
    mfa_secret = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    investigations = db.relationship('Investigation', backref='user', lazy=True, foreign_keys='Investigation.user_id')
    doctor_investigations = db.relationship('Investigation', backref='doctor', lazy=True, foreign_keys='Investigation.doctor_id')
