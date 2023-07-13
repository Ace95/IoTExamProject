// Marco Acerbis - Exam Project 2022/2023 IoT Course @ UNIBO
#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <String.h>
#include <HCSR04.h>
#include <time.h>
#include <NTPClient.h>

// WiFi Login information
const char* ssid = "TIM-92837114";
const char* password = "EQAdkDRCNT27u9hQkKGxdtky";

// Define NTP Client to get time
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");

// HTTP Server and MQTT Broker IPs and ports
const char* http_server = "http://192.168.1.17:8000/docs";
const char* mqtt_server = "192.168.1.17";
int mqtt_port = 1883;

//Sensors initialization
DHT dht(23,DHT22); //(pin input, sensor model)
UltraSonicDistanceSensor hc(26,25); //(trig pin , echo pin)

WiFiClient espClient;
PubSubClient client_mqtt(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

// Set up timer to regulate the sampling rate
unsigned long lastTime = 0;
unsigned long timerDelay = 10000;

float baseLevel = 5;
float threshold = 1;
int alarmCounter = 1;
int alarms = 0;
int status = 0;
float dt = 0;
time_t epochTime = 0;


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

  timeClient.update();
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

      epochTime = timeClient.getEpochTime();
      dt = millis();

      float level = distance - baseLevel;

      if (level > threshold){
        alarms = alarms + 1;
      }

      if (alarms < alarmCounter){
        status = 0;
      }else{
        status = 1;
        alarms = 0;
      }

      http.addHeader("Content-Type", "application/json");
      Serial.print("Sending data...");
      // Create a JSON object with the data 
      DynamicJsonDocument data(1024);
      data["sensor"] = "CrazyBowl";
      data["temperature"]   = temperature;
      data["humidity"] = humidity;
      data["waterLevel"] = distance;
      data["baseLevel"] = baseLevel;
      data["RSSI"] = RSSI;
      data["time"] = epochTime;
      data["dt"] = dt;
      data["status"] = status;

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