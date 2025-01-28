from flask import Blueprint, jsonify, request
from app.services.xray_service_binary import xray_binary_service
from app.utils.file_utils import save_temp_file

xray_binary_bp = Blueprint('xray_binary', __name__)

@xray_binary_bp.route('/predict-binary', methods=['POST'])
def predict_binary():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    temp_path = save_temp_file(file)
    
    try:
        predictions = xray_binary_service.predict_image(temp_path)
        os.remove(temp_path)
        return jsonify({
            'predictions': predictions,
            'model_type': 'binary'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500