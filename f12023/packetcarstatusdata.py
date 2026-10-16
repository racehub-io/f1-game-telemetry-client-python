import ctypes
from .packetheader import PacketHeader


class CarStatusData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_tractionControl", ctypes.c_uint8),
        ("m_antiLockBrakes", ctypes.c_uint8),
        ("m_fuelMix", ctypes.c_uint8),
        ("m_frontBrakeBias", ctypes.c_uint8),
        ("m_pitLimiterStatus", ctypes.c_uint8),
        ("m_fuelInTank", ctypes.c_float),
        ("m_fuelCapacity", ctypes.c_float),
        ("m_fuelRemainingLaps", ctypes.c_float),
        ("m_maxRPM", ctypes.c_uint16),
        ("m_idleRPM", ctypes.c_uint16),
        ("m_maxGears", ctypes.c_uint8),
        ("m_DRSAllowed", ctypes.c_uint8),
        ("m_DRSActivationDistance", ctypes.c_uint16),
        ("m_actualTyreCompound", ctypes.c_uint8),
        ("m_visualTyreCompound", ctypes.c_uint8),
        ("m_tyreAgeLaps", ctypes.c_uint8),
        ("m_vehicleFiaFlags", ctypes.c_int8),
        ("m_enginePowerICE", ctypes.c_float),
        ("m_enginePowerMGUK", ctypes.c_float),
        ("m_ersStoreEnergy", ctypes.c_float),
        ("m_ersDeployMode", ctypes.c_uint8),
        ("m_ersHarvestedThisLapMGUK", ctypes.c_float),
        ("m_ersHarvestedThisLapMGUH", ctypes.c_float),
        ("m_ersDeployedThisLap", ctypes.c_float),
        ("m_networkPaused", ctypes.c_uint8),
    ]

    def to_dict(self):
        return {
            field_name: getattr(self, field_name) for field_name, _ in self._fields_
        }


class PacketCarStatusData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_carStatusData", CarStatusData * 22),
    ]

    def to_dict(self):
        result = {
            field_name: getattr(self, field_name).to_dict()
            if isinstance(getattr(self, field_name), ctypes.Structure)
            else getattr(self, field_name)
            for field_name, field_type in self._fields_
            if field_name != "m_carStatusData"
        }
        result["m_carStatusData"] = [
            self.m_carStatusData[i].to_dict() for i in range(22)
        ]
        return result

    def flatten(self, car_index):
        packet_dict = self.to_dict()

        # Flatten the header fields
        header_fields = {"m_header_" + k: v for k, v in packet_dict["m_header"].items()}
        del packet_dict["m_header"]

        # Extract car data and other fields
        other_fields = {k: v for k, v in packet_dict.items() if k != "m_carStatusData"}

        # Flatten the car array data fields
        car_array_fields = {
            "m_carStatusData_" + k: v
            for k, v in packet_dict["m_carStatusData"][car_index].items()
        }

        return {**header_fields, **other_fields, **car_array_fields}
