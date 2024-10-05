from datetime import datetime

class DataPoint:
    def __init__(self, 
                 timestamp: datetime = None, 
                 latitude: float = 0.0, 
                 longitude: float = 0.0, 
                 speed: float = 0.0, 
                 heartRate: int = 0, 
                 acceleration: float = 0.0) -> None:
        self.timestamp:     datetime    = None
        if timestamp is not None:
            self.timestamp = datetime.strptime(timestamp, "%H:%M:%S.%f") # Use current time if not provided
        self.latitude:      float       = latitude
        self.longitude:     float       = longitude
        self.speed:         float       = speed
        self.heartRate:     int         = heartRate
        self.acceleration:  float       = acceleration
