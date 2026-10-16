import ctypes
from .packetheader import PacketHeader

NUM_MARSHAL_ZONES = 21
NUM_WEATHER_FORECAST_SAMPLES = 56


class MarshalZone(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_zoneStart", ctypes.c_float),
        ("m_zoneFlag", ctypes.c_int8),
    ]

    def to_dict(self):
        return {
            field_name: getattr(self, field_name) for field_name, _ in self._fields_
        }


class WeatherForecastSample(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_sessionType", ctypes.c_uint8),
        ("m_timeOffset", ctypes.c_uint8),
        ("m_weather", ctypes.c_uint8),
        ("m_trackTemperature", ctypes.c_int8),
        ("m_trackTemperatureChange", ctypes.c_int8),
        ("m_airTemperature", ctypes.c_int8),
        ("m_airTemperatureChange", ctypes.c_int8),
        ("m_rainPercentage", ctypes.c_uint8),
    ]

    def to_dict(self):
        return {
            field_name: getattr(self, field_name) for field_name, _ in self._fields_
        }


class PacketSessionData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_weather", ctypes.c_uint8),
        ("m_trackTemperature", ctypes.c_int8),
        ("m_airTemperature", ctypes.c_int8),
        ("m_totalLaps", ctypes.c_uint8),
        ("m_trackLength", ctypes.c_uint16),
        ("m_sessionType", ctypes.c_uint8),
        ("m_trackId", ctypes.c_int8),
        ("m_formula", ctypes.c_uint8),
        ("m_sessionTimeLeft", ctypes.c_uint16),
        ("m_sessionDuration", ctypes.c_uint16),
        ("m_pitSpeedLimit", ctypes.c_uint8),
        ("m_gamePaused", ctypes.c_uint8),
        ("m_isSpectating", ctypes.c_uint8),
        ("m_spectatorCarIndex", ctypes.c_uint8),
        ("m_sliProNativeSupport", ctypes.c_uint8),
        ("m_numMarshalZones", ctypes.c_uint8),
        ("m_marshalZone", MarshalZone * NUM_MARSHAL_ZONES),
        ("m_safetyCarStatus", ctypes.c_uint8),
        ("m_networkGame", ctypes.c_uint8),
        ("m_numWeatherForecastSamples", ctypes.c_uint8),
        (
            "m_weatherForecastSample",
            WeatherForecastSample * NUM_WEATHER_FORECAST_SAMPLES,
        ),
        ("m_forecastAccuracy", ctypes.c_uint8),
        ("m_aiDifficulty", ctypes.c_uint8),
        ("m_seasonLinkIdentifier", ctypes.c_uint32),
        ("m_weekendLinkIdentifier", ctypes.c_uint32),
        ("m_sessionLinkIdentifier", ctypes.c_uint32),
        ("m_pitStopWindowIdealLap", ctypes.c_uint8),
        ("m_pitStopWindowLatestLap", ctypes.c_uint8),
        ("m_pitStopRejoinPosition", ctypes.c_uint8),
        ("m_steeringAssist", ctypes.c_uint8),
        ("m_brakingAssist", ctypes.c_uint8),
        ("m_gearboxAssist", ctypes.c_uint8),
        ("m_pitAssist", ctypes.c_uint8),
        ("m_pitReleaseAssist", ctypes.c_uint8),
        ("m_ERSAssist", ctypes.c_uint8),
        ("m_DRSAssist", ctypes.c_uint8),
        ("m_dynamicRacingLine", ctypes.c_uint8),
        ("m_dynamicRacingLineType", ctypes.c_uint8),
        ("m_gameMode", ctypes.c_uint8),
        ("m_ruleSet", ctypes.c_uint8),
        ("m_timeOfDay", ctypes.c_uint32),
        ("m_sessionLength", ctypes.c_uint8),
        ("m_speedUnitsLeadPlayer", ctypes.c_uint8),
        ("m_temperatureUnitsLeadPlayer", ctypes.c_uint8),
        ("m_speedUnitsSecondaryPlayer", ctypes.c_uint8),
        ("m_temperatureUnitsSecondaryPlayer", ctypes.c_uint8),
        ("m_numSafetyCarPeriods", ctypes.c_uint8),
        ("m_numVirtualSafetyCarPeriods", ctypes.c_uint8),
    ]

    def to_dict(self):
        result = {
            field_name: getattr(self, field_name).to_dict()
            if isinstance(getattr(self, field_name), ctypes.Structure)
            else getattr(self, field_name)
            for field_name, field_type in self._fields_
            if field_name != "m_marshalZone" and field_name != "m_weatherForecastSample"
        }
        result["m_marshalZone"] = [
            self.m_marshalZone[i].to_dict() for i in range(NUM_MARSHAL_ZONES)
        ]
        result["m_weatherForecastSample"] = [
            self.m_weatherForecastSample[i].to_dict()
            for i in range(NUM_WEATHER_FORECAST_SAMPLES)
        ]
        return result

    def flatten(self, car_index):
        packet_dict = self.to_dict()

        # Flatten the header fields
        header_fields = {"m_header_" + k: v for k, v in packet_dict["m_header"].items()}
        del packet_dict["m_header"]

        # Extract car data and other fields
        other_fields = {
            k: v
            for k, v in packet_dict.items()
            if k != "m_marshalZone" or k != "m_weatherForecastSample"
        }

        # Flatten the m_marshalZone fields and include all 21 zones
        marshal_zone_fields = {
            "m_marshalZone_" + str(i) + "_" + k: v
            for i in range(NUM_MARSHAL_ZONES)
            for k, v in packet_dict["m_marshalZone"][i].items()
        }

        # Flatten the m_weatherForecastSample fields and include all 56 samples
        weather_forecast_sample_fields = {
            "m_weatherForecastSample_" + str(i) + "_" + k: v
            for i in range(NUM_WEATHER_FORECAST_SAMPLES)
            for k, v in packet_dict["m_weatherForecastSample"][i].items()
        }

        return {
            **header_fields,
            **other_fields,
            **marshal_zone_fields,
            **weather_forecast_sample_fields,
        }
