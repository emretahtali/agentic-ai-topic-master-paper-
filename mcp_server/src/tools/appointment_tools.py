from typing import Dict, Any
from .tool_base import ToolBase
from appointment.appointment_manager import AppointmentManager


class AppointmentTools(ToolBase):

    def __init__(self):
        self.service = AppointmentManager()

    # ---------- HELPERS ----------

    @staticmethod
    def _appointment_to_dict(appointment_obj) -> Dict[str, Any]:
        """
        [Helper] Converts an Appointment object to a dictionary for JSON serialization.
        """
        return {
            "id": appointment_obj.id,
            "doctor_id": appointment_obj.doctor_id,
            "patient_id": appointment_obj.patient_id,
            "start_time": appointment_obj.start_time.strftime("%Y-%m-%d %H:%M"),
            "status": appointment_obj.status.value,
            "hospital_id": appointment_obj.hospital_id
        }

    # ---------- PUBLIC TOOLS ----------

    def get_available_hospitals(self, city: str = None, district: str = None) -> dict:
        """
        Retrieves a list of active hospitals, optionally filtered by location.

        Args:
            city: The city name extracted from user query (e.g., "İstanbul").
            district: The district name extracted from user query (e.g., "Kadıköy").

        Returns:
            On success: {"hospitals": [{"id": "1", "name": "..."}]}
            On error: {"error": <error message>}
        """
        try:
            hospitals = self.service.get_available_hospitals(city=city, district=district)
            return {"hospitals": hospitals}
        except Exception as e:
            return {"error": str(e)}

    def get_available_slots(self, hospital_id: str = None, branch: str = None,
                            doctor_id: str = None, date_str: str = None) -> dict:
        """
        Searches for available appointment slots based on various filters.

        Use this when the user asks for doctor availability or free times.

        Args:
            hospital_id: Filter by specific hospital ID.
            branch: Filter by medical specialty (e.g., 'Cardiology').
            doctor_id: Filter by a specific doctor ID.
            date_str: Filter by a specific date (YYYY-MM-DD).

        Returns:
            On success: {"available_slots": [...]}
            On error: {"error": <error message>}
        """
        try:
            slots = self.service.get_available_slots(
                hospital_id=hospital_id,
                branch=branch,
                doctor_id=doctor_id,
                date_str=date_str
            )
            return {"available_slots": slots}
        except Exception as e:
            return {"error": str(e)}

    def get_patient_appointments(self, patient_id: str) -> dict:
        """
        Retrieves the entire appointment history for a specific patient.

        Args:
            patient_id: The unique identifier of the patient.

        Returns:
            On success: {"appointments": [...]}
            On error: {"error": <error message>}
        """
        try:
            apps = self.service.get_patient_appointments(patient_id=patient_id)
            return {"appointments": apps}
        except Exception as e:
            return {"error": str(e)}

    def create_appointment(self, doctor_id: str, patient_id: str,
                           date_str: str, time_str: str) -> dict:
        """
        Creates a new medical appointment in the system.

        Args:
            doctor_id: The unique ID of the doctor.
            patient_id: The unique ID of the patient.
            date_str: The date of the appointment in "YYYY-MM-DD" format.
            time_str: The time of the appointment in "HH:MM" format.

        Returns:
            On success: {"result": {"id": "...", "status": "...", ...}}
            On error: {"error": <error message>}
        """
        try:
            new_app = self.service.create_appointment(
                doctor_id=doctor_id,
                patient_id=patient_id,
                date_str=date_str,
                time_str=time_str
            )
            return {"result": self._appointment_to_dict(new_app)}
        except Exception as e:
            return {"error": str(e)}

    def update_appointment(self, appointment_id: str, new_doctor_id: str = None,
                           new_date_str: str = None, new_time_str: str = None) -> dict:
        """
        Updates an existing appointment by cancelling the old one and creating a new one.

        Args:
            appointment_id: The unique UUID of the appointment to be updated.
            new_doctor_id: The ID of the new doctor (optional).
            new_date_str: New date in "YYYY-MM-DD" format (optional).
            new_time_str: New time in "HH:MM" format (optional).

        Returns:
            On success: {"result": {"id": "...", "status": "...", ...}}
            On error: {"error": <error message>}
        """
        try:
            updated_app = self.service.update_appointment(
                appointment_id=appointment_id,
                new_doctor_id=new_doctor_id,
                new_date_str=new_date_str,
                new_time_str=new_time_str
            )
            return {"result": self._appointment_to_dict(updated_app)}
        except Exception as e:
            return {"error": str(e)}

    def cancel_appointment(self, appointment_id: str) -> dict:
        """
        Cancels an existing appointment.

        Args:
            appointment_id: The unique ID of the appointment.

        Returns:
            On success: {"result": {"message": "...", "status": "CANCELLED"}}
            On error: {"error": <error message>}
        """
        try:
            result = self.service.cancel_appointment(appointment_id=appointment_id)
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}

    def get_doctors_by_hospital_and_branch(self, hospital_id: str, branch: str) -> dict:
        """
        Retrieves the list of doctors associated with a specific hospital and branch.

        Args:
            hospital_id: The unique identifier of the hospital.
            branch: The medical branch or specialization.

        Returns:
            On success: {"doctors": [{"id": "...", "name": "..."}, ...]}
            On error: {"error": <error message>}
        """
        try:
            docs = self.service.get_doctors_by_hospital_and_branch(
                hospital_id=hospital_id,
                branch=branch
            )
            return {"doctors": docs}
        except Exception as e:
            return {"error": str(e)}