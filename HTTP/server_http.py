# to expose API netsh interface portproxy add v4tov4 listenport=8000 listenaddress=192.168.0.119 connectport=8000 connectaddress=127.0.0.1

from fastapi import FastAPI
from dtos import iotData, iotParameters
from endpoints import handlePostData, handleGetData, handleGetToken
import os

app = FastAPI()

@app.post("/data/")
async def handlePost(data: iotData):
  return await handlePostData(data)

@app.get("/data/")
async def handleData():
  return await handleGetData()

@app.get("/token/")
async def handleToken():
  return await handleGetToken()

def main():
  os.system('uvicorn crazyapi:app --reload')

if __name__ == "__main__":
    main()