from hospital_management_system.models.patients import PatientModel,PatientMedicalHistory,AppointmentRecords
from sqlalchemy import exc
from hospital_management_system.helpers.rest_response import RestResponse

class PatientService:
    def create_patient(self,data_dict):
        status,message,err,data,response_code=0,"","",{},201
        try:
            patient=PatientModel(**data_dict)
            patient.save()
            status=1
            message="Patient has been successfully created"
            data=patient.to_json()
        except exc.IntegrityError:
            err="A patient with this email or phone number already exists. Please use a different email or phone number."
            response_code=400
        return RestResponse(err=err,message=message,status=status,data=data).to_json(),response_code

    def get_patients(self):
        data,response_code=[],200
        all_patients=PatientModel.find_all()
        # TODO:Rohan, check for all medical records
        data=[{"medical_history":[j.to_json() for j in i.medical_history],\
               "appointment_records":[j.to_json() for j in i.appointment_records],\
               **i.to_json()} for i in all_patients]
        return RestResponse(message="All patient data has been been fetched successfully",data=data,status=1).to_json(),response_code

    def create_patient_record(self,data_dict):
        status,message,err,data,response_code=0,"","",{},201        
        patient=PatientModel.find_by_id(data_dict['patient_id'])
        if patient:
            patient=PatientMedicalHistory(**data_dict)
            patient.save()
            message="Patient Record has been created successfully"
            status=1
            data=patient.to_json()
        else:
            err=f"Patient with id {data_dict['patient_id']} does not exist"
            response_code=400
        return RestResponse(message=message,status=status,data=data,err=err).to_json(),response_code

    def get_patient_medical_record(self,id):
        status,message,err,data,response_code=0,"","",{},200        
        patient_medical_history=PatientMedicalHistory.find_by_id(id)        
        if patient_medical_history:
            status=1
            message="Pateint history has been fetched successfully"
            data=patient_medical_history.to_json()
        else:
            err=f"Patient Medical History with id {id} does not exist "
        return RestResponse(message=message,status=status,data=data,err=err).to_json(),response_code

    def update_patient_medical_record(self,id,data_dict):
        status,message,err,data,response_code=0,"","",{},200        
        patient_medical_history=PatientMedicalHistory.find_by_id(id)        
        if patient_medical_history:
            for key in data_dict:
                    setattr(patient_medical_history, key, data_dict[key])

            patient_medical_history.save()
            data=patient_medical_history.to_json()
            message="Patient record updated successfully"
            status=1
        else:
            err=f"Patient Medical History with id {id} does not exist "
        return RestResponse(message=message,status=status,data=data,err=err).to_json(),response_code

    def get_patient_record(self,id):
        status,message,err,data,response_code=0,"","",{},200      
        patient=PatientModel.find_by_id(id)
        if patient:
            data=patient.to_json()
            data['medical_history']=[i.to_json() for i in patient.medical_history]
            data['appointment_records']=[i.to_json() for i in patient.appointment_records]
    
            status=1
            message="Patient data has been fetched successfully"
        else:
            response_code=400
            err=f"Patient with id {id} does not exist"
        return RestResponse(message=message,status=status,data=data,err=err).to_json(),response_code

    def update_patient_record(self,id,data_dict):
        status,message,err,data,response_code=0,"","",{},200
        patient=PatientModel.find_by_id(id)
        if patient:
            for key in data_dict:
                    setattr(patient, key, data_dict[key])
            patient.save()
            data=patient.to_json()
            data['medical_history']=[i.to_json() for i in patient.medical_history]
            data['appointment_records']=[i.to_json() for i in patient.appointment_records]            


            status=1
            message="Pateint data has been updated successfully"
        else:
            response_code=400
            err=f"Patient with id {id} does not exist"
        return RestResponse(message=message,status=status,data=data,err=err).to_json(),response_code
    
    def get_patient_appointment_record(self,patient_id):
        status,message,err,data,response_code=0,"","",{},200
        patient=PatientModel.find_by_id(patient_id)
        if patient:
            message="Appointment records has been fetched successfully"
            status=1
            data=AppointmentRecords.find_by("patient_id",patient_id)
            data=[i.to_json() for i in data]
            
        else:
            err=f"Patient having id as {patient_id} does not exist"
            response_code=404
        return RestResponse(message=message,status=status,data=data,err=err).to_json(),response_code
