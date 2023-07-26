from sklearn.metrics import mean_squared_error as mse
import time as tm
import numpy as np
from utils import simpleModel,upgradedModel
import sys   
sys.path.insert(1, 'C:/Users/Marco/Documents/Corsi Uni/Internet of Things/FinalProject/IoTExamProject/HTTP')
from dtos import iotData
from influxdb_service import get_hum_data, get_temp_data, get_level_data



def read_data(data: iotData):

    temperature = np.mean(get_temp_data())
    humidity = np.mean(get_hum_data())
    baseLevel = data.baseLevel
    waterLevel = [np.mean(get_level_data())]
    time = data.time
    dt = data.dt/1000
    status = data.status
    rssi = data.rssi

    currentTime = tm.time()
    latency = abs(currentTime - time)

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
    print("Latency: ", latency*1000, " ms")
    print("RSSI: ", rssi, " dBm")


