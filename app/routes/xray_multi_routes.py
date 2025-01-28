from flask import Blueprint, jsonify, request
from app.services.xray_service_multi import xray_multi_service
from app.utils.file_utils import save_temp_file
import os

xray_multi_bp = Blueprint('xray_multi', __name__)

@xray_multi_bp.route('/predict-multi', methods=['POST'])
def predict_multi():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    temp_path = save_temp_file(file)
    
    try:
        predictions = xray_multi_service.predict_image(temp_path)
        os.remove(temp_path)
        return jsonify({
            'predictions': predictions,
            'model_type': 'multi-class'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500