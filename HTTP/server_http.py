# Port forwarding // netsh interface portproxy add v4tov4 listenport=8000 listenaddress=192.168.43.157 connectport=8000 connectaddress=127.0.0.1
# To reset port forwarding after reboot // netsh interface portproxy delete v4tov4 listenaddress=192.168.0.119 listenport=8000
# To list all forwarding rules // netsh interface portproxy show all 
# Note: you must run the cmd promt as administrator 

from fastapi import FastAPI
from dtos import iotData
from endpoints import handlePostData, handleGetData, handleGetToken
import os
import sys   
sys.path.insert(1, 'C:/Users/Marco/Documents/Corsi Uni/Internet of Things/FinalProject/IoTExamProject')
from forecastModel import read_data

app = FastAPI()

@app.post("/data/")
async def handlePost(data: iotData):
  read_data(data)
  return await handlePostData(data)

@app.get("/data/")
async def handleData():
  return await handleGetData()

@app.get("/token/")
async def handleToken():
  return await handleGetToken()

def main():
  os.system('uvicorn server_http:app --reload')

if __name__ == "__main__":
    main()