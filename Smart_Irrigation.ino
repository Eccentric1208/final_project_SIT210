#include <WiFiNINA.h>
#include <DHT.h>
#include <ArduinoHttpClient.h>

// Pin definitions
#define DHTPIN 2
#define DHTTYPE DHT11
#define MOISTURE_PIN A0

DHT dht(DHTPIN, DHTTYPE);

// WiFi credentials
char ssid[] = "TP-Link_729D";
char pass[] = "tplink123";

// Server details
char serverAddress[] = "192.168.1.100";  // Replace with your Raspberry Pi IP address
int port = 5000;

WiFiClient wifi;
HttpClient client = HttpClient(wifi, serverAddress, port);

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(MOISTURE_PIN, INPUT);

  // Connect to WiFi
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  int soilMoistureRaw = analogRead(MOISTURE_PIN);

  // Convert soil moisture raw value to percentage
  int soilMoisturePercent = map(soilMoistureRaw, 1000, 200, 0, 100);
  soilMoisturePercent = constrain(soilMoisturePercent, 0, 100);  // Ensure the value is within 0-100%

  // Send data to server
  String postData = "humidity=" + String(humidity) + "&temperature=" + String(temperature) + "&soilMoisture=" + String(soilMoisturePercent);
  client.post("/data", "application/x-www-form-urlencoded", postData);

  int statusCode = client.responseStatusCode();
  String response = client.responseBody();
  Serial.println("Status code: " + String(statusCode));
  Serial.println("Response: " + response);

  delay(1000);  // Delay between readings
}
