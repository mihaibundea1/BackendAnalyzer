from flask import Flask
from .config import Config
from .extensions import db, jwt # Import from extensions
from .routes import register_blueprints
from .utils import initialize_blackblaze
from .services import register_services

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize JWT
    jwt.init_app(app)

    # Registering the pytorch models
    register_services(app)

    # Register the routes blueprints
    register_blueprints(app)

    app.b2_api = initialize_blackblaze(
        app.config["APPLICATION_KEY_ID"], 
        app.config["APPLICATION_KEY"]
    )

    @app.route('/test-model')
    def test_model():
        try:
            # Correct import statement
            from app.services.xray_service_binary import xray_binary_service
            
            # Test with a sample image (replace with your test image path)
            test_image = 'app/pneumo_emphizem.png'
            probabilities = xray_binary_service.predict_image(test_image)
            
            return {
                'status': 'success',
                'predictions': probabilities
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500
    
    @app.route('/test-model-multi')
    def test_model_multi():
        try:
            # Correct import statement
            from app.services.xray_service_multi import xray_multi_service
            
            # Test with a sample image (replace with your test image path)
            test_image = 'app/pneumo_emphizem.png'
            probabilities = xray_multi_service.predict_image(test_image)
            
            return {
                'status': 'success',
                'predictions': probabilities
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500


    return app