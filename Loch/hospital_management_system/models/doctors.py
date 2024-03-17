from . import ParentModel
from hospital_management_system import db
class DoctorModel(ParentModel):
    name=db.Column(db.String(255),nullable=False)
    specialization=db.Column(db.String(255),nullable=False)
    email=db.Column(db.String(255),nullable=False,unique=True)
    phone=db.Column(db.String(100),nullable=False,unique=True)

    department_id = db.Column(db.ForeignKey('department_model.id'))
