import ctypes

from .packetheader import PacketHeader

NUM_HISTORIC_LAPS = 100
NUM_TYRE_STINTS = 8


class LapHistoryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_lapTimeInMS", ctypes.c_uint32),
        ("m_sector1TimeInMS", ctypes.c_uint16),
        ("m_sector1TimeInMinutes", ctypes.c_uint8),
        ("m_sector2TimeInMS", ctypes.c_uint16),
        ("m_sector2TimeInMinutes", ctypes.c_uint8),
        ("m_sector3TimeInMS", ctypes.c_uint16),
        ("m_sector3TimeInMinutes", ctypes.c_uint8),
        ("m_lapValidBitFlags", ctypes.c_uint8),
    ]

    def to_dict(self):
        return {
            field_name: getattr(self, field_name) for field_name, _ in self._fields_
        }


class TyreStintHistoryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_endLap", ctypes.c_uint8),
        ("m_tyreActualCompound", ctypes.c_uint8),
        ("m_tyreVisualCompound", ctypes.c_uint8),
    ]

    def to_dict(self):
        return {
            field_name: getattr(self, field_name) for field_name, _ in self._fields_
        }


class PacketSessionHistoryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_carIdx", ctypes.c_uint8),
        ("m_numLaps", ctypes.c_uint8),
        ("m_numTyreStints", ctypes.c_uint8),
        ("m_bestLapTimeLapNum", ctypes.c_uint8),
        ("m_bestSector1LapNum", ctypes.c_uint8),
        ("m_bestSector2LapNum", ctypes.c_uint8),
        ("m_bestSector3LapNum", ctypes.c_uint8),
        ("m_lapHistoryData", LapHistoryData * NUM_HISTORIC_LAPS),
        ("m_tyreStintsHistoryData", TyreStintHistoryData * NUM_TYRE_STINTS),
    ]

    def to_dict(self):
        result = {
            field_name: [item.to_dict() for item in getattr(self, field_name)]
            if isinstance(getattr(self, field_name, None), ctypes.Array)
            else getattr(self, field_name).to_dict()
            if isinstance(getattr(self, field_name, None), ctypes.Structure)
            else getattr(self, field_name)
            for field_name, _ in self._fields_
        }
        return result

    def flatten(self, car_index):
        packet_dict = self.to_dict()

        if car_index != packet_dict["m_carIdx"]:
            return {}

        # Flatten the header fields
        header_fields = {"m_header_" + k: v for k, v in packet_dict["m_header"].items()}
        del packet_dict["m_header"]

        # Extract car data and other fields
        other_fields = {
            k: v
            for k, v in packet_dict.items()
            if k != "m_lapHistoryData" or k != "m_tyreStintsHistoryData"
        }

        # Flatten the m_lapHistoryData fields and include all laps
        lap_history = {
            "m_lapHistoryData_" + str(i) + "_" + k: v
            for i in range(NUM_HISTORIC_LAPS)
            for k, v in packet_dict["m_lapHistoryData"][i].items()
        }

        # Flatten the m_tyreStintsHistoryData fields and include all tyre stints
        tyre_stint_history = {
            "m_tyreStintsHistoryData_" + str(i) + "_" + k: v
            for i in range(NUM_TYRE_STINTS)
            for k, v in packet_dict["m_tyreStintsHistoryData"][i].items()
        }

        return {
            **header_fields,
            **other_fields,
            **lap_history,
            **tyre_stint_history,
        }
