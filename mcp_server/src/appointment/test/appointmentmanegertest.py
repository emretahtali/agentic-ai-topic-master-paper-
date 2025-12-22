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

print("\n--- TEST 1: Mock Doktor Listesi ---")
docs = service.get_doctors_by_hospital_and_branch("1", "Kardiyoloji")
print(f"Gelen Doktorlar: {docs}")

print("\n--- TEST 2: Başarılı Randevu Oluşturma ---")
try:
    app1 = service.create_appointment("101", "patient_1", "2025-08-10", "09:00")
except Exception as e:
    logger.error(f"Test 2 Hata: {e}")


print("\n--- TEST 3: Başarılı Güncelleme (Saat Değişimi) ---")
if app1:
    try:
        new_app1 = service.update_appointment(app1.id, new_time_str="10:30")

        original_app = service.appointments_by_id[app1.id]
        logger.info(f"Eski Randevu Durumu: {original_app.status.value}")  # CANCELLED / İPTAL
        logger.info(f"Yeni Randevu Zamanı: {new_app1.start_time}")
    except Exception as e:
        logger.error(f"Test 4 Hata: {e}")
else:
    logger.error("⚠️ Test 2 başarısız olduğu için Test 4 çalıştırılamadı (app1 yok).")


print("\n--- TEST 4: Randevu İptal İşlemi ---")
app_to_cancel = locals().get('new_app1') if locals().get('new_app1') else app1

if app_to_cancel:
    try:
        logger.info(f"İptal edilecek Randevu ID: {app_to_cancel.id}")

        cancel_response = service.cancel_appointment(app_to_cancel.id)
        logger.info(f"İşlem Sonucu: {cancel_response}")

        cancelled_app_ref = service.appointments_by_id[app_to_cancel.id]
        logger.info(f"Veri Tabanı Durum Kontrolü: {cancelled_app_ref.status.value}")

    except Exception as e:
        logger.error(f"Test 5 Hata: {e}")

else:
    logger.error("⚠️ İptal testi için geçerli bir randevu nesnesi bulunamadı (Önceki testler başarısız).")


