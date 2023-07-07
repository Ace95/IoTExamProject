// Marco Acerbis - Exam Project 2022/2023 IoT Course @ UNIBO
#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <String.h>
#include <HCSR04.h>

// WiFi Login information
const char* ssid = "Acerbis";
const char* password = "IoT2023Exam";

// HTTP Server and MQTT Broker IPs and ports
const char* http_server = "http://192.168.43.157:8000/temp";
const char* mqtt_server = "192.168.43.157";
int mqtt_port = 1883;

//Sensors initialization
DHT dht(27,DHT22); //(pin input, sensor model)
UltraSonicDistanceSensor hc(26,25); //(trig pin , echo pin)

WiFiClient espClient;
PubSubClient client_mqtt(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

// Set up timer to regulate the sampling rate
unsigned long lastTime = 0;
unsigned long timerDelay = 10000;

float baseLevel = 0;
float threshold = 0;
int alarmCounter = 0;
int alarms = 0;

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client_mqtt.setServer(mqtt_server, mqtt_port);
  client_mqtt.setCallback(callback);
}

// Function to connect to WiFi
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

//Callback function for the MQTT Client - Once a new message is published on a subscribed topic, 
// the client downloads the message and sets the value of the corresponding variable(s).
void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.println(topic);
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    messageTemp += (char)message[i];
  }
  Serial.println();

  if (String(topic) == "esp32/calibration") {
    Serial.print("Setting new base level to: ");
    baseLevel = messageTemp.toFloat();
    Serial.println(baseLevel);
  }

  if (String(topic) == "esp32/threshold") {
    Serial.print("Setting new threshold to: ");
    threshold = messageTemp.toFloat();
    Serial.println(threshold);
  }

  if (String(topic) == "esp32/samplingRate") {
    Serial.print("Setting new sampling rate to: ");
    timerDelay = messageTemp.toFloat();
    Serial.println(timerDelay);
  }

  if (String(topic) == "esp32/alarmCounter") {
    Serial.print("Setting new alarm counter to: ");
    alarmCounter = messageTemp.toFloat();
    Serial.println(alarmCounter);
  }
  
}
// Function to connect to the MQTT Broker and subscribe to the topic of interest
void reconnect() {

  while (!client_mqtt.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    if (client_mqtt.connect("ESP32Client")) {
      Serial.println("connected");
      
      client_mqtt.subscribe("esp32/calibration");
      client_mqtt.subscribe("esp32/threshold");
      client_mqtt.subscribe("esp32/samplingRate");
      client_mqtt.subscribe("esp32/alarmCounter");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client_mqtt.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
// MQTT client running and checking for updates
  if (!client_mqtt.connected()) {
    reconnect();
  }
  client_mqtt.loop();

// Data is sent through HTTP according to the Sampling Rate
  if ((millis() - lastTime) > timerDelay) {
    if(WiFi.status()== WL_CONNECTED){
      WiFiClient client_wifi;
      HTTPClient http;
    
      http.begin(http_server);

      // Get data from sensors
      float distance = hc.measureDistanceCm();
      float temperature = dht.readTemperature();
      float humidity = dht.readHumidity();
      float RSSI = WiFi.RSSI();

      float level = distance - baseLevel;
      char* alarmMsg = "Water level is ok";

      if (level > threshold){
        alarms = alarms + 1;
      }

      if (alarms >= alarmCounter){
        alarmMsg = "Water level is low!";
        Serial.print("Number of alarms: ");
        Serial.println(alarms);
        alarms = 0;
        Serial.print("Water level too low! Alert sent!");
      }

      http.addHeader("Content-Type", "application/json");
      Serial.print("Sending data...");
      // Create a JSON object with the data 
      DynamicJsonDocument data(1024);
      data["sensor"] = "CrazyBowl";
      data["level"] = level;
      data["temperature"]   = temperature;
      data["humidity"] = humidity;
      data["RSSI"] = RSSI;
      data["alarm"] = alarmMsg;

      serializeJson(data, Serial);
      //Send the JSON through HTTP to the data proxy
      int httpResponseCode = http.POST("{data}");
     
      Serial.println("HTTP Response code: ");
      Serial.println(httpResponseCode);
        
      // Free resources
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}