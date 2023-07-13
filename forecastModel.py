from sklearn.metrics import mean_squared_error as mse
from datetime import datetime
import time as tm
from utils import simpleModel,upgradedModel
import sys   
sys.path.insert(1, 'C:/Users/Marco/Documents/Corsi Uni/Internet of Things/FinalProject/IoTExamProject/HTTP')
from dtos import iotData

def read_data(data: iotData):
    temperature = data.temperature
    humidity = data.humidity 
    baseLevel = data.baseLevel
    waterLevel = [data.waterLevel]
    time = data.time
    dt = data.dt
    status = data.status

    currentTime = datetime.utcnow()
    timestamp = int(currentTime.timestamp())
    latency = time - timestamp 

    simplePred = [simpleModel(baseLevel,dt)]
    upgradedPred = [upgradedModel(baseLevel,temperature,humidity,dt)]

    simpleError = mse(waterLevel,simplePred)
    upgradedError = mse(waterLevel,upgradedPred)

    if (status == 1):
        print("Low water level! Refill the bowl!")
    else:
        print("No need to refil the bowl.")

    print("Forecasted water level (simple model): ", simplePred, " MSE: ",simpleError)
    print("Forecasted water level (upgraded model): ", upgradedPred, " MSE: ",upgradedError)
    print("Latency: ", latency, " ms")


