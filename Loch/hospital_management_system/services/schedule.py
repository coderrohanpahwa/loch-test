# from datetimerange import DateTimeRange
from datetime import datetime, timedelta,time,date
from hospital_management_system import app,db
from hospital_management_system.helpers.rest_response import RestResponse
from hospital_management_system.models.doctors import DoctorModel
from hospital_management_system.models.patients import PatientModel,AppointmentRecords
from hospital_management_system.helpers.enum_handler import AppointmentBookingEnum
class Schedule:
    @staticmethod
    def generate_slots(start_time, end_time, slot_book_time):
        slots = []
        current_time = start_time
        while current_time < end_time:
            slots.append(str(current_time))
            current_time=datetime.combine(date.today(), current_time)
            current_time += timedelta(minutes=slot_book_time)
            current_time=current_time.time()

        return slots

    def get_schedule(self,doctor_id,date):
        status,message,err,data,response_code=0,"","",{},200
        if DoctorModel.find_by_id(doctor_id):
            date_obj = datetime.strptime(date, "%d/%m/%Y").date()
            today_date = datetime.today().date()
            if date_obj==today_date:
                start_time = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
                start_time=start_time.time()
                start_time=max(start_time,datetime.strptime(app.config["SHIFT_START_TIME"], "%H:%M").time())
            else:
                start_time = datetime.strptime(app.config["SHIFT_START_TIME"], "%H:%M").time()

            end_time = datetime.strptime(app.config["SHIFT_END_TIME"], "%H:%M").time()
            slot_book_time = app.config["SLOT_BOOK_TIME"]
            data=self.generate_slots(start_time,end_time,slot_book_time)
            
            previous_appointments=AppointmentRecords.query.filter(db.func.DATE(AppointmentRecords.appointment_start_time)\
                        ==date_obj,AppointmentRecords.doctor_id == doctor_id).all()
            if previous_appointments:
                for i in previous_appointments:
                    if str(i.appointment_start_time.time()) in data:
                        data.remove(str(i.appointment_start_time.time()))
            
            status=1
            message="Data correspoding to doctor has been fetched successfully"
        else:
            err=f"Doctor having doctor_id as {doctor_id} does not exist"
            status=0
            response_code=404
        return RestResponse(status=status,message=message,err=err,data=data).to_json(),response_code

    def create_appointment(self,data_dict):
        status,message,err,data,response_code=0,"","",{},200
        patient=PatientModel.find_by_id(data_dict["patient_id"])
        doctor=DoctorModel.find_by_id(data_dict["doctor_id"])
        booking_type=data_dict.pop("booking_type")
        if patient and doctor:
            doctor_appointments=AppointmentRecords.find_by("doctor_id",doctor.id)
            data_dict["appointment_start_time"]=datetime.strptime(data_dict["appointment_start_time"], "%Y-%m-%d %H:%M")
            
            if doctor_appointments and data_dict["appointment_start_time"] in [i.appointment_start_time for i in doctor_appointments] :
                if booking_type==AppointmentBookingEnum.ASSIGN.value:
                    message="Doctor with this time slot has been already booked"
                    status=1
                elif booking_type==AppointmentBookingEnum.RESIGN.value:
                    record=AppointmentRecords.find_by('appointment_start_time',data_dict["appointment_start_time"])[0]
                    record.patient_id=data_dict['patient_id']
                    record.doctor_id=data_dict['doctor_id']
                    record.purpose=data_dict['purpose']
                    record.save()
                    message="Doctor has been successfully reassigned"
                    data=record.to_json()
                    status=1
                    
            else:
                
                appointment_record=AppointmentRecords(**data_dict)
                appointment_record.save()
                data=appointment_record.to_json()
                status=1
                message="Appointment has been scheduled successfully"
        else:
            err="Either patient id or doctor id does not exist in database"
            response_code=404
        return RestResponse(status=status,message=message,err=err,data=data).to_json(),response_code
    
