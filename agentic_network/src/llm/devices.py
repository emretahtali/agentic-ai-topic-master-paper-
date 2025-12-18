from enum import Enum


class DeviceType(Enum):
    """
    Represents different device types for model loading.
    """
    CUDA = "cuda"  # NVIDIA GPUs
    MPS = "mps"  # Apple Silicon GPUs
    AUTO = "auto"  # Let Hugging Face determine the best device
    CPU = "cpu"  # CPU only
