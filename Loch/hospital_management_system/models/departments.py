from . import ParentModel
from hospital_management_system import db
class DepartmentModel(ParentModel):
    name=db.Column(db.String(255),nullable=False,unique=True)
    description=db.Column(db.String(255),nullable=False)
    doctors=db.relationship('DoctorModel',backref='deptartment',lazy=True)
    services=db.relationship('ServicesModel',backref='deptartment',lazy=True)


class ServicesModel(ParentModel):
    name=db.Column(db.String(255),nullable=False,unique=True)
    description=db.Column(db.String(255),nullable=False)
    department_id = db.Column(db.ForeignKey('department_model.id'), nullable=False)

