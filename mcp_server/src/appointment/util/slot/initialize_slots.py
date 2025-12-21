from appointment.util.slot import AppointmentState, SlotDetail, SlotStatus


def create_initial_appointment_state() -> AppointmentState:
    def empty_slot() -> SlotDetail:
        return {"value": None, "status": SlotStatus.EMPTY, "source": None}

    steps = ["tc_kimlik", "sehir", "ilce", "hastane", "poliklinik", "doktor", "tarih", "saat", "onay"]
    return {
        "slots": {step: empty_slot() for step in steps},
        "flow": {
            "current_step": "tc_kimlik",
            "steps": steps,
            "completed": False,
        },
        "memory": {"pending_slots": {}, "preferences": {}},
    }