from enum import StrEnum
from typing import Any, Optional, TypedDict
from typing_extensions import Literal


# Slots
class SlotStatus(StrEnum):
    EMPTY = "empty"
    FILLED = "filled"
    INVALID = "invalid"

class SlotSource(StrEnum):
    USER = "user"
    INFERRED = "inferred"
    SYSTEM = "system"


# State
StepName = Literal[
    "tc_kimlik", "sehir", "ilce", "hastane",
    "poliklinik", "doktor", "tarih", "saat", "onay"
]

class SlotDetail(TypedDict):
    value: Optional[Any]
    status: SlotStatus
    source: Optional[SlotSource]

class Slots(TypedDict):
    tc_kimlik: SlotDetail
    sehir: SlotDetail
    ilce: SlotDetail
    hastane: SlotDetail
    poliklinik: SlotDetail
    doktor: SlotDetail
    tarih: SlotDetail
    saat: SlotDetail
    onay: SlotDetail

class FlowDetail(TypedDict):
    current_step: StepName
    steps: list[StepName]
    completed: bool

class MemoryDetail(TypedDict, total=False):
    pending_slots: dict[StepName, Any]
    preferences: dict[str, Any]

class AppointmentState(TypedDict):
    slots: Slots
    flow: FlowDetail
    memory: MemoryDetail


