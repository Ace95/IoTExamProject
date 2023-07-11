from sklearn.metrics import mean_squared_error as mse
from utils import simpleModel,upgradedModel
import sys   
sys.path.insert(1, 'C:/Users/Marco/Documents/Corsi Uni/Internet of Things/FinalProject/IoTExamProject/HTTP')
from dtos import iotData

def read_data(data: iotData):
    temperature = data.temperature


    
Ktemperature = temperature + 273.2
humidity = 0.2
baseLevel = 5
waterLevel = [6]
evaCoeff = 0.000003
dt = 2000
specHeat = 4186 #J/Kg*K

simplePred = [simpleModel(baseLevel,evaCoeff,dt)]
upgradedPred = [upgradedModel(baseLevel,Ktemperature,humidity,dt,evaCoeff)]

simpleError = mse(waterLevel,simplePred)
upgradedError = mse(waterLevel,upgradedPred)

print("Forcasted water level (simple model): ", simplePred, " MSE: ",simpleError)
print("Forcasted water level (upgraded model): ", upgradedPred, " MSE: ",upgradedError)

