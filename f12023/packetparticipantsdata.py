import ctypes
from .packetheader import PacketHeader


class ParticipantsData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_aiControlled", ctypes.c_uint8),
        ("m_driverId", ctypes.c_uint8),
        ("m_networkId", ctypes.c_uint8),
        ("m_teamId", ctypes.c_uint8),
        ("m_myTeam", ctypes.c_uint8),
        ("m_raceNumber", ctypes.c_uint8),
        ("m_nationality", ctypes.c_uint8),
        ("m_name", ctypes.c_char * 48),
        ("m_yourTelemetry", ctypes.c_uint8),
        ("m_showOnlineNames", ctypes.c_uint8),
        ("m_platform", ctypes.c_uint8),
    ]

    def to_dict(self):
        return {
            field_name: getattr(self, field_name) for field_name, _ in self._fields_
        }


class PacketParticipantsData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_numActiveCars", ctypes.c_uint8),
        ("m_participantsData", ParticipantsData * 22),
    ]

    def to_dict(self):
        result = {
            field_name: getattr(self, field_name).to_dict()
            if isinstance(getattr(self, field_name), ctypes.Structure)
            else getattr(self, field_name)
            for field_name, field_type in self._fields_
            if field_name != "m_participantsData"
        }
        result["m_participantsData"] = [
            self.m_participantsData[i].to_dict() for i in range(22)
        ]
        return result

    def flatten(self, car_index):
        packet_dict = self.to_dict()

        # Flatten the header fields
        header_fields = {"m_header_" + k: v for k, v in packet_dict["m_header"].items()}
        del packet_dict["m_header"]

        # Extract car data and other fields
        other_fields = {
            k: v for k, v in packet_dict.items() if k != "m_participantsData"
        }

        # Flatten the car array data fields
        car_array_fields = {
            "m_participantsData_" + k: v
            for k, v in packet_dict["m_participantsData"][car_index].items()
        }

        return {**header_fields, **other_fields, **car_array_fields}
