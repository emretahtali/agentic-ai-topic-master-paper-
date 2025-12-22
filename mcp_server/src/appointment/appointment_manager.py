from datetime import datetime, timedelta
import uuid
from typing import List

from appointment.util.data import MOCK_DATA
from appointment.util.core.models import *


class AppointmentManager:
    """ Manages medical appointments including creation and updates."""

    def __init__(self):
        self.hospitals = MOCK_DATA["hospitals"]
        self.doctors = MOCK_DATA["doctors"]
        self.appointments = MOCK_DATA["appointments"]
        self.availability_map = MOCK_DATA["availability_map"]
        self.patients = MOCK_DATA["patients"]

        self.appointments_by_id = {app.id: app for app in self.appointments}


    # HELPER FUNCTIONS

    def _get_appointment_by_id(self, appointment_id: str):
        """Internal helper to safely retrieve an appointment object."""
        return self.appointments_by_id.get(appointment_id)

    def _is_slot_booked(self, doctor_id: str, target_dt: datetime) -> bool:
        """Internal helper to check if a specific slot is already taken in the database."""
        for app in self.appointments:
            if (app.doctor_id == doctor_id and
                    app.status == AppointmentStatus.BOOKED and
                    app.start_time == target_dt):
                return True
        return False

    def _filter_doctors(self, hospital_id: str = None, branch: str = None) -> List:
        """Internal helper to filter doctors based on hospital and branch."""
        filtered_docs = self.doctors
        if hospital_id:
            filtered_docs = [d for d in filtered_docs if d.hospital_id == hospital_id]
        if branch:
            filtered_docs = [d for d in filtered_docs if d.branch == branch]
        return filtered_docs

    # FUNCTIONS

    def get_available_hospitals(self, city: str, district: str):
        """
        Retrieves a list of all active hospitals registered in the system with specific city and district.

        This tool MUST be used when:
        - The user asks "Which hospitals are available?"
        - The user wants to know the locations where they can book an appointment.
        - The user is browsing options before selecting a specific department.

        Returns:
            list: A list of dictionaries containing hospital ID, name, and city.
        """
        return [
            {"id": h.id, "name": h.name}
            for h in self.hospitals
        ]

    def get_available_slots(self, hospital_id: str = None, branch: str = None, doctor_id: str = None,
                            date_str: str = None):
        """
        Searches for available appointment slots based on various filters.

        This tool is the PRIMARY search engine for finding free time slots.
        Use it when the user asks: "Is Dr. X available?", "Find me a cardiologist in City Hospital",
        or "What times are free on Friday?".

        Search Logic:
        1. Filters doctors by Hospital, Branch, or specific Doctor ID.
        2. Looks up the 'Availability Map' (Working hours) for each doctor.
        3. Cross-references with existing 'Appointments' to exclude booked slots.

        Parameters:
        - hospital_id (str, OPTIONAL): Filter by specific hospital ID.
        - branch (str, OPTIONAL): Filter by medical specialty (e.g., 'Cardiology').
        - doctor_id (str, OPTIONAL): Filter by a specific doctor.
        - date_str (str, OPTIONAL): Filter by a specific date (YYYY-MM-DD). If None, returns all future slots.

        Returns:
        - list: A structured list of available slots formatted as:
          [
            {
              "doctor_name": "Dr. House",
              "branch": "Diagnostic",
              "date": "2025-10-10",
              "slots": ["09:00", "09:30", ...] // Only FREE slots
            },
            ...
          ]
        """
        results = []

        # 1. Filter relevant doctors using helper
        target_doctors = self._filter_doctors(hospital_id, branch)
        if doctor_id:
            target_doctors = [d for d in target_doctors if d.id == doctor_id]

        for doctor in target_doctors:
            # Get doctor's working schedule
            schedule = self.availability_map.get(doctor.id, {})

            doctor_availability = {
                "doctor_name": doctor.name,
                "doctor_id": doctor.id,
                "branch": doctor.branch,
                "schedule": []
            }

            for day, slots in schedule.items():
                # Apply date filter if provided
                if date_str and day != date_str:
                    continue

                # Check real availability using helper
                free_slots = []
                for time_s in slots:
                    dt_check = datetime.strptime(f"{day} {time_s}", "%Y-%m-%d %H:%M")
                    if not self._is_slot_booked(doctor.id, dt_check):
                        free_slots.append(time_s)

                if free_slots:
                    doctor_availability["schedule"].append({
                        "date": day,
                        "slots": free_slots
                    })

            if doctor_availability["schedule"]:
                results.append(doctor_availability)

        return results

    def get_patient_appointments(self, patient_id: str):
        """
        Retrieves the entire appointment history and upcoming schedule for a specific patient.

        This tool MUST be used when:
        - The user asks "What are my appointments?"
        - The user wants to check the status of their bookings.
        - The user wants to know the time of their next visit.

        Parameters:
        - patient_id (str, REQUIRED): The unique ID of the patient.

        Returns:
        - list: A list of appointment objects with Doctor names and locations resolved.
        """
        patient_apps = []
        for app in self.appointments:
            if app.patient_id == patient_id:
                # Resolve relationships for clearer output
                doc = next((d for d in self.doctors if d.id == app.doctor_id), None)
                hosp = next((h for h in self.hospitals if h.id == app.hospital_id), None)

                patient_apps.append({
                    "appointment_id": app.id,
                    "date": app.start_time.strftime("%Y-%m-%d"),
                    "time": app.start_time.strftime("%H:%M"),
                    "doctor": doc.name if doc else "Unknown",
                    "hospital": hosp.name if hosp else "Unknown",
                    "status": app.status.value
                })

        return patient_apps

    def cancel_appointment(self, appointment_id: str):
        """
        Cancels an existing appointment.

        This tool MUST be used when the user explicitly says "Cancel my appointment".

        Validation Logic:
        1. Checks if the appointment ID is valid.
        2. Checks if the appointment is already cancelled to avoid redundancy.
        3. Sets the status to 'CANCELLED' (Soft Delete).

        Parameters:
        - appointment_id (str, REQUIRED): The unique ID of the appointment.

        Returns:
        - dict: A success message confirming the cancellation.
        - Raises ValueError: If appointment not found.
        """
        app = self._get_appointment_by_id(appointment_id)

        if not app:
            raise ValueError(f"Appointment with ID {appointment_id} not found.")

        if app.status == AppointmentStatus.CANCELLED:
            return {"message": "Appointment is already cancelled.", "status": "ALREADY_CANCELLED"}

        app.status = AppointmentStatus.AVAILABLE
        print(f"❌ Appointment {appointment_id} cancelled successfully.")

        return {
            "message": "Appointment cancelled successfully.",
            "appointment_id": appointment_id,
            "status": "CANCELLED"
        }

    def get_doctors_by_hospital_and_branch(self, hospital_id:str, branch:str):
        """
        Retrieves the list of doctors associated with a specific hospital and branch.

        Args:
            hospital_id (str): The unique identifier of the hospital.
            branch (str): The medical branch or specialization.

        Returns:
            list: A list of objects containing doctor IDs and names.
        """

        result = []
        for doc in self.doctors:
            doc_obj = {
                "id": doc.id,
                "name": doc.name
            }
            result.append(doc_obj)

        return result

    def create_appointment(self, doctor_id: str, patient_id: str, date_str: str, time_str: str):
        """
        Creates a new medical appointment in the system.

        This tool MUST be used when the user explicitly requests to book a NEW appointment.
        (e.g., "Book an appointment with Dr. House for tomorrow at 10:00")

        Validation Logic:
        1. Checks if the doctor and patient exist.
        2. Checks if the doctor is working on that specific date and time (Availability Map).
        3. Checks if the doctor is already fully booked for that slot (Double Booking Check).

        Parameters:
        - doctor_id (str, REQUIRED): The unique ID of the doctor (e.g., 'doc-1').
        - patient_id (str, REQUIRED): The unique ID of the patient (e.g., 'pat-100').
        - date_str (str, REQUIRED): The date of the appointment in "YYYY-MM-DD" format.
        - time_str (str, REQUIRED): The time of the appointment in "HH:MM" format.

        Returns:
        - Appointment: The successfully created appointment object.
        - Raises ValueError: If the slot is unavailable, doctor not found, or invalid format.
        """

        doctor = next((d for d in self.doctors if d.id == doctor_id), None)
        if not doctor:
            raise ValueError(f"Doctor with ID {doctor_id} not found.")

        patient = next((p for p in self.patients if p.id == patient_id), None)
        if not patient:
            raise ValueError(f"Patient with ID {patient_id} not found.")

        doc_slots = self.availability_map.get(doctor_id, {}).get(date_str, [])
        if time_str not in doc_slots:
            raise ValueError(f"Doctor {doctor.name} is not available at {date_str} {time_str}.")

        target_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

        for app in self.appointments:
            if (app.doctor_id == doctor_id and
                    app.status == AppointmentStatus.BOOKED and
                    app.start_time == target_dt):
                raise ValueError(f"The slot {date_str} {time_str} is already booked.")

        new_id = str(uuid.uuid4())
        new_appointment = Appointment(
            id=new_id,
            doctor_id=doctor_id,
            patient_id=patient_id,
            start_time=target_dt,
            status=AppointmentStatus.BOOKED,
            end_time=target_dt + timedelta(minutes=30),
            hospital_id=doctor.hospital_id
        )

        self.appointments.append(new_appointment)
        self.appointments_by_id[new_id] = new_appointment

        return new_appointment



    def update_appointment(self, appointment_id: str, new_doctor_id: str = None, new_date_str: str = None, new_time_str: str = None) -> Appointment:
        """
        Updates an existing appointment by atomically cancelling the old one and creating a new one.

        This tool MUST be used whenever the user requests a change to an ALREADY BOOKED appointment.
        (e.g., "Change my appointment time to 14:00", "I want to see another doctor", etc.)

        Behavior and Rules:
        - ATOMICITY: The system performs a "Safe Update". It first checks if the NEW slot is available.
          If the new slot is busy or the doctor is unavailable, the function raises an error
          and the OLD appointment remains ACTIVE (no data loss).
        - PARTIAL UPDATES: Only provide the fields that need to change.
          The system will automatically copy the remaining data from the old appointment.

        Parameters:
        - appointment_id (str, REQUIRED): The unique UUID of the appointment to be updated.
        - new_doctor_id (str, OPTIONAL): The ID of the new doctor (only if changing doctor).
        - new_date_str (str, OPTIONAL): New date in "YYYY-MM-DD" format (only if changing date).
        - new_time_str (str, OPTIONAL): New time in "HH:MM" format (only if changing time).

        Returns:
        - Appointment: The newly created appointment object.
        - Raises ValueError: If the new slot is full, the doctor is unavailable, or appointment_id is invalid.

        Example Usage:
            # 1. Change only time (Date and Doctor remain same):
            update_appointment(appointment_id="uuid-123...", new_time_str="14:30")

            # 2. Change Doctor and Date (Time remains same):
            update_appointment(appointment_id="uuid-123...", new_doctor_id="doc-99", new_date_str="2025-08-20")
        """

        old_appointment = self.appointments_by_id.get(appointment_id)

        if not old_appointment:
            raise ValueError("id can not found.")

        if old_appointment.status == AppointmentStatus.CANCELLED:
            raise ValueError("this appointment already cancelled.")

        target_doctor_id = new_doctor_id if new_doctor_id else old_appointment.doctor_id

        current_date_str = old_appointment.start_time.strftime("%Y-%m-%d")
        current_time_str = old_appointment.start_time.strftime("%H:%M")

        target_date_str = new_date_str if new_date_str else current_date_str
        target_time_str = new_time_str if new_time_str else current_time_str

        if (target_doctor_id == old_appointment.doctor_id and
                target_date_str == current_date_str and
                target_time_str == current_time_str):
            print("ℹ️ No changes detected.")
            return old_appointment

        available_slots = self.availability_map.get(target_doctor_id, {}).get(target_date_str, [])
        if target_time_str not in available_slots:
            raise ValueError(f"Doctor is not working at {target_date_str} {target_time_str}.")

        target_start_dt = datetime.strptime(f"{target_date_str} {target_time_str}", "%Y-%m-%d %H:%M")

        for app in self.appointments:
            if (app.doctor_id == target_doctor_id and
                    app.status == AppointmentStatus.BOOKED and
                    app.start_time == target_start_dt):

                if app.id != old_appointment.id:
                    raise ValueError("Seçilen yeni tarih/saat maalesef dolu.")

        print(f"🔄 Randevu güncelleniyor: {appointment_id}...")


        old_appointment.status = AppointmentStatus.AVAILABLE

        try:
            new_appointment = self.create_appointment(
                doctor_id=target_doctor_id,
                patient_id=old_appointment.patient_id,
                date_str=target_date_str,
                time_str=target_time_str
            )
            return new_appointment

        except Exception as e:
            old_appointment.status = AppointmentStatus.BOOKED
            raise e

