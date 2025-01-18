from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from app.routes import register_blueprints
from .utils import init_app as init_utils

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    init_utils(app)

    from app.routes import register_blueprints
    register_blueprints(app)
    
    with app.app_context():
        from app.models import User, Investigation  # Importă modelele aici
        db.create_all()  # Creează tabelele în baza de date, dacă nu există deja
    
    return app