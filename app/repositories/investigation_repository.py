from app.models import Investigation
from sqlalchemy.exc import SQLAlchemyError
from app import db

class InvestigationRepository:
    @staticmethod
    def get_all():
        return Investigation.query.all()

    @staticmethod
    def get_by_id(investigation_id):
        return Investigation.query.get(investigation_id)

    @staticmethod
    def create(investigation_data):
        try:
            investigation = Investigation(**investigation_data)
            db.session.add(investigation)
            db.session.commit()
            return investigation
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(investigation_id):
        try:
            investigation = Investigation.query.get(investigation_id)
            if investigation:
                db.session.delete(investigation)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
