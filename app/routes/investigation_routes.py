from flask import Blueprint, request, jsonify
from app.services.investigation_service import InvestigationService

investigation_bp = Blueprint('/investigations', __name__)

@investigation_bp.route('/', methods=['GET'])
def get_investigations():
    investigations = InvestigationService.get_all_investigations()
    if investigations:
        return jsonify([investigation.serialize() for investigation in investigations])
    return jsonify({'error': 'No investigations found'}), 404

@investigation_bp.route('/<int:investigation_id>', methods=['GET'])
def get_investigation(investigation_id):
    investigation = InvestigationService.get_investigation_details(investigation_id)
    if investigation is not None:
        return jsonify(investigation.serialize())
    return jsonify({'error': f'Investigation with ID {investigation_id} not found'}), 404

@investigation_bp.route('/', methods=['POST'])
def create_investigation():
    files = request.files
    form = request.form
    new_investigation = InvestigationService.create_investigation(files=files, form=form)

    if new_investigation:
        return jsonify(new_investigation.serialize()), 201
    else:
        return jsonify({'error': 'Failed to create investigation'}), 500

@investigation_bp.route('/<int:investigation_id>', methods=['DELETE'])
def delete_investigation(investigation_id):
    success = InvestigationService.delete_investigation(investigation_id)
    if success:
        return jsonify({'message': 'Investigation deleted successfully'}), 200
    return jsonify({'error': f'Investigation with ID {investigation_id} not found for deletion'}), 404
