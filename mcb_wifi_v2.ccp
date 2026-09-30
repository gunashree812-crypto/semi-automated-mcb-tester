
#include <WiFi.h>

// ESP32 will broadcast its own Wi-Fi network
const char* AP_SSID = "STM32_MCB_Tester";
const char* AP_PASS = "12345678"; // Must be at least 8 characters

WiFiServer server(8888);
WiFiClient client;

#define RX2_PIN 16
#define TX2_PIN 17

void setup() {
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, RX2_PIN, TX2_PIN);

  // Start ESP32 Access Point mode
  WiFi.softAP(AP_SSID, AP_PASS);
  
  Serial.println("\n--- ESP32 Access Point Started ---");
  Serial.print("Connect your laptop Wi-Fi to: ");
  Serial.println(AP_SSID);
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.softAPIP()); // Default is always 192.168.4.1

  server.begin();
}

void loop() {
  if (!client || !client.connected()) {
    client = server.available();
    if (client) {
      Serial.println("Laptop connected via TCP!");
    }
  }

  // Forward Laptop (Wi-Fi) -> STM32 (UART)
  if (client && client.connected() && client.available()) {
    while (client.available()) {
      char c = client.read();
      Serial2.write(c);
    }
  }

  // Forward STM32 (UART) -> Laptop (Wi-Fi)
  if (Serial2.available()) {
    while (Serial2.available()) {
      char c = Serial2.read();
      if (client && client.connected()) {
        client.write(c);
      }
    }
  }
}