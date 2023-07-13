from sklearn.metrics import mean_squared_error as mse
from utils import simpleModel,upgradedModel, read_data
import sys   
sys.path.insert(1, 'C:/Users/Marco/Documents/Corsi Uni/Internet of Things/FinalProject/IoTExamProject/HTTP')
from dtos import iotData

temperature, humidity, baseLevel, waterLevel, time, dt, status = read_data(iotData)

dt = 1000

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

