

from . import ParentModel
from hospital_management_system import db
class PatientModel(ParentModel):
    name=db.Column(db.String(255),nullable=False)
    age=db.Column(db.String(255),nullable=False)
    gender=db.Column(db.String(255))
    mobile=db.Column(db.String(20),nullable=False,unique=True)
    email=db.Column(db.String(100),nullable=False,unique=True)
    medical_history=db.relationship('PatientMedicalHistory',backref='patient',lazy=True)
    appointment_records=db.relationship('AppointmentRecords',backref='patient',lazy=True)

class PatientMedicalHistory(ParentModel):
    type=db.Column(db.String(255))
    description=db.Column(db.Text)
    patient_id=db.Column(db.ForeignKey('patient_model.id'), nullable=False)


class AppointmentRecords(ParentModel):
    appointment_start_time = db.Column(db.DateTime, nullable=False)
    purpose = db.Column(db.String(255))
    patient_id=db.Column(db.ForeignKey('patient_model.id'), nullable=False)
    doctor_id = db.Column(db.ForeignKey('doctor_model.id'), nullable=False)