from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

class AppointmentStatus(Enum):
    AVAILABLE = "MÜSAİT"
    BOOKED = "DOLU"
    CANCELLED = "CANCEL"
    COMPLETED = "TAMAMLANDI"

@dataclass(frozen=True)
class Hospital:
    id: str
    name: str
    city: str
    district: str

@dataclass(frozen=True)
class Doctor:
    id: str
    hospital_id: str
    name: str
    branch: str

@dataclass
class Patient:
    id: str
    name: str
    age: int

@dataclass
class Appointment:
    id: str
    doctor_id: str
    patient_id: str
    start_time: datetime
    end_time: datetime
    status: AppointmentStatus = AppointmentStatus.BOOKED
    hospital_id: Optional[str] = None