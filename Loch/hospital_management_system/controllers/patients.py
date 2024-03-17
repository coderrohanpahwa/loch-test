from flask import Flask
from flask_restful import reqparse,Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from hospital_management_system.helpers.rest_response import RestResponse
from hospital_management_system.services.patients import PatientService
from hospital_management_system.helpers.enum_handler import GenderEnum,MedicalHistoryEnum
from hospital_management_system.helpers.decorators import user_exists

class Patient(Resource):
    
    @staticmethod
    def validate(data):
        empty_keys = [key for key, value in data.items() if not value]
        if empty_keys:
            return False,"Field/Fields "+",".join(empty_keys) +" are required"
        gender_list=[i.value for i in GenderEnum]
        if data['gender'].lower() not in [i.value for i in GenderEnum]:
            return False,f"Gender can take values as {','.join(gender_list)}"
        
        return True,""

    @jwt_required()
    @user_exists
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', type=str, help='Name can not be blank', required=True)
        parser.add_argument('age', type=int, help='Age can not be blank and it should be entered integer', required=True)
        parser.add_argument('gender', type=str, help='Gender can not be blank', required=True)
        parser.add_argument('mobile', type=str, help='Mobile can not be blank', required=True)
        parser.add_argument('email', type=str, help='Email can not be blank', required=True)
        args_dict=parser.parse_args().copy()
        current_user_id=get_jwt_identity()
        is_validated,err_message=self.validate(args_dict)
        if is_validated:
            if current_user_id:
                return PatientService().create_patient(args_dict)
            else:
                return RestResponse(err="User Unauthorized").to_json(),401
        else:
            return RestResponse(err=err_message).to_json(),400
    @jwt_required()
    @user_exists
    def get(self):
        current_user_id=get_jwt_identity()
        if current_user_id:
            return PatientService().get_patients()
        else:
            return RestResponse(err="User Unauthorized").to_json(),400
        
class PatientAction(Resource):
    @jwt_required()
    @user_exists
    def get(self,id):
        current_user_id=get_jwt_identity()
        if current_user_id:
            return PatientService().get_patient_record(id)
        else:
            return RestResponse(err="User Unauthorized").to_json(),400
    
    @jwt_required()
    @user_exists
    def put(self,id):
        current_user_id=get_jwt_identity()
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', type=str, help='Name can not be blank', required=True)
        parser.add_argument('age', type=int, help='Age can not be blank and it should be entered integer', required=True)
        parser.add_argument('gender', type=str, help='Gender can not be blank', required=True)
        parser.add_argument('mobile', type=str, help='Mobile can not be blank', required=True)
        parser.add_argument('email', type=str, help='Email can not be blank', required=True)
        args_dict=parser.parse_args().copy()
        is_validated,err_message=Patient.validate(args_dict)
        if current_user_id:
            if is_validated:
                return PatientService().update_patient_record(id,args_dict)
            else:
                return RestResponse(err=err_message).to_json(),400
        else:
            return RestResponse(err="User unauthorized").to_json(),400


class PatientMedicalHistory(Resource):
    @staticmethod
    def validate(data):
        empty_keys = [key for key, value in data.items() if not value]
        if empty_keys:
            return False,"Field/Fields "+",".join(empty_keys) +" are required"
        medical_history_list=[i.value for i in MedicalHistoryEnum]
        if data['type'].lower() not in [i.value for i in MedicalHistoryEnum]:
            return False,f"type can take values as {','.join(medical_history_list)}"
        
        return True,""


    @jwt_required()
    @user_exists
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('type',type=str,help=f"Type must be one of the following { [i.value for i in MedicalHistoryEnum]}",)
        parser.add_argument('description',type=str,help="Description can't be blank",required=True)
        parser.add_argument('patient_id',type=int,help="Patient Id can't be blank and it should be entered integer",required=True)
        args_dict=parser.parse_args().copy()
        current_user_id=get_jwt_identity()
        is_validated,err_message=self.validate(args_dict)
        if is_validated:
            if current_user_id:
                return PatientService().create_patient_record(args_dict)
            else:
                return RestResponse(err="User Unauthorized").to_json(),401
        else:
            return RestResponse(err=err_message).to_json(),400
    @jwt_required()
    @user_exists
    def get(self,id):
        current_user_id=get_jwt_identity()
        if current_user_id:
            return PatientService().get_patient_medical_record(id)
        else:
            return RestResponse(err="User Unauthorized").to_json(),401
    
    @jwt_required()
    @user_exists
    def put(self,id):
        parser = reqparse.RequestParser(bundle_errors=True)
        current_user_id=get_jwt_identity()
        parser.add_argument('type',type=str,help=f"Type must be one of the following { [i.value for i in MedicalHistoryEnum]}",)
        parser.add_argument('description',type=str,help="Description can't be blank",required=True)
        parser.add_argument('patient_id',type=int,help="Patient Id can't be blank and it should be entered integer",required=True)
        args_dict=parser.parse_args().copy()
        is_validated,err_message=self.validate(args_dict)
        if is_validated:
            if current_user_id:
                return PatientService().update_patient_medical_record(id,args_dict)
            else:
                return RestResponse(err="User Unauthorized").to_json(),401
        else:
            return RestResponse(err=err_message).to_json(),400

class AppointmentRecords(Resource):
    @jwt_required()
    @user_exists
    def get(self,patient_id):
        return PatientService().get_patient_appointment_record(patient_id)