def simpleModel(baseLevel,dt):
    predLevel = baseLevel + 0.00278*dt # Simple forecast model with water level descrising constantly of 1 cm per hour

    return predLevel

def upgradedModel(baseLevel,temperature,humidity,dt):
    predLevel = baseLevel + 0.0015*(temperature/humidity)*dt # Upgraded model to also account fot the air temperature and humidity

    return predLevel

def read_data(data):
    temperature = data.temperature
    humidity = data.humidity  
    baseLevel = data.baseLevel
    waterLevel = data.waterLevel
    time = data.time
    dt = data.dt
    status = data.status
    return temperature, humidity, baseLevel, waterLevel, time, dt, status