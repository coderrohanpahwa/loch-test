from hospital_management_system.models.users import UsersModel
from hospital_management_system.helpers.rest_response import RestResponse
from flask_jwt_extended import create_access_token
from sqlalchemy import exc
from datetime import datetime

class UserService:
    def create_user(self,email,password):
        status,message,err,data,response_code=0,"","",{},201
        password = UsersModel.generate_password_hash(password)
        user=UsersModel(email=email,password=password)       
        try:
            user.generate_password_hash(password=password)
            
            user.last_login=datetime.utcnow()
            user.save()
            user.access_token = create_access_token(identity=str(user.id), expires_delta=False)
            user.save()
            message="User has been successfully created"
            status=1
            data=user.to_json()

        except exc.IntegrityError:
            response_code=400
            err="Username already exist"

        return RestResponse(err=err,message=message,status=status,data=data).to_json(),response_code
    
    def login_user(self,email,password):
        status,message,err,data,response_code=0,"","",{},201
        user=UsersModel.find_by_email(email)
        if user:
            if UsersModel.verify_hash(password, user.password):
                user.last_login = datetime.utcnow()
                user.save()
                data=user.to_json()
                data=data
                status=1
                message="User has been login successfully"
            else:
                response_code=400
                err="Email and password combination does not match"
        else:
            response_code=404
            err="Email does not exist"
        return RestResponse(err=err,message=message,status=status,data=data).to_json(),response_code