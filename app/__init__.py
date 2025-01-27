from flask import Flask
from .config import Config
from .extensions import db  # Import from extensions
from .routes import register_blueprints
from .utils import initialize_blackblaze
from .services import create_xray_service

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)  # Initialize db with the app

    register_blueprints(app)

    app.b2_api = initialize_blackblaze(
        app.config["APPLICATION_KEY_ID"], 
        app.config["APPLICATION_KEY"]
    )

    # create_xray_service('app/models/pytorch_models/chest_xray_binary.pth', model_type='binary')

    @app.route('/test-model')
    def test_model():
        try:
            # Get the initialized model from your service
            model_service = create_xray_service('app/models/pytorch_models/chest_xray_binary.pth')
            
            # Test with a sample image (replace with your test image path)
            test_image = 'app/test.jpeg'
            probabilities = model_service.classify_image(test_image)
            
            return {
                'status': 'success',
                'predictions': probabilities.tolist()
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500
    
    return app