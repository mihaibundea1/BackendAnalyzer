from app.models import User
from app import db
import pyotp

class UserService:
    @staticmethod
    def get_all_users():
        """Returnează toți utilizatorii."""
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        """Returnează un utilizator după ID."""
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_user_by_email(email):
        """Returnează un utilizator după email."""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_user(data):
        """Creează un utilizator nou și generează un secret MFA dacă nu este furnizat."""
        mfa_secret = pyotp.random_base32()

        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            type=data.get('type'),
            mfa_secret=mfa_secret
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_user(user_id, data):
        """Actualizează informațiile unui utilizator."""
        user = User.query.filter_by(id=user_id).first()
        if user:
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.password_hash = data.get('password_hash', user.password_hash)
            user.type = data.get('type', user.type)
            user.mfa_secret = data.get('mfa_secret', user.mfa_secret)
            db.session.commit()
            return user
        return None

    @staticmethod
    def delete_user(user_id):
        """Șterge un utilizator."""
        user = User.query.filter_by(id=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
