from dtos import iotData
from influxdb_service import save_esp32_data, get_esp32_data, get_db_token

async def handlePostData(data: iotData):
    point = save_esp32_data(data)
    return point

async def handleGetData():
    data = get_esp32_data()
    return data

async def handleGetToken():
    token = get_db_token()
    return token
