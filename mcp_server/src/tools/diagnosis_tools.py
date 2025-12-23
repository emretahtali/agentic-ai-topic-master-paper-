from .tool_base import ToolBase


class DiagnosisTools(ToolBase):

    def __init__(self):
        pass

    def get_user_health_record(self, patient_id: str = "12345678901") -> dict:
        """
        Retrieves the comprehensive medical history and health profile of the patient.

        This tool acts as the "Source of Truth" for the patient's background.
        ALWAYS call this tool at the beginning of a diagnosis session to understand risk factors.

        --- USE CASES ---
        1. Context Loading: Before asking symptoms, know who you are talking to (e.g., if user has Hypertension, chest pain is more critical).
        2. Safety Check: Before suggesting medication or food, check 'allergies' and 'chronic_diseases'.
        3. Lifestyle Analysis: Use 'smoking' and 'alcohol' data to tailor advice.

        --- ARGUMENTS ---
        Args:
            patient_id (str, Optional): The unique ID of the patient.
                Defaults to the current authenticated user if not provided.

        --- RETURNS ---
        Returns:
            dict: A dictionary containing:
                - allergies (List[str]): Known allergies (e.g., ['Peanuts']).
                - chronic_diseases (List[str]): Ongoing conditions (e.g., ['Hypertension']).
                - use_of_smoking (str): Frequency or status (e.g., 'No', 'Daily').
                - use_of_alcohol (str): Frequency (e.g., 'Occasionally').
                - past_operations (str): History of surgeries.
        """
        try:
            records = dict()
            records["patient_id"] = patient_id
            records["allergies"] = ["Peanuts", "Penicillin"]
            records["use_of_smoking"] = "No"
            records["use_of_alcohol"] = "Occasionally"
            records["past_operations"] = "Appendectomy"
            records["chronic_diseases"] = ["Hypertension", "Asthma"]

            return {"health_record": records}

        except Exception as e:
            return {"error": f"Failed to fetch health records: {str(e)}"}

    def appointment_tool(self):
        """
        Placeholder for appointment booking integration.
        Currently not active for Diagnosis Agent.
        """
        pass