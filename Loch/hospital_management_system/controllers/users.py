from flask import Flask
from flask_restful import reqparse,Resource
from hospital_management_system.services.users import UserService
from hospital_management_system.helpers.rest_response import RestResponse

class User(Resource):
    @staticmethod
    def validate(email,password):
        return email and password
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("email",type=str,required=True,help="Email is required")
        parser.add_argument("password",type=str,required=True,help="Password is required")
        args = parser.parse_args()
        is_validated=self.validate(args['email'],args['password'])
        if is_validated:
            return UserService().create_user(args['email'],args['password'])
        else:
            return RestResponse(err="Both email and password should have values").to_json(),400
    
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("email",type=str,required=True,help="Email is required")
        parser.add_argument("password",type=str,required=True,help="Password is required")
        args = parser.parse_args()
        is_validated=self.validate(args['email'],args['password'])
        if is_validated:
            return UserService().login_user(args['email'],args['password'])
        else:
            return RestResponse(err="Empty credentials passed").to_json(),400

