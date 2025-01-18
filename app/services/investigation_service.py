from app.repositories.investigation_repository import InvestigationRepository

class InvestigationService:
    @staticmethod
    def get_all_investigations():
        return InvestigationRepository.get_all()

    @staticmethod
    def get_investigation_details(investigation_id):
        return InvestigationRepository.get_by_id(investigation_id)

    @staticmethod
    def create_investigation(data):
        # Posibilă logică suplimentară înainte de a salva
        return InvestigationRepository.create(data)

    @staticmethod
    def delete_investigation(investigation_id):
        return InvestigationRepository.delete(investigation_id)
