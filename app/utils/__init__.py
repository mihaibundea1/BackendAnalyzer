from flask_sqlalchemy import SQLAlchemy
from .database import LocalMySQL
from ..config import Config

# Crearea instanței Singleton pentru conexiunea DB
mysql_instance = LocalMySQL(host='localhost', port=3308, user='admin', password='admin_password', database='myapp')

# Inițializarea SQLAlchemy
db = SQLAlchemy()

def init_app(app):
    # Conectarea SQLAlchemy la aplicație
    app.config.from_object(Config)
    db.init_app(app)
