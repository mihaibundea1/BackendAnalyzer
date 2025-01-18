from flask import Flask
from .config import Config
from .routes import main_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Register Blueprints (routes)
    app.register_blueprint(main_routes)
    
    return app