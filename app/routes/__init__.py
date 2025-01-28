from flask import Flask, Blueprint

def register_blueprints(app: Flask):
    from .user_routes import user_routes
    from .investigation_routes import investigation_routes
    from .xray_binary_routes import xray_binary_bp
    from .xray_multi_routes import xray_multi_bp

    app.register_blueprint(user_routes, url_prefix='/users')  # Prefixul '/users'
    app.register_blueprint(investigation_routes, url_prefix='/investigations')
    app.register_blueprint(xray_binary_bp, url_prefix='/xray_binary')
    app.register_blueprint(xray_multi_bp, url_prefix='/xray_multi')
