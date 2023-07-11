def simpleModel(baseLevel,evaCoeff,dt):
    predLevel = baseLevel + evaCoeff*dt 

    return predLevel

def upgradedModel(baseLevel,Ktemperature,humidity,dt,evaCoeff):
    predLevel = baseLevel + evaCoeff*(Ktemperature/humidity)*dt

    return predLevel