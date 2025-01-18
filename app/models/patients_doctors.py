from datetime import datetime
from app import db

class PatientsDoctors(db.Model):
    __tablename__ = 'patients_doctors'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    patient = db.relationship('User', foreign_keys=[patient_id])
    doctor = db.relationship('User', foreign_keys=[doctor_id])
        
    def serialize(self):
        """Transformă obiectul User într-un dict JSON serializabil."""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'patient': self.patient,
            'doctor': self.doctor
        }