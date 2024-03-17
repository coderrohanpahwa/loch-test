from flask_restful import reqparse,Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from hospital_management_system.helpers.decorators import user_exists
from hospital_management_system.helpers.enum_handler import SearchModelNameEnum
from hospital_management_system.services.search import SearchService
from hospital_management_system.helpers.rest_response import RestResponse
from hospital_management_system.helpers.enum_handler import SearchModelNameEnum,SearchTypeEnum

class Search(Resource):
    @staticmethod
    def check_model_field(model_name,field_name):
        field_mapping={SearchModelNameEnum.PATIENTS.value:["name","gender","mobile","email"],\
                       SearchModelNameEnum.DOCTORS.value:["name","specialization","email","phone"],
                       SearchModelNameEnum.DEPARTMENTS.value:["name"]}
        if field_name not in field_mapping[model_name]:    
            return False,f"Field can take value as {','.join(field_mapping[model_name])}"
        return True,"Validated"


    @staticmethod
    def validate(data_dict):
        if data_dict["page_number"]<1:
            return False,"page_number should be greater than 0"
        if data_dict["limit"]<1:
            return False,"limit should be greater than 0"
        empty_keys = [key for key, value in data_dict.items() if not value]
        search_model_li=[i.value for i in SearchModelNameEnum]

        if data_dict['search_on'] not in search_model_li:
            return False,f"search_on can take values as {','.join(search_model_li)}"

        search_type_li=[i.value for i in SearchTypeEnum]
        if data_dict['search_type'] not in search_type_li:
            return False,f"search_type can take values as {','.join(search_type_li)}"


        if empty_keys:
            return False,"Field/Fields "+",".join(empty_keys) +" are required"
        return True,"Validated"

    @jwt_required()
    @user_exists
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("search_on",required=True,type=str,help="search_on can't be blank")
        parser.add_argument("field",required=True,type=str,help="field can't be blank")
        parser.add_argument("page_number",type=int,help="page_number can't be blank",default=1)
        parser.add_argument("limit",type=int,help="limit can't be blank",default=10)
        parser.add_argument("search_type",type=str,help="search_type can't be blank")
        parser.add_argument("query",type=str,help="query can't be blank")
        args_dict=parser.parse_args().copy()
        is_validated,err=self.validate(args_dict)
        if is_validated:
            status,err=self.check_model_field(args_dict['search_on'],args_dict['field'])
            if status:
                return SearchService().search_based_on_criteria(args_dict)
            else:
                return RestResponse(err=err).to_json(),400
        else:
            return RestResponse(err=err).to_json(),400
