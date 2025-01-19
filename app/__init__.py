from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from .routes import register_blueprints
from .utils import initialize_blackblaze

db = SQLAlchemy()  # Instanțiem SQLAlchemy aici

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)  # Inițializăm db cu aplicația

    # Initialization routes blueprints
    register_blueprints(app)

    # Intiailization of B2 Cloud
    app.b2_api = initialize_blackblaze(
        app.config["APPLICATION_KEY_ID"], 
        app.config["APPLICATION_KEY"]
        )
    return app
