import ctypes
from .packetheader import PacketHeader


class CarMotionData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_worldPositionX", ctypes.c_float),
        ("m_worldPositionY", ctypes.c_float),
        ("m_worldPositionZ", ctypes.c_float),
        ("m_worldVelocityX", ctypes.c_float),
        ("m_worldVelocityY", ctypes.c_float),
        ("m_worldVelocityZ", ctypes.c_float),
        ("m_worldForwardDirX", ctypes.c_int16),
        ("m_worldForwardDirY", ctypes.c_int16),
        ("m_worldForwardDirZ", ctypes.c_int16),
        ("m_worldRightDirX", ctypes.c_int16),
        ("m_worldRightDirY", ctypes.c_int16),
        ("m_worldRightDirZ", ctypes.c_int16),
        ("m_gForceLateral", ctypes.c_float),
        ("m_gForceLongitudinal", ctypes.c_float),
        ("m_gForceVertical", ctypes.c_float),
        ("m_yaw", ctypes.c_float),
        ("m_pitch", ctypes.c_float),
        ("m_roll", ctypes.c_float),
    ]

    def to_dict(self):
        return {
            field_name: getattr(self, field_name) for field_name, _ in self._fields_
        }


class PacketMotionData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_carMotionData", CarMotionData * 22),
        ("m_suspensionPositionRL", ctypes.c_float),
        ("m_suspensionPositionRR", ctypes.c_float),
        ("m_suspensionPositionFL", ctypes.c_float),
        ("m_suspensionPositionFR", ctypes.c_float),
        ("m_suspensionVelocityRL", ctypes.c_float),
        ("m_suspensionVelocityRR", ctypes.c_float),
        ("m_suspensionVelocityFL", ctypes.c_float),
        ("m_suspensionVelocityFR", ctypes.c_float),
        ("m_suspensionAccelerationRL", ctypes.c_float),
        ("m_suspensionAccelerationRR", ctypes.c_float),
        ("m_suspensionAccelerationFL", ctypes.c_float),
        ("m_suspensionAccelerationFR", ctypes.c_float),
        ("m_wheelSpeedRL", ctypes.c_float),
        ("m_wheelSpeedRR", ctypes.c_float),
        ("m_wheelSpeedFL", ctypes.c_float),
        ("m_wheelSpeedFR", ctypes.c_float),
        ("m_wheelSlipRatioRL", ctypes.c_float),
        ("m_wheelSlipRatioRR", ctypes.c_float),
        ("m_wheelSlipRatioFL", ctypes.c_float),
        ("m_wheelSlipRatioFR", ctypes.c_float),
        ("m_wheelSlipAngleRL", ctypes.c_float),
        ("m_wheelSlipAngleRR", ctypes.c_float),
        ("m_wheelSlipAngleFL", ctypes.c_float),
        ("m_wheelSlipAngleFR", ctypes.c_float),
        ("m_wheelLatForceRL", ctypes.c_float),
        ("m_wheelLatForceRR", ctypes.c_float),
        ("m_wheelLatForceFL", ctypes.c_float),
        ("m_wheelLatForceFR", ctypes.c_float),
        ("m_wheelLongForceRL", ctypes.c_float),
        ("m_wheelLongForceRR", ctypes.c_float),
        ("m_wheelLongForceFL", ctypes.c_float),
        ("m_wheelLongForceFR", ctypes.c_float),
        ("m_heightOfCOGAboveGround", ctypes.c_float),
        ("m_localVelocityX", ctypes.c_float),
        ("m_localVelocityY", ctypes.c_float),
        ("m_localVelocityZ", ctypes.c_float),
        ("m_angularVelocityX", ctypes.c_float),
        ("m_angularVelocityY", ctypes.c_float),
        ("m_angularVelocityZ", ctypes.c_float),
        ("m_angularAccelerationX", ctypes.c_float),
        ("m_angularAccelerationY", ctypes.c_float),
        ("m_angularAccelerationZ", ctypes.c_float),
        ("m_frontWheelsAngle", ctypes.c_float),
    ]

    def to_dict(self):
        result = {
            field_name: getattr(self, field_name).to_dict()
            if isinstance(getattr(self, field_name), ctypes.Structure)
            else getattr(self, field_name)
            for field_name, field_type in self._fields_
            if field_name != "m_carMotionData"
        }
        result["m_carMotionData"] = [
            self.m_carMotionData[i].to_dict() for i in range(22)
        ]
        return result

    def flatten(self, car_index):
        packet_dict = self.to_dict()

        # Flatten the header fields
        header_fields = {"m_header_" + k: v for k, v in packet_dict["m_header"].items()}
        del packet_dict["m_header"]

        # Extract car data and other fields
        other_fields = {k: v for k, v in packet_dict.items() if k != "m_carMotionData"}

        # Flatten the car array data fields
        car_array_fields = {
            "m_carMotionData_" + k: v
            for k, v in packet_dict["m_carMotionData"][car_index].items()
        }

        return {**header_fields, **other_fields, **car_array_fields}
