from flask import Flask, Blueprint

from .user_routes import user_routes
from .investigation_routes import investigation_routes

def register_blueprints(app: Flask):
    app.register_blueprint(user_routes, url_prefix='/users')  # Prefixul '/users'
    app.register_blueprint(investigation_routes, url_prefix='/investigation')
