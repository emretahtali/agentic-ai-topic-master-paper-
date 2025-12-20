import json
from ...data.mock_data import MOCK_DATA
from typing import Any

from src.agentic_network.core.appointment_state import SlotSource, SlotStatus
from src.agentic_network.core.agent_state import AgentState


class AppointmnetTool(ToolBase):
    
    def __init__(self):
        self.mock_data = MOCK_DATA

    
    def update_appointment_slots(
        self,
        state: AgentState,
        extracted_values: dict[str, Any]
    ) -> dict:
        """
        Update the appointment state with information extracted from the user's message.

        This tool MUST be used whenever the user provides any appointment-related information
        (e.g., identity number, city, hospital, clinic, doctor, date, or time),
        even if that information is not requested at the current step.

        Behavior and Rules:
        - Only the slot corresponding to the current flow step will be directly filled.
        - Information provided for future steps MUST still be sent to this tool;
        such information will be safely stored and applied later when its turn comes.
        - Do NOT try to manage the conversation flow yourself.
        The system state determines which information is required next.

        Validation:
        - The Turkish ID number (tc_kimlik) must be exactly 11 digits and numeric.
        - If invalid data is detected, the slot will be marked as INVALID and the system
        will request the information again from the user.

        Output:
        - Returns the updated appointment state.
        - May include validation feedback messages if any provided information is invalid.

        Important:
        - Do NOT skip this tool call when the user gives relevant information.
        - Do NOT finalize or confirm the appointment inside this tool.
        - Final confirmation will only occur after all required slots are completed
        and the user explicitly confirms the appointment.

        Parameters:
        - state: The current agent state containing appointment data.
        - extracted_values: A dictionary of extracted slot values from the user's message.
        Example:
            {
            "tc_kimlik": "12345678901",
            "sehir": "Istanbul",
            "tarih": "2025-12-20"
            }
        """
        app_data = state.get("appointment_data")
        slots = app_data["slots"]
        flow = app_data["flow"]
        memory = app_data["memory"]

        validation_errors = []

        # slot filling
        for key, value in extracted_values.items():
            if key not in slots or value in (None, "null"):
                continue

            is_valid = True

            if key == "tc_kimlik":
                if not (isinstance(value, str) and len(value) == 11 and value.isdigit()):
                    validation_errors.append(
                        "TC Kimlik numarası tam olarak 11 haneli ve sadece rakam olmalıdır."
                    )
                    is_valid = False

            if not is_valid:
                slots[key]["status"] = SlotStatus.INVALID
                continue

            if flow["current_step"] == key:
                slots[key]["value"] = value
                slots[key]["status"] = SlotStatus.FILLED
                slots[key]["source"] = SlotSource.USER
            else:
                memory.setdefault("pending_slots", {})[key] = value

        # flow update
        for step in flow["steps"]:
            # Try to resolve from memory
            if (
                slots[step]["status"] == SlotStatus.EMPTY
                and step in memory.get("pending_slots", {})
            ):
                value = memory["pending_slots"].pop(step)

                # Only TC validation for now
                if step == "tc_kimlik":
                    if not (isinstance(value, str) and len(value) == 11 and value.isdigit()):
                        slots[step]["status"] = SlotStatus.INVALID
                        continue

                slots[step]["value"] = value
                slots[step]["status"] = SlotStatus.FILLED
                slots[step]["source"] = SlotSource.INFERRED

            # Determine next step
            if slots[step]["status"] in (SlotStatus.EMPTY, SlotStatus.INVALID):
                flow["current_step"] = step
                flow["completed"] = False
                break
        else:
            # All slots filled, now waiting for ONAY
            flow["current_step"] = "onay"
            flow["completed"] = False

        return {
            "appointment_data": app_data,
            "validation_feedback": validation_errors or None,
            }

    def get_hospitals_by_city_and_district(self, city: str, district: str) -> list:
        """
        Belirtilen şehir ve ilçeye göre hastanelerin listesini alır.
        Hiçbir hastane bulunamazsa, boş bir liste yerine net bir hata mesajı döndürür.

        Args:
            şehir (str): Aranacak şehrin adı.
            ilçe (str): Aranacak ilçenin adı.

        Returns:
            list: Şehir ve ilçeyle eşleşen hastane adlarının listesi.
                Hastane bulunamazsa boş bir liste döndürür.
        """
        city = city.lower()
        district = district.lower()
        hospitals = [
            h["adi"] for h in self.mock_data["hastaneler"]
            if h["konum_il"].lower() == city and h["konum_ilce"].lower() == district
        ]
        if not hospitals:
            return [{"error": "Hastane bulunamadı, lütfen şehir/ilçeyi tekrar kontrol edin"}]
        return hospitals


    # def get_hospitals_by_location(self, location: str) -> list:
    #     """
    #     Belirtilen şehir veya ilçeye göre hastanelerin listesini alır.

    #     Args:
    #         location (str): Aranacak şehir veya ilçenin adı. Büyük/küçük harfe duyarlı değildir.

    #     Returns:
    #         list: A list of hospital names that match the location.
    #                 Returns an empty list if no hospitals are found.
    #     """
    #     location = location.lower()
    #     return [
    #         h["adi"] for h in self.mock_data["hastaneler"]
    #         if h["konum_il"].lower() == location or h["konum_ilce"].lower() == location
    #     ]


    def get_policlinics_by_hospital_name(self, hospital_name: str) -> list[str]:
        """
        Belirli bir hastanede bulunan tüm benzersiz polikliniklerin listesini alır.

        Args:
            hospital_name (str): Aranacak hastanenin tam adı.
        Returns:
            list: Benzersiz poliklinik adlarının listesi (örneğin, ['KBB', 'Kardiyoloji']).
                Hastane bulunamazsa veya doktoru yoksa boş bir liste döndürür.
        """
        hospital_id = None
        for h in self.mock_data["hastaneler"]:
            if h["adi"].lower() == hospital_name.lower():
                hospital_id = h["id"]
                break

        if not hospital_id:
            return []

        policlinics = {
            d["uzmanlik"] 
            for d in self.mock_data["doktorlar"]
            if d["hastane_id"] == hospital_id
        }

        return sorted(list(policlinics))


    def get_doctors_by_hospital_and_policlinic(self, hospital_name: str, policlinic: str) -> list:
        """
        Belirli bir hastane ve poliklinikte çalışan doktorları listeler.

        Bu fonksiyon önce hastanenin ID'sini bulur ve ardından doktor listesini hem hastane ID'sine hem de poliklinik adına göre filtreler.

        Args:
            hospital_name (str): Hastanenin tüm adı (e.g., 'Ankara Şehir Hastanesi').
            policlinic (str): Polikliniğin tam adı (e.g., 'KBB', 'Kardiyoloji').

        Returns:
            list: Kriterlere uyan doktor isimlerinin listesi.
                Hastane veya doktorlar bulunamazsa boş bir liste döndürür.
        """
        policlinic_map = {
            "kulak burun boğaz": "KBB",
            "kbb": "KBB",
            "kardiyoloji": "Kardiyoloji",
            "nöroloji": "Nöroloji",
            "dermatoloji": "Dermatoloji",
            "gastroenteroloji": "Gastroenteroloji",
            "plastik cerrahi": "Plastik Cerrahi",
            "ortopedi": "Ortopedi"
        }
        
        # Gelen poliklinik adını eşleme sözlüğünde ara
        mapped_policlinic = policlinic_map.get(policlinic.lower(), policlinic)

        hospital_id = None
        for h in self.mock_data["hastaneler"]:
            if h["adi"].lower() == hospital_name.lower():
                hospital_id = h["id"]
                break
        
        if not hospital_id:
            return []
            
        doctors_in_policlinic = [
            d for d in self.mock_data["doktorlar"]
            if d["uzmanlik"].lower() == mapped_policlinic.lower() and d["hastane_id"] == hospital_id
        ]

        doctors = [d["adi"] for d in doctors_in_policlinic]

        return doctors


    def get_available_dates_for_doctor(self, doctor_name: str) -> list:
        """
        Belirli bir doktor için müsait randevu tarihlerinin listesini alır.

        Bu fonksiyon, verilen `doctor_name` için bir eşleşme bulmak üzere doktorların sahte verilerini yineler. 
        Doktor bulunduğunda, doktorun `musaitlik` (müsaitlik) sözlüğünden müsait tarihleri temsil eden anahtarları çıkarır. 
        Fonksiyon, doktorun adı için büyük/küçük harfe duyarlı değildir. Eşleşen bir doktor bulunamazsa, boş bir liste döndürür.

        Args:
            doctor_name (str): Müsaitlik tarihleri alınacak doktorun tam adı.
                        Arama büyük/küçük harfe duyarlı değildir.
        Returns:
            list: Her dizenin 'YYYY-AA-GG' biçiminde müsait bir tarih olduğu dizelerden oluşan bir liste (örneğin, ['2025-08-15', '2025-08-16']).
                Eşleşen bir doktor bulunamazsa boş bir liste döndürür.
        """
        for doktor in self.mock_data["doktorlar"]:
            if doktor["adi"].lower() == doctor_name.lower():
                # 'musaitlik' sözlüğünün anahtarları müsait tarihleri temsil eder.
                return list(doktor["musaitlik"].keys())
        return []


    def get_available_appointments(self, doctor_name: str, date: str) -> list:
        """
        Belirli bir tarihte bir doktor için müsait randevu aralıklarını bulur ve döndürür.

        Doktorun genel müsaitliğini kontrol eder ve önceden rezerve edilmiş randevuları kaldırır.

        Args:
            doctor_name (str): Doktorun tam adı.
            date (str): The date to check, in 'YYYY-MM-DD' format.

        Returns:
            list: Uygun zamanların listesi ('HH:MM'). eğer hiçbir doktor/tarih müsait değilse boş liste dön.
        """
        for doktor in self.mock_data["doktorlar"]:
            if doktor["adi"].lower() == doctor_name.lower():
                original_times = doktor["musaitlik"].get(date, [])
                
                booked_times = {
                    r["saat"] for r in self.mock_data["randevular"]
                    if r["doktor"].lower() == doctor_name.lower() and r["tarih"] == date
                }
                
                available_times = [
                    time for time in original_times if time not in booked_times
                ]
                
                return available_times
        return []

    def book_appointment(self, doctor_name: str, date: str, time: str) -> str:
        """
        Belirli bir tarih ve saat için bir doktorla yeni bir randevu oluşturur.

        Bu işlev, yeni randevuyu oluşturmadan önce istenen zaman aralığının müsait olup olmadığını 
        ve daha önce rezerve edilip edilmediğini doğrular.

        Args:
            doctor_name (str):Doktorun tüm adı.
            date (str): 'YYYY-MM-DD' formatında randevu tarihi.
            time (str): 'HH:MM' formatında saat tarihi.

        Returns:
            str: Rezervasyon durumunu ('success' or 'error')
                    belirten bir JSON dizesi ve sonucu açıklayan bir mesaj.
        """
        is_booked = any(
            r["doktor"].lower() == doctor_name.lower() and
            r["tarih"] == date and
            r["saat"] == time
            for r in self.mock_data["randevular"]
        )

        if is_booked:
            return json.dumps({"status": "error", "message": "Bu randevu saati zaten dolu."})
        
        available_times = self.get_available_appointments(doctor_name, date)
        if time not in available_times:
            return json.dumps({"status": "error", "message": "Belirtilen saat müsait değil veya geçersiz."})

        # Find doctor details to get hospital_id and policlinic
        doctor_info = None
        for doc in self.mock_data["doktorlar"]:
            if doc["adi"].lower() == doctor_name.lower():
                doctor_info = doc
                break

        if not doctor_info:
            return json.dumps({"status": "error", "message": "Doktor bilgisi bulunamadı."})

        # Find hospital details using hospital_id
        hospital_info = None
        for hosp in self.mock_data["hastaneler"]:
            if hosp["id"] == doctor_info["hastane_id"]:
                hospital_info = hosp
                break
        
        if not hospital_info:
            return json.dumps({"status": "error", "message": "Hastane bilgisi bulunamadı."})

        randevu_bilgisi = {
            "doktor": doctor_name,
            "tarih": date,
            "saat": time,
            "hastane_adi": hospital_info["adi"],
            "hastane_il": hospital_info["konum_il"],
            "hastane_ilce": hospital_info["konum_ilce"],
            "poliklinik": doctor_info["uzmanlik"]
        }
        self.mock_data["randevular"].append(randevu_bilgisi)
        return json.dumps({"status": "success", "message": "Randevunuz başarıyla oluşturuldu.", "randevu": randevu_bilgisi})


    def delete_appointment(self, doctor_name: str, hospital_name: str, policlinic: str, date: str, time: str) -> str:
        """
        Tam eşleşme için tüm ayrıntıları kullanarak, mevcut bir randevuyu sahte verilerden siler.

        Args:
            Doktorun tam adı.
            hastane_adı (dize): Hastanenin adı.
            poliklinik (dize): Polikliniğin adı.
            tarih (dize): Randevunun tarihi 'YYYY-AA-GG' biçiminde.
            saat (dize): Randevunun saati 'SS:DD' biçiminde.

        Returns:
            str:Durumu ('başarılı' veya 'hata') ve bir mesajı gösteren bir JSON dizesi.
        """
        
        # Filter out the appointment that matches all the provided details
        appointment_list_before_deletion = len(self.mock_data["randevular"])
        self.mock_data["randevular"] = [
            r for r in self.mock_data["randevular"]
            if not (r["doktor"].lower() == doctor_name.lower() and
                    r["hastane_adi"].lower() == hospital_name.lower() and
                    r["poliklinik"].lower() == policlinic.lower() and
                    r["tarih"] == date and
                    r["saat"] == time)
        ]
        
        if len(self.mock_data["randevular"]) < appointment_list_before_deletion:
            return json.dumps({"status": "success", "message": "Randevunuz başarıyla silindi."})
        else:
            return json.dumps({"status": "error", "message": "Belirtilen randevu bulunamadı veya randevu silinemedi."})
        


    def get_my_appointments(self) -> list:
        """
        Kullanıcı için hazır bulunan rezerve edilmiş tüm randevuları alır ve biçimlendirir.

        Bu işlev, başarıyla rezerve edilmiş tüm randevuları almak için dahili sahte verilerin "randevular" listesine erişir. 
        Her randevu, sonraki işlemler için çok önemli olan benzersiz bir sayısal kimlikle zenginleştirilir (`cancel_appointment_by_id` kullanılarak).

        Returns:
            list: Her sözlüğün rezerve edilmiş bir randevuyu temsil ettiği ve 'id', 'doctor_name' (doktor adı),
                'hastane_adi' (hastane adı),
                'poliklinik' (poliklinik),
                'tarih' (tarih) ve
                'saat' (saat) değerlerini içerdiği bir sözlük listesi. Randevu bulunamazsa boş bir liste döndürür.
        """
        formatted_appointments = []
        for i, appt in enumerate(self.mock_data["randevular"]):
            formatted_appointments.append({
                "id": i,
                "doktor": appt["doktor"],
                "hastane_adi": appt["hastane_adi"],
                "poliklinik": appt["poliklinik"],
                "tarih": appt["tarih"],
                "saat": appt["saat"]
            })
        return formatted_appointments


    def cancel_appointment_by_id(self, appointment_id: int) -> str:
        """
        Benzersiz tanımlayıcısını (ID) kullanarak rezerve edilmiş bir randevuyu iptal eder.
        
        Args:
            appointment_id (int): iptal edilecek randevunun benzersiz ID'si.
        
        Returns:
            str: Durumu ('başarılı' veya 'hata') ve bir mesajı gösteren JSON dizesi.
        """
        # mock_data'daki "randevular" listesini güncelleyerek randevuyu sil
        if 0 <= appointment_id < len(self.mock_data["randevular"]):
            del self.mock_data["randevular"][appointment_id]
            return json.dumps({"status": "success", "message": "Randevunuz başarıyla iptal edildi."})
        else:
            return json.dumps({"status": "error", "message": "Geçersiz randevu ID'si."})