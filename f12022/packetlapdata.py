import ctypes
from .packetheader import PacketHeader


class LapData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_lastLapTimeInMS", ctypes.c_uint32),
        ("m_currentLapTimeInMS", ctypes.c_uint32),
        ("m_sector1TimeinMS", ctypes.c_uint16),
        ("m_sector2TimeinMS", ctypes.c_uint16),
        ("m_lapDistance", ctypes.c_float),
        ("m_totalDistance", ctypes.c_float),
        ("m_safetyCarDelta", ctypes.c_float),
        ("m_carPosition", ctypes.c_uint8),
        ("m_currentLapNum", ctypes.c_uint8),
        ("m_pitStatus", ctypes.c_uint8),
        ("m_numPitStops", ctypes.c_uint8),
        ("m_sector", ctypes.c_uint8),
        ("m_currentLapInvalid", ctypes.c_uint8),
        ("m_penalties", ctypes.c_uint8),
        ("m_warnings", ctypes.c_uint8),
        ("m_numUnservedDriveThroughPens", ctypes.c_uint8),
        ("m_numUnservedStopGoPens", ctypes.c_uint8),
        ("m_gridPosition", ctypes.c_uint8),
        ("m_driverStatus", ctypes.c_uint8),
        ("m_resultStatus", ctypes.c_uint8),
        ("m_pitLaneTimerActive", ctypes.c_uint8),
        ("m_pitLaneTimeInLaneInMS", ctypes.c_uint16),
        ("m_pitStopTimerInMS", ctypes.c_uint16),
        ("m_pitStopShouldServePen", ctypes.c_uint8),
    ]

    def to_dict(self):
        return {
            field_name: getattr(self, field_name) for field_name, _ in self._fields_
        }


class PacketLapData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_lapData", LapData * 22),
        ("m_timeTrialPBCarIdx", ctypes.c_uint8),
        ("m_timeTrialRivalCarIdx", ctypes.c_uint8),
    ]

    def to_dict(self):
        result = {
            field_name: getattr(self, field_name).to_dict()
            if isinstance(getattr(self, field_name), ctypes.Structure)
            else getattr(self, field_name)
            for field_name, field_type in self._fields_
            if field_name != "m_lapData"
        }
        result["m_lapData"] = [self.m_lapData[i].to_dict() for i in range(22)]
        return result

    def flatten(self, car_index):
        packet_dict = self.to_dict()

        # Flatten the header fields
        header_fields = {"m_header_" + k: v for k, v in packet_dict["m_header"].items()}
        del packet_dict["m_header"]

        # Extract car data and other fields
        other_fields = {k: v for k, v in packet_dict.items() if k != "m_lapData"}

        # Flatten the car array data fields
        car_array_fields = {
            "m_lapData_" + k: v for k, v in packet_dict["m_lapData"][car_index].items()
        }

        return {**header_fields, **other_fields, **car_array_fields}
