# app/routes/xray_routes.py

from flask import Blueprint, request, jsonify
from flask import current_app as app

xray_bp = Blueprint('xray', __name__)

@xray_bp.route('/classify', methods=['POST'])
def classify():
    image_path = request.json.get('image_path')
    model_used = request.json.get('model_used')
    if not image_path:
        return jsonify({"error": "image_path is required"}), 400
    probabilities = app.xray_service.classify_image(image_path)
    return jsonify({"probabilities": probabilities.tolist()})

@xray_bp.route('/confusion_matrix', methods=['POST'])
def confusion_matrix():
    test_dir = request.json.get('test_dir')
    if not test_dir:
        return jsonify({"error": "test_dir is required"}), 400
    app.xray_service.confusion_matrixDraw(test_dir)
    return jsonify({"message": "Confusion matrix drawn"})