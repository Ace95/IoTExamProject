# Pet Smart Bowl - IoT Exam Project
 Exam project for the 2022/23 IoT course @ UNIBO
 
 In this work I present a Smart Bowl for pets, that monitors the water level and send an allert when the level is too low.

## Architecture
The system is divided into:
- Hardware components: ESP32 VROOM by DOiT, DH22 temperature and humidity sensor and HC-SR04 ultrasonic ranging sensor
- Communication pipeline: some parameters on the ESP32 are tunable through MQTT (base water level, water level threshold, sampling rate and number of allarms before sending the allert).
                          I used Mosquitto as broker for the Pub/Sub protocol.
                          Data collected by the sensor is sent to a data proxy using HTTP protocol (HTTP server wrote in Python) that collects the received data into an InfluxDB (Docker).
- Forcasting models: two models have been developed in order to forcast the water level during the day. The first simpler model only utilizes the base water level and assumes constant descrising in the water level.
                     The second model implemente also the information about temperature and humidity in order to predict a more accurate water level. The results from both models are then evaluated respect to the actual 
                     measured level using RMS error between the two values.
- Data representation: the stored data is then made available for visualization through Grafana.

 ## How to run the full system

### On the ESP32
In the folder "esp32" you can find the script file that must be flashed on the ESP32 board. I developed the code in C++ with the [ArduinoIDE](https://www.arduino.cc/en/software), so make sure to install all the required librariesto to be able to run the script correctly.

### On your pc
On your pc you need to install some components and libraries:
- (Optional) Docker desktop to run the InfluxDB composer you find in the folder "docker". You can skip this step if you have an online InfluxDB account;
-  [Grafana](https://grafana.com/);
-  [Mosquitto Broker](https://mosquitto.org/), this one is needed to handle the MQTT Pub/Sub;
-  [MQTT Explorer](http://mqtt-explorer.com/), I've used this app to change the parameters on the ESP32;
-  [Fast API](https://fastapi.tiangolo.com/) and [Uvicorn](https://www.uvicorn.org/) python libraries, these libraries have been used to create the HTTP server that collects data from the ESP32.
> pip install fast-api uvicorn

NOTE you need to specify the correcte SSID and IP adresses where requested. Also, you may have to open your ports, in order to allow the communicatin with the ESP32, and run the follwing command: </br>
> netsh interface portproxy add v4tov4 listenport=xxxx listenaddress=xxx.xxx.xxx.xxx connectport=xxxx connectaddress=127.0.0.1

Once you are done with the set-up, open two terminals: in the first one launch the server_http.py file, while in the second one you must run the Mosquitto Broker.
At this point you can boot the previously-flashed ESP32 and the system should be online and working.
