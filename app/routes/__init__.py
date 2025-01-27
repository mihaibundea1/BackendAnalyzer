from flask import Flask, Blueprint

def register_blueprints(app: Flask):
    from .user_routes import user_routes
    from .investigation_routes import investigation_routes
    from .xray_routes import xray_bp

    app.register_blueprint(user_routes, url_prefix='/users')  # Prefixul '/users'
    app.register_blueprint(investigation_routes, url_prefix='/investigations')
    app.register_blueprint(xray_bp, url_prefix='/xray')
