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
current_patient_id = "123456789"
test_doctor_id = "101"
test_date = "2025-08-10"

print("\n--- TEST 1: Mock Doctor List ---")
docs = service.get_doctors_by_hospital_and_branch("1", "Kardiyoloji")
print(f"Retrieved Doctors: {docs}")

print("\n--- TEST 2: Successful Appointment Creation ---")
try:
    app1 = service.create_appointment(test_doctor_id, current_patient_id, test_date, "09:00")
    logger.info(f"Appointment Created. ID: {app1.id}")
except Exception as e:
    logger.error(f"Test 2 Error: {e}")

print("\n--- TEST 3: Successful Update (Time Change) ---")
if app1:
    try:
        new_app1 = service.update_appointment(app1.id, new_time_str="10:30")
        logger.info(f"Appointment Updated. New ID: {new_app1.id}")
        logger.info(f"New Appointment Time: {new_app1.start_time}")
    except Exception as e:
        logger.error(f"Test 3 Error: {e}")
else:
    logger.error("⚠️ Test 3 could not run because Test 2 failed.")

print("\n--- TEST 4: Appointment Cancellation (Soft Delete) Process ---")
app_to_cancel = locals().get('new_app1') if locals().get('new_app1') else app1

if app_to_cancel:
    try:
        logger.info(f"Appointment ID to Cancel: {app_to_cancel.id}")

        cancel_response = service.cancel_appointment(app_to_cancel.id)
        logger.info(f"Operation Result: {cancel_response}")

        cancelled_app = service.appointments_by_id.get(app_to_cancel.id)

        if cancelled_app is not None and cancelled_app.status.name == "CANCELLED":
            logger.info("✅ VERIFICATION SUCCESSFUL: Appointment exists and status is 'CANCELLED'.")
        else:
            current_status = cancelled_app.status.name if cancelled_app else "NONE"
            logger.error(f"❌ ERROR: Expected status CANCELLED, Current status: {current_status}")

    except Exception as e:
        logger.error(f"Test 4 Error: {e}")
else:
    logger.error("⚠️ No valid appointment object found for cancellation test.")

print("\n--- TEST 5: Retrieve Available Hospitals (get_available_hospitals) ---")
try:
    hospitals = service.get_available_hospitals(city="Yozgat", district="Sorgun")

    for h in hospitals:
        print(f"Hospital: {h['name']} (ID: {h['id']})")

    if len(hospitals) > 0:
        logger.info("✅ Hospital list successfully retrieved.")
except Exception as e:
    logger.error(f"Test 5 Error: {e}")

print("\n--- TEST 6: Availability Check (get_available_slots) ---")
try:
    logger.info(f"Searching for slots for Dr. {test_doctor_id} on {test_date}...")

    slots_result = service.get_available_slots(
        doctor_id=test_doctor_id,
        date_str=test_date
    )

    found_1030 = False
    if slots_result:
        doctor_schedule = slots_result[0]["schedule"]
        for day_schedule in doctor_schedule:
            if day_schedule["date"] == test_date:
                print(f"Available Hours: {day_schedule['slots']}")
                if "10:30" in day_schedule['slots']:
                    found_1030 = True

    if found_1030:
        logger.info("✅ SUCCESS: The cancelled 10:30 slot is listed as available again.")
    else:
        logger.warning("⚠️ WARNING: 10:30 slot does not appear in available list! (Check Mock data config)")

except Exception as e:
    logger.error(f"Test 6 Error: {e}")

print("\n--- TEST 7: Retrieve Patient Appointments (get_patient_appointments) ---")
try:
    my_appointments = service.get_patient_appointments(current_patient_id)
    print(f"Patient ({current_patient_id}) Appointments: {len(my_appointments)} found.")

    for app in my_appointments:
        print(f"   - {app['date']} {app['time']} | Dr. {app['doctor']} | Status: {app['status']}")

    if app_to_cancel:
        found_app = next((a for a in my_appointments if a['appointment_id'] == app_to_cancel.id), None)

        if found_app:
            status_text = str(found_app['status']).upper()

            if "CANCELLED" in status_text or "İPTAL" in status_text:
                logger.info(f"✅ VERIFICATION SUCCESSFUL: Appointment remains in list and status is '{found_app['status']}'.")
            else:
                logger.error(f"❌ ERROR: Appointment found but status not updated! Status: {found_app['status']}")
        else:
            logger.error("❌ ERROR: Appointment not found in list at all! (Soft delete should not remove data)")

except Exception as e:
    logger.error(f"Test 7 Error: {e}")