from typing import Dict, Any, Annotated
from pydantic import Field
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

    def get_available_hospitals(self, city: str, district: str = None) -> dict:
        """
        Retrieves a list of active hospitals from the database, optionally filtered by location (City/District).

        This tool serves as the initial step for appointment booking or general hospital inquiries.
        It enables the agent to show options to the user before proceeding to department selection.

        --- CRITICAL RULE ---
        This tool requires a 'city' argument. If the user asks "Show me hospitals"
        WITHOUT specifying a city, DO NOT call this tool immediately.
        Instead, ask the user: "Which city are you looking for?"

        --- USE CASES (When to use this tool) ---
        1. User specifies a location: "Is there a hospital in Ankara?", "Find hospitals in Kadıköy."
        2. User wants to book an appointment but hasn't selected a hospital yet.
        3. User provides a partial location: "Hospitals in Beşiktaş" (Extract 'Beşiktaş' as district).

        --- PARAMETER RULES ---
        - city (str, REQUIRED): The city name.
          RULE: This is MANDATORY. You must extract a valid city name (e.g., 'İstanbul', 'İzmir').
          If the user provided only a district (e.g., 'Çankaya'), you must infer the city (e.g., 'Ankara') or ask the user.

        - district (str, OPTIONAL): The specific district/county.
          RULE: Send this only if explicitly mentioned. Default is None.

        --- BEHAVIOR ---
        - Returns a list of dictionaries containing 'id', 'name'.

        Returns:
            On success: {"hospitals": [{"id": "1", "name": "Acıbadem", ...]}
            On error: {"error": "Database connection failed"}
        """
        try:
            hospitals = self.service.get_available_hospitals(city=city, district=district)
            return {"hospitals": hospitals}
        except Exception as e:
            return {"error": str(e)}

    def get_available_slots(self, doctor_id: str) -> dict:
        """
        Retrieves the full list of available appointment slots for a KNOWN doctor.

        This tool returns the doctor's entire schedule.
        Use it after the user has selected a specific doctor to see when they are free.

        --- CRITICAL RULE ---
        You MUST know the 'doctor_id' before calling this tool.
        Do not use this tool for general searches like "Find a cardiologist".
        First find the doctor, then call this tool to get their hours.

        --- USE CASES ---
        1. User asks: "When is Dr. Ali available?" (Resolve Dr. Ali -> ID first).
        2. User asks: "What are the working hours of this doctor?"

        --- ARGUMENTS ---
        Args:
            doctor_id (str, REQUIRED): The unique identifier of the doctor.
                RULE: You must extract this from the output of 'get_doctors_by_hospital_and_branch'.
                Never guess or hallucinate an ID.

        Returns:
            On success: {"available_slots": [{"doctor_name": "...", "schedule": [{"date": "...", "slots": [...]}]}]}
            On error: {"error": "Doctor not found" or other messages}
        """
        try:
            slots = self.service.get_available_slots(doctor_id=doctor_id)
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

    def create_appointment(
            self,
            doctor_id: str,
            patient_id: str,
            date_str: Annotated[str, Field(
                description="The date of the appointment in STRICT 'YYYY-MM-DD' format. Calculate relative dates (like 'tomorrow') based on the current date.")],
            time_str: Annotated[
                str, Field(description="The time of the appointment in STRICT 'HH:MM' format (24-hour clock).")]
    ) -> dict:
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
                you must have already resolved it to an ID using 'get_available_slots'.

            patient_id (str): The unique ID of the patient.
                RULE: Get this from the current user session/context.

            date_str (str): The date of the appointment.
                RULE: STRICT FORMAT "YYYY-MM-DD".

            time_str (str): The time of the appointment.
                RULE: STRICT FORMAT "HH:MM".

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

    def update_appointment(
            self,
            appointment_id: Annotated[str, Field(
                description="The unique UUID of the appointment to update. You MUST identify the correct appointment first using 'get_patient_appointments'."
            )],
            new_doctor_id: Annotated[str, Field(
                description="The ID of the new doctor. Provide ONLY if the user explicitly wants to change the doctor. Otherwise leave None."
            )] = None,
            new_date_str: Annotated[str, Field(
                description="The new date in STRICT 'YYYY-MM-DD' format. Calculate relative dates (like 'tomorrow') based on current date. Leave None if date is unchanged."
            )] = None,
            new_time_str: Annotated[str, Field(
                description="The new time in STRICT 'HH:MM' format. Leave None if time is unchanged."
            )] = None
    ) -> dict:
        """
        Modifies an existing appointment's details (Time, Date, or Doctor).

        This tool performs a "Safe Update". It checks availability for the new slot BEFORE
        cancelling the old one. If the new slot is full, the old appointment remains active (no data loss).

        --- USE CASES ---
        1. Rescheduling: User says "Change my appointment to 14:00" or "Move it to next Monday."
        2. Swapping Doctor: User says "Actually, I want to see Dr. House instead."
        3. Correction: User realizes they picked the wrong date and wants to fix it.

        --- CRITICAL RULES ---
        - You generally only need to send the field that is changing.
        - If the user changes ONLY the time, send new_time_str and leave new_date_str as None.

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