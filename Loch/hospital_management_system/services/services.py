from hospital_management_system.helpers.rest_response import RestResponse
from hospital_management_system.models.departments import ServicesModel,DepartmentModel
from sqlalchemy import exc
class Services:
    def create_service(self,data_dict):
        status,message,err,data,response_code=0,"","",{},201
        department=DepartmentModel.find_by_id(data_dict['department_id'])
        if department:
            try:
                service=ServicesModel(**data_dict)
                service.save()
                message="Serivce has been made successfully"
                status=1
                data=service.to_json()
            except exc.IntegrityError:
                response_code=400
                err=f"Service with name {data_dict['name']} already exist"
        else:
            err=f"Department having department_id as {data_dict['department_id']} does not exist "
        return RestResponse(err=err,message=message,status=status,data=data).to_json(),response_code

