from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from flask import jsonify
from hospital_management_system.models.users import UsersModel
from hospital_management_system.helpers.rest_response import RestResponse
def user_exists(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user_exist = UsersModel.find_by_id(current_user_id)
        if not user_exist:
            return RestResponse(err="User with access token does not exist in database").to_json(), 404
        return fn(*args, **kwargs)
    return wrapper
