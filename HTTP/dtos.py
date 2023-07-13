from pydantic import BaseModel

#Data Transfer Object

class iotData(BaseModel):
  sensor: str
  temperature: float
  humidity: float
  waterLevel: float
  baseLevel: float
  RSSI: float
  alarm: str
  time: float
  dt: float
  status: int
