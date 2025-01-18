from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from .routes import register_blueprints

db = SQLAlchemy()  # Instanțiem SQLAlchemy aici

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)  # Inițializăm db cu aplicația

    register_blueprints(app)
    return app
