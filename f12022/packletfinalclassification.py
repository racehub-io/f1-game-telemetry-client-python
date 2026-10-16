import ctypes

from .packetheader import PacketHeader


class FinalClassificationData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_position", ctypes.c_uint8),
        ("m_numLaps", ctypes.c_uint8),
        ("m_gridPosition", ctypes.c_uint8),
        ("m_points", ctypes.c_uint8),
        ("m_numPitStops", ctypes.c_uint8),
        ("m_resultStatus", ctypes.c_uint8),
        ("m_bestLapTimeInMS", ctypes.c_uint32),
        ("m_totalRaceTime", ctypes.c_double),
        ("m_penaltiesTime", ctypes.c_uint8),
        ("m_numPenalties", ctypes.c_uint8),
        ("m_numTyreStints", ctypes.c_uint8),
        ("m_tyreStintsActual", ctypes.c_uint8 * 8),
        ("m_tyreStintsVisual", ctypes.c_uint8 * 8),
        ("m_tyreStintsEndLaps", ctypes.c_uint8 * 8),
    ]

    def to_dict(self):
        return {
            field_name: list(getattr(self, field_name))
            if field_name
            in ["m_tyreStintsActual", "m_tyreStintsVisual", "m_tyreStintsEndLaps"]
            else getattr(self, field_name)
            for field_name, field_type in self._fields_
        }


class PacketFinalClassificationData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_numCars", ctypes.c_uint8),
        ("m_classificationData", FinalClassificationData * 22),
    ]

    def to_dict(self):
        return {
            field_name: [car.to_dict() for car in getattr(self, field_name)]
            if field_name == "m_classificationData"
            else getattr(self, field_name).to_dict()
            if isinstance(getattr(self, field_name), ctypes.Structure)
            else getattr(self, field_name)
            for field_name, field_type in self._fields_
        }

    def flatten(self, car_index):
        packet_dict = self.to_dict()

        # Flatten the header fields
        header_fields = {"m_header_" + k: v for k, v in packet_dict["m_header"].items()}
        del packet_dict["m_header"]

        # Extract car data and other fields
        other_fields = {
            k: v for k, v in packet_dict.items() if k != "m_classificationData"
        }

        # Flatten the car array data fields
        car_array_fields = {
            "m_classificationData_" + k: v
            for k, v in packet_dict["m_classificationData"][car_index].items()
        }

        return {**header_fields, **other_fields, **car_array_fields}
