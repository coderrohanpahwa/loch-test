from flask import Flask
from flask_restful import Api
import json
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from hospital_management_system.helpers.rest_response import RestResponse
from flask_jwt_extended import JWTManager

class CustomApi(Api):
    def handle_error(self, e):
        response = super().handle_error(e)
        try:
            err_resp=RestResponse(err=json.loads(response.get_data())["message"]).to_json()
            response.set_data(json.dumps(err_resp))
        except: pass
    
        return response
        
     


app = Flask(__name__)

app.config.from_object('config')
jwt = JWTManager(app)
api = CustomApi(app)
db = SQLAlchemy(app)

import hospital_management_system.routes.routes

@app.before_request
def create_tables():
    db.create_all()