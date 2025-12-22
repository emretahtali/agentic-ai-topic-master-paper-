import logging
from appointment.appointment_manager import AppointmentManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("AppointmentSystem")

service = AppointmentManager()

app1 = None
current_patient_id = "patient_1"
test_doctor_id = "101"
test_date = "2025-08-10"

print("\n--- TEST 1: Mock Doktor Listesi ---")
docs = service.get_doctors_by_hospital_and_branch("1", "Kardiyoloji")
print(f"Gelen Doktorlar: {docs}")

print("\n--- TEST 2: Başarılı Randevu Oluşturma ---")
try:
    app1 = service.create_appointment(test_doctor_id, current_patient_id, test_date, "09:00")
    logger.info(f"Randevu Oluşturuldu. ID: {app1.id}")
except Exception as e:
    logger.error(f"Test 2 Hata: {e}")

print("\n--- TEST 3: Başarılı Güncelleme (Saat Değişimi) ---")
if app1:
    try:
        new_app1 = service.update_appointment(app1.id, new_time_str="10:30")
        logger.info(f"Randevu Güncellendi. Yeni ID: {new_app1.id}")
        logger.info(f"Yeni Randevu Zamanı: {new_app1.start_time}")
    except Exception as e:
        logger.error(f"Test 3 Hata: {e}")
else:
    logger.error("⚠️ Test 2 başarısız olduğu için Test 3 çalıştırılamadı.")

print("\n--- TEST 4: Randevu İptal (Soft Delte) İşlemi ---")
app_to_cancel = locals().get('new_app1') if locals().get('new_app1') else app1

if app_to_cancel:
    try:
        logger.info(f"İptal edilecek Randevu ID: {app_to_cancel.id}")

        cancel_response = service.cancel_appointment(app_to_cancel.id)
        logger.info(f"İşlem Sonucu: {cancel_response}")

        cancelled_app = service.appointments_by_id.get(app_to_cancel.id)

        if cancelled_app is not None and cancelled_app.status.name == "CANCELLED":
            logger.info("✅ DOĞRULAMA BAŞARILI: Randevu duruyor ve statüsü 'CANCELLED' oldu.")
        else:
            current_status = cancelled_app.status.name if cancelled_app else "YOK"
            logger.error(f"❌ HATA: Beklenen durum CANCELLED, Mevcut durum: {current_status}")

    except Exception as e:
        logger.error(f"Test 4 Hata: {e}")
else:
    logger.error("⚠️ İptal testi için geçerli bir randevu nesnesi bulunamadı.")

print("\n--- TEST 5: Mevcut Hastaneleri Getirme (get_available_hospitals) ---")
try:
    hospitals = service.get_available_hospitals(city="Yozgat", district="Sorgun")

    for h in hospitals:

        print(f"Hastane: {h['name']} (ID: {h['id']})")

    if len(hospitals) > 0:
        logger.info("✅ Hastane listesi başarıyla çekildi.")
except Exception as e:
    logger.error(f"Test 5 Hata: {e}")

print("\n--- TEST 6: Uygunluk Kontrolü (get_available_slots) ---")
try:
    logger.info(f"Dr. {test_doctor_id} için {test_date} tarihindeki boşluklar aranıyor...")

    slots_result = service.get_available_slots(
        doctor_id=test_doctor_id,
        date_str=test_date
    )

    found_1030 = False
    if slots_result:
        doctor_schedule = slots_result[0]["schedule"]
        for day_schedule in doctor_schedule:
            if day_schedule["date"] == test_date:
                print(f"Müsait Saatler: {day_schedule['slots']}")
                if "10:30" in day_schedule['slots']:
                    found_1030 = True

    if found_1030:
        logger.info("✅ BAŞARILI: İptal edilen 10:30 saati tekrar müsait olarak listelendi.")
    else:
        logger.warning("⚠️ UYARI: 10:30 saati müsait listesinde görünmüyor! (Mock data config'ine bakılmalı)")

except Exception as e:
    logger.error(f"Test 6 Hata: {e}")

print("\n--- TEST 7: Hasta Randevularını Getirme (get_patient_appointments) ---")
try:
    my_appointments = service.get_patient_appointments(current_patient_id)
    print(f"Hasta ({current_patient_id}) Randevuları: {len(my_appointments)} adet bulundu.")

    for app in my_appointments:
        print(f"   - {app['date']} {app['time']} | Dr. {app['doctor']} | Durum: {app['status']}")

    if app_to_cancel:
        found_app = next((a for a in my_appointments if a['appointment_id'] == app_to_cancel.id), None)

        if found_app:
            status_text = str(found_app['status']).upper()

            if "CANCELLED" in status_text or "İPTAL" in status_text:
                logger.info(f"✅ DOĞRULAMA BAŞARILI: Randevu listede duruyor ve statüsü '{found_app['status']}' olmuş.")
            else:
                logger.error(f"❌ HATA: Randevu bulundu ama statüsü güncellenmemiş! Durum: {found_app['status']}")
        else:
            logger.error("❌ HATA: Randevu listede hiç bulunamadı! (Soft delete veriyi silmemeliydi)")

except Exception as e:
    logger.error(f"Test 7 Hata: {e}")