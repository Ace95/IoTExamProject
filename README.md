# Pet Smart Bowl - IoTExamProject
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
In the folder "esp32" you can find the script file that must be flashed on the ESP32 board. I developed the code in C++ with the [ArduinoIDE](https://www.arduino.cc/en/software), so make sure to install all the required librariesto be able to run the script correctly.

### On you pc
On you pc you need to install some components:
- (Optional) Docker desktop to run the InfluxDB composer you find in the folder "docker". You can skip this step if you have an online InfluxDB account;
-  Grafana;
-  Mosquitto Broker, this one is needed to handle the MQTT Pub/Sub;
-  Fast API python library, this library have been used to create the HTTP server that collects data from the ESP32.
