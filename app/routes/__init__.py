from flask import Flask, Blueprint

def register_blueprints(app: Flask):
    from .auth_routes import auth_bp
    from .user_routes import user_bp
    from .investigation_routes import investigation_bp
    from .xray_binary_routes import xray_binary_bp
    from .xray_multi_routes import xray_multi_bp
    from .xray_to_text_routes import xray_to_text_bp

    # Used for JWT operations
    app.register_blueprint(auth_bp, url_prefix="/auth")

    app.register_blueprint(user_bp, url_prefix='/users')  # Prefixul '/users'
    app.register_blueprint(investigation_bp, url_prefix='/investigations')
    app.register_blueprint(xray_binary_bp, url_prefix='/xray_binary')
    app.register_blueprint(xray_multi_bp, url_prefix='/xray_multi')
    app.register_blueprint(xray_to_text_bp, url_prefix='/xray_to_text')


