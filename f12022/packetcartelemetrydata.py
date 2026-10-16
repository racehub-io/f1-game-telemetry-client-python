import ctypes
from .packetheader import PacketHeader


class CarTelemetryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_speed", ctypes.c_uint16),
        ("m_throttle", ctypes.c_float),
        ("m_steer", ctypes.c_float),
        ("m_brake", ctypes.c_float),
        ("m_clutch", ctypes.c_uint8),
        ("m_gear", ctypes.c_int8),
        ("m_engineRPM", ctypes.c_uint16),
        ("m_drs", ctypes.c_uint8),
        ("m_revLightsPercent", ctypes.c_uint8),
        ("m_revLightBitValue", ctypes.c_uint16),
        ("m_brakesTemperatureRL", ctypes.c_uint16),
        ("m_brakesTemperatureRR", ctypes.c_uint16),
        ("m_brakesTemperatureFL", ctypes.c_uint16),
        ("m_brakesTemperatureFR", ctypes.c_uint16),
        ("m_tyresSurfaceTemperatureRL", ctypes.c_uint8),
        ("m_tyresSurfaceTemperatureRR", ctypes.c_uint8),
        ("m_tyresSurfaceTemperatureFL", ctypes.c_uint8),
        ("m_tyresSurfaceTemperatureFR", ctypes.c_uint8),
        ("m_tyresInnerTemperatureRL", ctypes.c_uint8),
        ("m_tyresInnerTemperatureRR", ctypes.c_uint8),
        ("m_tyresInnerTemperatureFL", ctypes.c_uint8),
        ("m_tyresInnerTemperatureFR", ctypes.c_uint8),
        ("m_engineTemperature", ctypes.c_uint16),
        ("m_tyresPressureRL", ctypes.c_float),
        ("m_tyresPressureRR", ctypes.c_float),
        ("m_tyresPressureFL", ctypes.c_float),
        ("m_tyresPressureFR", ctypes.c_float),
        ("m_surfaceTypeRL", ctypes.c_uint8),
        ("m_surfaceTypeRR", ctypes.c_uint8),
        ("m_surfaceTypeFL", ctypes.c_uint8),
        ("m_surfaceTypeFR", ctypes.c_uint8),
    ]

    def to_dict(self):
        return {
            field_name: getattr(self, field_name) for field_name, _ in self._fields_
        }


class PacketCarTelemetryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_carTelemetryData", CarTelemetryData * 22),
    ]

    def to_dict(self):
        result = {
            field_name: getattr(self, field_name).to_dict()
            if isinstance(getattr(self, field_name), ctypes.Structure)
            else getattr(self, field_name)
            for field_name, field_type in self._fields_
            if field_name != "m_carTelemetryData"
        }
        result["m_carTelemetryData"] = [
            self.m_carTelemetryData[i].to_dict() for i in range(22)
        ]
        return result

    def flatten(self, car_index):
        packet_dict = self.to_dict()

        # Flatten the header fields
        header_fields = {"m_header_" + k: v for k, v in packet_dict["m_header"].items()}
        del packet_dict["m_header"]

        # Extract car data and other fields
        other_fields = {
            k: v for k, v in packet_dict.items() if k != "m_carTelemetryData"
        }

        # Flatten the car array data fields
        car_array_fields = {
            "m_carTelemetryData_" + k: v
            for k, v in packet_dict["m_carTelemetryData"][car_index].items()
        }

        return {**header_fields, **other_fields, **car_array_fields}
