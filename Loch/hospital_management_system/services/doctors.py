from hospital_management_system.models.doctors import DoctorModel
from sqlalchemy import exc,func,join
from hospital_management_system import db
from hospital_management_system.helpers.rest_response import RestResponse
from hospital_management_system.models.patients import AppointmentRecords,PatientModel
from datetime import datetime
class DoctorService:
    def create_doctor(self,data_dict):
        status,message,err,data,response_code=0,"","",{},201
        try:
            doctor=DoctorModel(**data_dict)
            doctor.save()
            status=1
            message="Doctor has been successfully created"
            data=doctor.to_json()
        except exc.IntegrityError:
            err="A doctor with this email or phone number already exists. Please use a different email or phone number."
            response_code=400
        return RestResponse(err=err,message=message,status=status,data=data).to_json(),response_code

    @staticmethod
    def format_res(li):
        res=[]
        for i in li:
            is_found=False
            for j in res:
                if j["id"]==i["id"]:
                    j['appointment_start_time'].append(i['appointment_start_time'])
                    is_found=True
            if not is_found:
                min_dict={**i}
                min_dict["appointment_start_time"]=[min_dict["appointment_start_time"]]
                res.append(min_dict)
        return res


    def get_patient_list(self,doctor_id):
        status,message,err,data,response_code=0,"","",[],200
        doctor=DoctorModel.find_by_id(doctor_id)
        res=[]
        if doctor:
            patients=[(i.patient_id,i.appointment_start_time) for i in AppointmentRecords.find_by("doctor_id",doctor_id)]
            for patient_id,appointment_start_time in patients:
                res.append({**PatientModel.find_by_id(patient_id).to_json(),"appointment_start_time":str(appointment_start_time)})


            data=self.format_res(res)

            status=1
            message="Patient List has been fetched successfully"
        
        else:
            err=f"Doctor with corresponding {doctor_id} does not exist"
            response_code=404
        return RestResponse(err=err,message=message,status=status,data=data).to_json(),response_code
    
    def get_doctors(self):
        status,message,err,data,response_code=1,"Doctors has been fetched successfully","",[],200
        data=[i.to_json() for i in DoctorModel.find_all()]
        return RestResponse(err=err,message=message,status=status,data=data).to_json(),response_code
    
    def get_busy_doctor(self,data_dict):
        status,message,err,data,response_code=0,"","",[],200
        date_format = '%d/%m/%Y %H:%M'
        date_time_obj = datetime.strptime(f"{data_dict['date']} {data_dict['time']}", date_format)
        data=db.session.query(AppointmentRecords, DoctorModel)\
            .join(DoctorModel, AppointmentRecords.doctor_id == DoctorModel.id)\
            .filter(AppointmentRecords.appointment_start_time == date_time_obj).all()
        data=[{**i.to_json(),**j.to_json()} for i,j in data]
        status=1
        message="Busy doctors have been fetched successfully"
        return RestResponse(err=err,message=message,status=status,data=data).to_json(),response_code
        