from flask import Blueprint, request, jsonify
from app.services.investigation_service import InvestigationService

investigation_routes = Blueprint('investigation_routes', __name__)

@investigation_routes.route('/investigations', methods=['GET'])
def get_investigations():
    investigations = InvestigationService.get_all_investigations()
    return jsonify([investigation.serialize() for investigation in investigations])

@investigation_routes.route('/investigation/<int:investigation_id>', methods=['GET'])
def get_investigation(investigation_id):
    investigation = InvestigationService.get_investigation_details(investigation_id)
    if investigation:
        return jsonify(investigation.serialize())
    return jsonify({'error': 'Investigation not found'}), 404

@investigation_routes.route('/investigation', methods=['POST'])
def create_investigation():
    data = request.json
    new_investigation = InvestigationService.create_investigation(data)
    return jsonify(new_investigation.serialize()), 201

@investigation_routes.route('/investigation/<int:investigation_id>', methods=['DELETE'])
def delete_investigation(investigation_id):
    success = InvestigationService.delete_investigation(investigation_id)
    if success:
        return jsonify({'message': 'Investigation deleted successfully'}), 200
    return jsonify({'error': 'Investigation not found'}), 404
