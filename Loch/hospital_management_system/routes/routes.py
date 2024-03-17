from hospital_management_system import api
from hospital_management_system.controllers.users import User
from hospital_management_system.controllers.patients import Patient,PatientMedicalHistory,PatientAction,AppointmentRecords
from hospital_management_system.controllers.doctors import Doctor,PatientList,BusyDoctor
from hospital_management_system.controllers.schedule import Appointment,AvailableSchedule
from hospital_management_system.controllers.departments import Department,DepartmentServices,AssignDepartment
from hospital_management_system.controllers.services import Service
from hospital_management_system.controllers.search import Search

api.add_resource(User,"/api/user")
api.add_resource(Patient,"/api/patient")
api.add_resource(PatientMedicalHistory,"/api/patient/history","/api/patient/history/<int:id>")
api.add_resource(PatientAction,"/api/patient/<int:id>")
api.add_resource(Appointment,"/api/appointment")

api.add_resource(Doctor,"/api/doctor")

api.add_resource(AvailableSchedule,"/api/doctor_availability/<int:doctor_id>")

api.add_resource(AppointmentRecords,"/api/<int:patient_id>/appointment_records")
api.add_resource(PatientList,"/api/doctor_patient_list/<int:doctor_id>")

api.add_resource(Department,"/api/department")

api.add_resource(AssignDepartment,'/api/assgin_department')

api.add_resource(Service,"/api/service")

api.add_resource(DepartmentServices,"/api/department_service/<int:department_id>")

api.add_resource(Search,"/api/search")
api.add_resource(BusyDoctor,"/api/busy_doctor")