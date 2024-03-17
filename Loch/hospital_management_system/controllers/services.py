from flask_restful import reqparse,Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from hospital_management_system.helpers.decorators import user_exists,jwt_required
from hospital_management_system.services.services import Services
from hospital_management_system.helpers.rest_response import RestResponse

class Service(Resource):
    @staticmethod
    def validate(data_dict):
        empty_keys = [key for key, value in data_dict.items() if not value]
        if empty_keys:
            return False,"Field/Fields "+",".join(empty_keys) +" are required"
        return True,"Validated"

    @jwt_required()
    @user_exists
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("name",type=str,required=True,help="name can't be blank")
        parser.add_argument("description",type=str,required=True,help="description can't be blank")
        parser.add_argument("department_id",type=str,required=True,help="department_id can't be blank")

        args_dict=parser.parse_args().copy()
        is_validated,err=self.validate(args_dict)
        if is_validated:
            return Services().create_service(args_dict)
        else:
            return RestResponse(err=err).to_json(),400