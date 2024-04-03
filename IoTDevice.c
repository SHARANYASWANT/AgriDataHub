#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h> // Include the HTTPClient library
#include <ArduinoJson.h>       // Include the ArduinoJson library
#include <DHT.h>

// Define Wi-Fi credentials
const char* ssid = "Praveen's Galaxy S20 FE 5G";
const char* password = "ovcw6881";

// Define the type of DHT sensor (DHT11 or DHT22)
#define DHTTYPE DHT11 

// Define the pin for DHT sensor
#define DHT_PIN 14 // D5 corresponds to GPIO 14 on NodeMCU

// Define the pin for soil moisture sensor
#define SOIL_MOISTURE_PIN A0

// Initialize DHT sensor
DHT dht(DHT_PIN, DHTTYPE);

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Connect to Wi-Fi
  Serial.println();
  Serial.println("Connecting to WiFi");
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");

  // Initialize DHT sensor
  dht.begin();
}

void loop() {
  // Read sensor data
  float humidity = dht.readHumidity();
  float temperatureCelsius = dht.readTemperature();

  // Read soil moisture sensor value
  int soilMoistureValue = analogRead(SOIL_MOISTURE_PIN);

  // Check if any reads failed and exit early (to try again).
  if (isnan(humidity) || isnan(temperatureCelsius)) {
    Serial.println("Failed to read from DHT sensor!");
    delay(2000);
    return;
  }

  // Create JSON payload for sensor data
  StaticJsonDocument<200> jsonDocument;
  jsonDocument["humidity"] = humidity;
  jsonDocument["temperature"] = temperatureCelsius;
  jsonDocument["soil_moisture"] = soilMoistureValue;

  // Serialize JSON document to a string
  String jsonString;
  serializeJson(jsonDocument, jsonString);

  // Create WiFiClient object
  WiFiClient client;

  // Send HTTP POST request to the server
  HTTPClient http;
  http.begin(client, "http://192.168.54.112:3000/data");

  http.addHeader("Content-Type", "application/json");
  int httpCode = http.POST(jsonString);
  
  // Check for errors
  if (httpCode > 0) {
    Serial.printf("[HTTP] POST request sent, status code: %d\n", httpCode);
  } else {
    Serial.printf("[HTTP] POST request failed, error: %s\n", http.errorToString(httpCode).c_str());
  }
  
  // End HTTP connection
  http.end();

  // Wait for a moment before sending the next request
  delay(5000);
}
