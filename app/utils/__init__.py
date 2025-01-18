from .database import DatabaseManager

db_manager = DatabaseManager()

def init_app(app):
    db_manager.init_app(app)