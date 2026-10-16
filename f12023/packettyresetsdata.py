import ctypes

from .packetheader import PacketHeader


class TyreSetData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_actualTyreCompound", ctypes.c_uint8),
        ("m_visualTyreCompound", ctypes.c_uint8),
        ("m_wear", ctypes.c_uint8),
        ("m_available", ctypes.c_uint8),
        ("m_recommendedSession", ctypes.c_uint8),
        ("m_lifeSpan", ctypes.c_uint8),
        ("m_usableLife", ctypes.c_uint8),
        ("m_lapDeltaTime", ctypes.c_float),
        ("m_fitted", ctypes.c_uint8),
    ]

    def to_dict(self):
        result = {
            field_name: getattr(self, field_name) for field_name, _ in self._fields_
        }
        return result


class PacketTyreSetsData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_carIdx", ctypes.c_uint8),
        ("m_tyreSetData", TyreSetData * 20),  # 13 (dry) + 7 (wet)
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
        other_fields = {k: v for k, v in packet_dict.items() if k != "m_tyreSetData"}

        # Flatten the m_lapHistoryData fields and include all laps
        tyre_set_data = {
            "m_tyreSetData_" + str(i) + "_" + k: v
            for i in range(20)
            for k, v in packet_dict["m_tyreSetData"][i].items()
        }

        return {
            **header_fields,
            **other_fields,
            **tyre_set_data,
        }
