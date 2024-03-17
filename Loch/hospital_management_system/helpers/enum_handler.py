from enum import Enum,unique

@unique
class GenderEnum(Enum):
    MALE="male"
    FEMALE="female"
    OTHER="other"

@unique
class MedicalHistoryEnum(Enum):
    PREVIOUS_DIAGNOSES="previous_diagnoses"
    ALLERGIES ="allergies"
    MEDICATIONS="medications"

@unique
class AppointmentBookingEnum(Enum):
    ASSIGN="assign"
    RESIGN="reassign"

@unique
class SearchModelNameEnum(Enum):
    PATIENTS="patients"
    DOCTORS= "doctors" 
    DEPARTMENTS="departments"

@unique
class SearchTypeEnum(Enum):
    EXACT="exact"
    PARTIAL="partial"
    STARTS_WITH="starts_with"