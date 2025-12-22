from datetime import datetime
from appointment.util.core.models import Doctor, Patient, Appointment, AppointmentStatus

def str_to_dt(dt_str):
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M")

MOCK_DATA = {
    "hospitals": [
        {"id": "1", "name": "Medipol Hospital", "city": "Ankara", "district": "Çankaya"},
        {"id": "2", "name": "Hacettepe Hospital", "city": "Ankara", "district": "Çankaya"},
        {"id": "3", "name": "Acıbadem Hospital", "city": "İstanbul", "district": "Fatih"},
        {"id": "4", "name": "Haseki Hospital", "city": "İstanbul", "district": "Fatih"},
        {"id": "5", "name": "Öztan Hospital", "city": "İzmir", "district": "Bornova"},
        {"id": "6", "name": "YKB Private Hospital", "city": "İzmir", "district": "Bornova"},
        {"id": "7", "name": "Sorgun Devlet Hastanesi", "city": "Yozgat", "district": "Sorgun"},
        {"id": "8", "name": "EKABI Hospital", "city": "Yozgat", "district": "Sorgun"}
    ],

    "doctors": [
        Doctor(id="101", hospital_id="1", name="Dr. Ayşe Yılmaz", branch="Kardiyoloji"),
        Doctor(id="201", hospital_id="1", name="Dr. Emre Şahin", branch="Kardiyoloji"),
        Doctor(id="102", hospital_id="2", name="Dr. Mehmet Kaya", branch="Kardiyoloji"),
        Doctor(id="202", hospital_id="2", name="Dr. Selin Özkan", branch="Kardiyoloji"),
        Doctor(id="103", hospital_id="1", name="Dr. Zeynep Can", branch="KBB"),
        Doctor(id="105", hospital_id="1", name="Dr. Nihat Aksoy", branch="Nöroloji"),
    ],

    "patients": [
        Patient(id="123456789", name="Demo Hasta", age = 25)
    ],

    "appointments": [
        Appointment(
            id="6500c262-8ecf-46a9-a1ec-f50eb7f4f9aa",
            doctor_id="201",
            patient_id="123456789",
            hospital_id="2",
            start_time=str_to_dt("2025-08-14 08:50"),
            end_time=str_to_dt("2025-08-14 09:20"),
            status=AppointmentStatus.BOOKED
        ),
        Appointment(
            id="7cb80365-b031-4784-9c68-2fef90c5ccbf",
            doctor_id="101",
            patient_id="123456789",
            hospital_id="2",
            start_time=str_to_dt("2025-08-19 09:00"),
            end_time=str_to_dt("2025-08-19 09:30"),
            status=AppointmentStatus.BOOKED
        )
    ],

    "availability_map": {
        "101": {"2025-08-10": ["09:00", "10:30"]},
        "201": {"2025-08-12": ["09:00"]},
        "102": {"2025-08-10": ["14:00"]},
        "202": {"2025-08-11": ["10:00"]},
        "103": {"2025-08-10": ["11:00"]},
        "105": {"2025-08-10": ["16:00"]},
        "107": {"2025-08-10": ["16:00"]},
        "109": {"2025-08-10": ["10:00"]},
        "111": {"2025-08-10": ["11:30"]},
        "113": {"2025-08-10": ["09:30"]},
        "117": {"2025-08-14": ["09:00"]},
        "127": {"2025-08-14": ["08:50", "11:30"]},
        "227": {"2025-08-19": ["09:00"]}
    }
}