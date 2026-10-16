import ctypes
from .packetheader import PacketHeader


class CarSetupData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_frontWing", ctypes.c_uint8),
        ("m_rearWing", ctypes.c_uint8),
        ("m_onThrottle", ctypes.c_uint8),
        ("m_offThrottle", ctypes.c_uint8),
        ("m_frontCamber", ctypes.c_float),
        ("m_rearCamber", ctypes.c_float),
        ("m_frontToe", ctypes.c_float),
        ("m_rearToe", ctypes.c_float),
        ("m_frontSuspension", ctypes.c_uint8),
        ("m_rearSuspension", ctypes.c_uint8),
        ("m_frontAntiRollBar", ctypes.c_uint8),
        ("m_rearAntiRollBar", ctypes.c_uint8),
        ("m_frontSuspensionHeight", ctypes.c_uint8),
        ("m_rearSuspensionHeight", ctypes.c_uint8),
        ("m_brakePressure", ctypes.c_uint8),
        ("m_brakeBias", ctypes.c_uint8),
        ("m_rearLeftTyrePressure", ctypes.c_float),
        ("m_rearRightTyrePressure", ctypes.c_float),
        ("m_frontLeftTyrePressure", ctypes.c_float),
        ("m_frontRightTyrePressure", ctypes.c_float),
        ("m_ballast", ctypes.c_uint8),
        ("m_fuelLoad", ctypes.c_float),
    ]

    def to_dict(self):
        return {
            field_name: getattr(self, field_name) for field_name, _ in self._fields_
        }


class PacketCarSetupData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("m_header", PacketHeader), ("m_carSetupData", CarSetupData * 22)]

    def to_dict(self):
        result = {
            field_name: getattr(self, field_name).to_dict()
            if isinstance(getattr(self, field_name), ctypes.Structure)
            else getattr(self, field_name)
            for field_name, field_type in self._fields_
            if field_name != "m_carSetupData"
        }
        result["m_carSetupData"] = [self.m_carSetupData[i].to_dict() for i in range(22)]
        return result

    def flatten(self, car_index):
        packet_dict = self.to_dict()

        # Flatten the header fields
        header_fields = {"m_header_" + k: v for k, v in packet_dict["m_header"].items()}
        del packet_dict["m_header"]

        # Extract car data and other fields
        other_fields = {k: v for k, v in packet_dict.items() if k != "m_carSetupData"}

        # Flatten the car array data fields
        car_array_fields = {
            "m_carSetupData_" + k: v
            for k, v in packet_dict["m_carSetupData"][car_index].items()
        }

        return {**header_fields, **other_fields, **car_array_fields}
