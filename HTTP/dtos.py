from pydantic import BaseModel

#Data Transfer Object

class iotData(BaseModel):
  sensor: str
  temperature: float
  humidity: float
  waterLevel: float
  bowlHeight: float
  thresholdLevel: float
  signalQuality: float
