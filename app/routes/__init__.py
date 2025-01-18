from flask import Blueprint, request, jsonify
from app.services.image_processing import process_image

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/upload', methods=['POST'])
def upload_xray():
    file = request.files['file']
    result = process_image(file)
    return jsonify(result)