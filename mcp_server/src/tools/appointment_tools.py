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
        Retrieves a list of active hospitals from the database, optionally filtered by location (City/District).

        This tool serves as the initial step for appointment booking or general hospital inquiries.
        It enables the agent to show options to the user before proceeding to department selection.

        --- USE CASES (When to use this tool) ---
        1. User asks generic questions: "Which hospitals are available?", "List all hospitals."
        2. User specifies a location: "Is there a hospital in Ankara?", "Find hospitals in Kadıköy."
        3. User wants to book an appointment but hasn't selected a hospital yet.
        4. User provides a partial location: "Hospitals in Beşiktaş" (Extract 'Beşiktaş' as district).

        --- PARAMETER RULES ---
        - city (str, Optional): The city name. Must be a full city name (e.g., 'İstanbul', 'Ankara').
          If the user mentions a district but no city, try to infer the city or leave it None.
        - district (str, Optional): The specific district/county. (e.g., 'Çankaya', 'Kadıköy').
          Do not hallucinate districts if not explicitly mentioned or strongly implied.

        --- BEHAVIOR ---
        - If NO city or district is provided by the user, this tool MUST be called without arguments to retrieve the full list.
        - Returns a list of dictionaries containing 'id', 'name', 'city', and 'district'.

        Returns:
            On success: {"hospitals": [{"id": "1", "name": "Acıbadem", "city": "İstanbul"}, ...]}
            On error: {"error": "Database connection failed"}
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
        Retrieves the entire appointment history and upcoming schedule for a specific patient.

        This tool is ESSENTIAL for context awareness. It acts as the "memory" of the user's interactions.

        --- USE CASES ---
        1. Status Check: User asks "When is my next appointment?" or "Do I have any bookings?"
        2. PRE-ACTION STEP (Crucial): If the user says "Cancel my appointment" or "Reschedule my visit"
           WITHOUT providing specific details, call this tool FIRST to list their active appointments
           so the user can select the correct one.
        3. History: User asks "Who was the doctor I saw last week?"

        Args:
            patient_id (str): The unique identifier of the patient.
                RULE: Usually obtained from the authenticated user context (e.g., 'patient_1').
                Do not invent or hallucinate a patient ID if it's not provided in the context.

        Returns:
            On success: {"appointments": [
                {"appointment_id": "...", "doctor": "Dr. X", "date": "...", "status": "BOOKED"}, ...
            ]}
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
        Finalizes and creates a new medical appointment in the system.

        This is a COMMIT ACTION. It should be triggered only after the user has explicitly
        confirmed the details and you have verified the slot availability.

        --- USE CASES ---
        1. Explicit Booking: User says "Yes, book Dr. Ali for tomorrow at 10:00."
        2. Flow Completion: The final step after listing available slots and getting user selection.

        --- CRITICAL RULES FOR ARGUMENTS ---
        Args:
            doctor_id (str): The unique UUID of the doctor.
                RULE: Do NOT guess. If the user provided a name (e.g., "Dr. Ayşe"),
                you must have already resolved it to an ID using 'get_available_slots' or 'get_doctors...'.

            patient_id (str): The unique ID of the patient.
                RULE: Get this from the current user session/context.

            date_str (str): The date of the appointment.
                RULE: STRICT FORMAT "YYYY-MM-DD". You must convert relative dates
                (e.g., "tomorrow", "next Friday", "12th of August") to this exact format.

            time_str (str): The time of the appointment.
                RULE: STRICT FORMAT "HH:MM" (24-hour clock). Example: "09:00", "14:30".

        Returns:
            On success: {"result": {"id": "...", "status": "BOOKED", ...}}
            On error: {"error": "The slot 2025-08-10 09:00 is already booked."}
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
        Modifies an existing appointment's details (Time, Date, or Doctor).

        This tool performs a "Safe Update". It checks availability for the new slot BEFORE
        cancelling the old one. If the new slot is full, the old appointment remains active (no data loss).

        --- USE CASES ---
        1. Rescheduling: User says "Change my appointment to 14:00" or "Move it to next Monday."
        2. Swapping Doctor: User says "Actually, I want to see Dr. House instead."
        3. Correction: User realizes they picked the wrong date and wants to fix it.

        --- CRITICAL RULES FOR ARGUMENTS ---
        Args:
            appointment_id (str): The unique UUID of the appointment to update.
                RULE: You MUST identify the correct appointment first using 'get_patient_appointments'.
                Never hallucinate this ID. If the user has multiple appointments, ask them which one to change.

            new_doctor_id (str, optional): The ID of the new doctor.
                RULE: Provide ONLY if the user explicitly wants to change the doctor.
                If the doctor remains the same, send None.

            new_date_str (str, optional): The new date.
                RULE: STRICT FORMAT "YYYY-MM-DD". Convert "next week", "tomorrow" to this format.
                If the date remains the same (e.g., only changing time), send None.

            new_time_str (str, optional): The new time.
                RULE: STRICT FORMAT "HH:MM".
                If the time remains the same (e.g., only changing doctor), send None.

        Returns:
            On success: {"result": {"id": "...", "status": "BOOKED", ...}} (New appointment object)
            On error: {"error": "The slot is already booked."} (Old appointment remains valid)
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
        Cancels an existing appointment, releasing the booked slot.

        This is a DESTRUCTIVE ACTION. Once cancelled, the slot becomes free for other patients immediately.

        --- USE CASES ---
        1. Direct Cancellation: User says "Cancel my appointment with Dr. Ali."
        2. Unable to attend: User says "I won't be able to make it tomorrow."
        3. Clean up: User booked by mistake and wants to remove it immediately.

        --- CRITICAL RULES FOR ARGUMENTS ---
        Args:
            appointment_id (str): The unique UUID of the appointment to cancel.
                RULE: You MUST first retrieve the user's appointments using 'get_patient_appointments'
                to find the correct ID.
                NEVER hallucinate or guess this ID.
                NEVER try to cancel using a natural language description (e.g., "the 9 AM one")
                without resolving it to a UUID first.

        Returns:
            On success: {"result": {"message": "...", "status": "CANCELLED"}}
            On error: {"error": "Appointment not found"}
        """
        try:
            result = self.service.cancel_appointment(appointment_id=appointment_id)
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}

    def get_doctors_by_hospital_and_branch(self, hospital_id: str, branch: str) -> dict:
        """
        Retrieves a targeted list of doctors working at a specific hospital within a specific medical branch.

        This tool is a FILTERING STEP. It helps narrow down the user's options when they know
        "Where" (Hospital) and "What" (Specialty) but need to select "Who" (Doctor).

        --- USE CASES ---
        1. Specific Search: User says "I need a Cardiologist at Ankara City Hospital."
        2. Exploration: User asks "Who are the dermatologists in this hospital?"
        3. Pre-booking: User wants to book a specific specialty but hasn't picked a doctor yet.

        --- CRITICAL RULES FOR ARGUMENTS ---
        Args:
            hospital_id (str): The unique ID of the hospital.
                RULE: You MUST have a valid hospital ID (e.g., '1').
                Do NOT pass a hospital name (e.g., "Ankara Hastanesi") directly.
                Use 'get_available_hospitals' first to find the correct ID corresponding to the name.

            branch (str): The medical specialization (e.g., "Kardiyoloji", "Dahiliye").
                RULE: Normalize user input to standard medical terms matching the system language.
                (e.g., if user says "heart doctor", convert to "Kardiyoloji"; if "eye", convert to "Göz Hastalıkları").

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