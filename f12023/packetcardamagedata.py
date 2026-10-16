import ctypes
from .packetheader import PacketHeader


class CarDamageData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_tyresWearRL", ctypes.c_float),
        ("m_tyresWearRR", ctypes.c_float),
        ("m_tyresWearFL", ctypes.c_float),
        ("m_tyresWearFR", ctypes.c_float),
        ("m_tyresDamageRL", ctypes.c_uint8),
        ("m_tyresDamageRR", ctypes.c_uint8),
        ("m_tyresDamageFL", ctypes.c_uint8),
        ("m_tyresDamageFR", ctypes.c_uint8),
        ("m_brakesDamageRL", ctypes.c_uint8),
        ("m_brakesDamageRR", ctypes.c_uint8),
        ("m_brakesDamageFL", ctypes.c_uint8),
        ("m_brakesDamageFR", ctypes.c_uint8),
        ("m_frontLeftWingDamage", ctypes.c_uint8),
        ("m_frontRightWingDamage", ctypes.c_uint8),
        ("m_rearWingDamage", ctypes.c_uint8),
        ("m_floorDamage", ctypes.c_uint8),
        ("m_diffuserDamage", ctypes.c_uint8),
        ("m_sidepodDamage", ctypes.c_uint8),
        ("m_drsFault", ctypes.c_uint8),
        ("m_ersFault", ctypes.c_uint8),
        ("m_gearBoxDamage", ctypes.c_uint8),
        ("m_engineDamage", ctypes.c_uint8),
        ("m_engineMGUHWear", ctypes.c_uint8),
        ("m_engineESWear", ctypes.c_uint8),
        ("m_engineCEWear", ctypes.c_uint8),
        ("m_engineICEWear", ctypes.c_uint8),
        ("m_engineMGUKWear", ctypes.c_uint8),
        ("m_engineTCWear", ctypes.c_uint8),
        ("m_engineBlown", ctypes.c_uint8),
        ("m_engineSeized", ctypes.c_uint8),
    ]

    def to_dict(self):
        return {
            field_name: getattr(self, field_name) for field_name, _ in self._fields_
        }


class PacketCarDamageData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_carDamageData", CarDamageData * 22),
    ]

    def to_dict(self):
        result = {
            field_name: getattr(self, field_name).to_dict()
            if isinstance(getattr(self, field_name), ctypes.Structure)
            else getattr(self, field_name)
            for field_name, field_type in self._fields_
            if field_name != "m_carDamageData"
        }
        result["m_carDamageData"] = [
            self.m_carDamageData[i].to_dict() for i in range(22)
        ]
        return result

    def flatten(self, car_index):
        packet_dict = self.to_dict()

        # Flatten the header fields
        header_fields = {"m_header_" + k: v for k, v in packet_dict["m_header"].items()}
        del packet_dict["m_header"]

        # Extract car data and other fields
        other_fields = {k: v for k, v in packet_dict.items() if k != "m_carDamageData"}

        # Flatten the car array data fields
        car_array_fields = {
            "m_carDamageData_" + k: v
            for k, v in packet_dict["m_carDamageData"][car_index].items()
        }

        return {**header_fields, **other_fields, **car_array_fields}
