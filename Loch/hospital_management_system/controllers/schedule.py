from flask_restful import reqparse,Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from hospital_management_system.helpers.decorators import user_exists
from hospital_management_system.services.schedule import Schedule
from hospital_management_system.helpers.rest_response import RestResponse
from hospital_management_system.helpers.enum_handler import AppointmentBookingEnum

class Appointment(Resource):
    @staticmethod
    def validate(data):
        empty_keys = [key for key, value in data.items() if not value]
        if empty_keys:
            return False,"Field/Fields "+",".join(empty_keys) +" are required"
        appointment_booking=[i.value for i in AppointmentBookingEnum]
        if data["booking_type"] not in appointment_booking:
            return False,f"booking_type can only take values as {','.join(appointment_booking)}"
        return True,""

    @jwt_required()
    @user_exists
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("patient_id",required=True,type=int,help="patient_id can't be blank")
        parser.add_argument("doctor_id",required=True,type=int,help="doctor_id can't be blank")
        parser.add_argument("purpose",required=True,type=str,help="purpose can't be blank")
        parser.add_argument("appointment_start_time",required=True,type=str,help="appointment_start_time can't be blank")
        parser.add_argument("booking_type",required=True,type=str,help=f"booking_type can't be blank ") 

        args=parser.parse_args().copy()
        is_validated,err=self.validate(args)
        if is_validated:
            return Schedule().create_appointment(args)
        else:
            return RestResponse(err=err).to_json(),400
        


class AvailableSchedule(Resource):
    def get(self,doctor_id):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("date",required=True,help="Date can't be blank")
        # TODO:Rohan Have to give list of Dates
        args=parser.parse_args()
        return Schedule().get_schedule(doctor_id,args["date"])

    