from pydantic import BaseModel

# Data Transfer Objects

class iotData(BaseModel):
  sensor: str
  temperature: float
  humidity: float
  waterLevel: float
  baseLevel: float
  rssi: float
  time: int
  dt: float
  status: int
