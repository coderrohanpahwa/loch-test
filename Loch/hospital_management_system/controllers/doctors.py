from flask import Flask
from flask_restful import reqparse,Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from hospital_management_system.helpers.rest_response import RestResponse
from hospital_management_system.services.doctors import DoctorService
from hospital_management_system.helpers.decorators import user_exists
class Doctor(Resource):
    @staticmethod
    def validate(data_dict):
        empty_keys = [key for key, value in data_dict.items() if not value]
        if empty_keys:
            return False,"Field/Fields "+",".join(empty_keys) +" are required"
        return True,"Validated"

    @jwt_required()
    @user_exists
    def post(self):
        current_user_id=get_jwt_identity()
        parser = reqparse.RequestParser(bundle_errors=True)

        parser.add_argument("name",type=str,required=True,help="name can't be blank")
        parser.add_argument("specialization",type=str,required=True,help="specialization can't be blank")
        parser.add_argument("email",type=str,required=True,help="email can't be blank")
        parser.add_argument("phone",type=str,required=True,help="phone can't be blank")
        
        args_dict=parser.parse_args().copy()
        if current_user_id:
            is_validated,err=self.validate(args_dict)
            if is_validated:
                return DoctorService().create_doctor(args_dict)
            else:
                return RestResponse(err=err).to_json(),400

        else:
            return RestResponse(err="User unauthorized").to_json()
    @jwt_required()
    @user_exists
    def get(self):
        return DoctorService().get_doctors()        


class PatientList(Resource):
    @jwt_required()
    @user_exists
    def get(self,doctor_id):
        return DoctorService().get_patient_list(doctor_id)

class BusyDoctor(Resource):
    @staticmethod
    def validate(data_dict):
        empty_keys = [key for key, value in data_dict.items() if not value]
        if empty_keys:
            return False,"Field/Fields "+",".join(empty_keys) +" are required"
        return True,"Validated"
    
    @jwt_required()
    @user_exists
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("date",type=str,required=True,help="date can't be blank")
        parser.add_argument("time",type=str,required=True,help="time can't be blank")

        args_dict=parser.parse_args().copy()
        is_validated,err=self.validate(args_dict)
        if is_validated:
            return DoctorService().get_busy_doctor(args_dict)
        else:
            return RestResponse(err=err).to_json(),400
