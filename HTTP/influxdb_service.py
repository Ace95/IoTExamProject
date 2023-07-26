from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from dtos import iotData

# Create the InfluxDB consumer
token = "0O-HGkisjhPAGZxp6J_G-KqmcDDx_Z6XI41R2S73XDYR1EEuZyDcQemc8AErUsdvWGskiklJq1y9Y4a0TeppXw=="
org = "ML-IoT"
url = "http://localhost:8086"
bucket="IoTExam"

db_client = InfluxDBClient(url=url, token=token, org=org)
write_api = db_client.write_api(write_options=SYNCHRONOUS)
query_api = db_client.query_api()

def save_esp32_data(data: iotData):
    currentDateTime = datetime.utcnow()
    point = (
        Point("esp32Events")
        .tag("deviceName", data.sensor)
        .time(currentDateTime)
        .field("temperature", data.temperature)
    )
    write_api.write(bucket=bucket, org="ML-IoT", record=point)

    point = (
        Point("esp32Events")
        .tag("deviceName", data.sensor)
        .time(currentDateTime)
        .field("humidity", data.humidity)
    )
    write_api.write(bucket=bucket, org="ML-IoT", record=point)

    point = (
        Point("esp32Events")
        .tag("deviceName", data.sensor)
        .time(currentDateTime)
        .field("waterLevel", data.waterLevel)
    )
    write_api.write(bucket=bucket, org="ML-IoT", record=point)

    return point

def get_db_token():
    return token

def get_esp32_data():
    query = """from(bucket: "IoTExam") 
        |> range(start: -10m)
        |> filter(fn: (r) => r._measurement == "esp32Events")"""
    tables = query_api.query(query, org="ML-IoT")

    records = []

    for table in tables:
        for record in table.records:
            records.append(record)

    return records

def get_hum_data():
    query = """from(bucket: "IoTExam") 
        |> range(start: -10m)
        |> filter(fn: (r) => r._measurement == "esp32Events")
        |> filter(fn: (r) => r._field == "humidity")"""
    tables = query_api.query(query, org="ML-IoT")

    records = []

    for table in tables:
        for record in table.records:
            records.append(record.get_value())

    return records

def get_temp_data():
    query = """from(bucket: "IoTExam") 
        |> range(start: -10m)
        |> filter(fn: (r) => r._measurement == "esp32Events")
        |> filter(fn: (r) => r._field == "temperature")"""
    tables = query_api.query(query, org="ML-IoT")

    records = []

    for table in tables:
        for record in table.records:
            records.append(record.get_value())

    return records

def get_level_data():
    query = """from(bucket: "IoTExam") 
        |> range(start: -10m)
        |> filter(fn: (r) => r._measurement == "esp32Events")
        |> filter(fn: (r) => r._field == "waterLevel")"""
    tables = query_api.query(query, org="ML-IoT")

    records = []

    for table in tables:
        for record in table.records:
            records.append(record.get_value())

    return records