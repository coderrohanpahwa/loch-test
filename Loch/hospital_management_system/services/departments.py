from hospital_management_system.models.departments import DepartmentModel,ServicesModel
from hospital_management_system.models.doctors import DoctorModel
from sqlalchemy import exc
from hospital_management_system.helpers.rest_response import RestResponse
class DepartmentService:
    def create_department(self,data_dict):
        status,message,err,data,response_code=0,"","",{},201
        try:
            department=DepartmentModel(**data_dict)
            department.save()
            status=1
            data=department.to_json()
            message="Department has been created successfully"
        except exc.IntegrityError:
            err="Department Name already exists"
            response_code=400
        return RestResponse(err=err,message=message,status=status,data=data).to_json(),response_code

    def assign_department(self,data_dict):
        status,message,err,data,response_code=0,"","",{},201
        doctor=DoctorModel.find_by_id(data_dict['doctor_id'])
        department=DepartmentModel.find_by_id(data_dict['department_id'])      
        if doctor and department:
            if doctor.department_id:
                err="Doctor has already assigned to Department"
            else:
                doctor.department_id=department.id
                doctor.save()
                data=doctor.to_json()
                message="Doctor has successfully assigned to department"
                status=1
        else:
            err="Invalid doctor_id or department_id entered"
            response_code=400
        return RestResponse(err=err,message=message,status=status,data=data).to_json(),response_code

    def get_department_service(self,department_id):
        status,message,err,data,response_code=0,"","",{},200
        department=DepartmentModel.find_by_id(department_id)      
        if department: 
            data=[i.to_json() for i in ServicesModel.find_by("department_id",department_id)]
            message="Services have been fetched successfully"
            status=1
        else:
            err=f"Department with department_id as {department_id} does not exist"
            response_code=404
        return RestResponse(err=err,message=message,status=status,data=data).to_json(),response_code
