/*
 * Project: Industrial IoT Gateway Prototype
 * Component: Edge Sensor Node
 * Hardware: Arduino Uno
 * Author: Béla Krzebek
*/

#include <ArduinoJson.h>
#include <DHT.h>

// 1. Define constants for configuration (Clean Code practice)
const int LED_PIN = A3;

const int DHT_PIN = 6;
#define DHT_TYPE DHT11 

const unsigned long READ_INTERVAL = 2000; // 2000ms = 2 seconds
const long BAUD_RATE = 115200;            // Faster is better for latency

const char* DEVICE_ID = "MEGA_SENSOR_01";

// 2. Global variable to store the "last time we checked our watch"
unsigned long previousMillis = 0;

//3. Initializing the LEDs and sensors would go here (if any)
DHT dht(DHT_PIN, DHT_TYPE);
StaticJsonDocument<200> doc;              // Reserving memory for json
int ledState = LOW;


void setup() {
  // Initialize Serial Communication
  Serial.begin(BAUD_RATE);
  pinMode(LED_PIN, OUTPUT);
  dht.begin();

  // Empty the json document each session, since the complete data is being handled by the raspberry
  doc.clear();
  
  // Create data structure, through keys
  doc["temperature"];
  doc["humidity"];
  doc["device_id"];
  doc["status"];

  // Wait for Serial to be ready (Good practice for some boards)
  while (!Serial) { ; }
  
  Serial.println("System Initialized.");
}

void loop() {
  // 3. Check the "watch" (Current Time)
  unsigned long currentMillis = millis();

  // 4. Compare: Has enough time passed?
  if (currentMillis - previousMillis >= READ_INTERVAL) {
    // Save the last time you blinked the LED
    previousMillis = currentMillis;

    // 1. Reading sensor data:
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();
    
    // 2. Check for failures:
    if (isnan(humidity) || isnan(temperature)) {
      doc.clear();
      doc["device_id"] = DEVICE_ID;
      doc["status"] = "ERROR_SENSOR_DATA";
      serializeJson(doc, Serial);
      Serial.println();
      
      ledState = HIGH;
      digitalWrite(LED_PIN, ledState);
      return;
    }
    // 3. Data is valid:
    else {
      // Reset LED state in case earlier data was wrong
      ledState = LOW;
      digitalWrite(LED_PIN, ledState);

      // Clear the json doc
      doc.clear();
      
      // Save Data in json doc
      doc["temperature"] = temperature;
      doc["humidity"] = humidity;
      doc["device_id"] = DEVICE_ID;

      // Serialize json data
      serializeJson(doc, Serial);
      Serial.println();
    }
  }
  
  // You can write other code here (like checking buttons) 
  // and it will run INSTANTLY, even while waiting for the 2 seconds.
}