import ctypes

from .packetheader import PacketHeader


class LobbyInfoData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_aiControlled", ctypes.c_uint8),
        ("m_teamId", ctypes.c_uint8),
        ("m_nationality", ctypes.c_uint8),
        ("m_name", ctypes.c_char * 48),
        ("m_carNumber", ctypes.c_uint8),
        ("m_readyStatus", ctypes.c_uint8),
    ]

    def to_dict(self):
        result = {
            field_name: getattr(self, field_name).decode("utf-8").rstrip("\0")
            if field_name == "m_name"
            else getattr(self, field_name)
            for field_name, _ in self._fields_
        }
        return result


class PacketLobbyInfoData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_numPlayers", ctypes.c_uint8),
        ("m_lobbyPlayers", LobbyInfoData * 22),
    ]

    def to_dict(self):
        return {
            field_name: [player.to_dict() for player in getattr(self, field_name)]
            if field_name == "m_lobbyPlayers"
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
        other_fields = {k: v for k, v in packet_dict.items() if k != "m_lobbyPlayers"}

        # Flatten the car array data fields
        car_array_fields = {
            "m_lobbyPlayers_" + k: v
            for k, v in packet_dict["m_lobbyPlayers"][car_index].items()
        }

        return {**header_fields, **other_fields, **car_array_fields}
