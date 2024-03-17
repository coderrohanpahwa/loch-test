from hospital_management_system.models.departments import DepartmentModel
from hospital_management_system.models.doctors import DoctorModel
from hospital_management_system.models.patients import PatientModel
from hospital_management_system.helpers.enum_handler import SearchTypeEnum,SearchModelNameEnum
from hospital_management_system.helpers.rest_response import RestResponse

class SearchService:
    def search_based_on_criteria(self,dict_data):
        status,message,err,data,response_code=0,"","",{},200
        if dict_data['search_on'] ==SearchModelNameEnum.DOCTORS.value:
            model=DoctorModel
        elif dict_data['search_on']==SearchModelNameEnum.PATIENTS.value:
            model=PatientModel
        elif dict_data["search_on"]==SearchModelNameEnum.DEPARTMENTS.value:
            model=DepartmentModel

        if SearchTypeEnum.PARTIAL.value==dict_data['search_type']:
            db_query=getattr(model,dict_data['field']).like(f'%{dict_data["query"]}%')
        elif SearchTypeEnum.EXACT.value==dict_data['search_type']:
            db_query=getattr(model,dict_data['field']).like(f'{dict_data["query"]}') 
        elif SearchTypeEnum.STARTS_WITH.value==dict_data["search_type"]:
            db_query=getattr(model,dict_data['field']).like(f'{dict_data["query"]}%')

        try:
            db_result=model.query.filter(db_query).paginate(page=dict_data['page_number'],per_page=dict_data['limit'])
            data['items']=[i.to_json() for i in db_result.items]
            data['total']=db_result.total
            data['next_page']=db_result.next_num
            data['curr_page'] =db_result.page 
        except Exception as e:
            data['items']=[]
            data['total']=model.query.filter(db_query).count()
            data['page'] =dict_data['page_number']
            data['next_page']=None
        status=1
        message="Requested data has been fetched successfully"
        return RestResponse(err=err,message=message,status=status,data=data).to_json(),response_code
