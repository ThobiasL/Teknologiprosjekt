#include <WiFi.h>
#include <WiFiUdp.h>
#define BUTTON_PIN 12    // Knapp for Ã¥ aktivere enable-signal
#define ENABLE_PIN 13    // Pin som sender enable-signal til Arduino
#define DONE_PIN 14      // Pin som mottar done-signal fra Arduino

bool enableActive = false;

// Wi-Fi credentials
const char* ssid = "MakerSpace";
const char* password = "321drossap";
// UDP port for receiving commands
const unsigned int udpPort = 12345;
// UDP port for sending confirmations
const IPAddress confirmationIP(192, 168, 1, 208); // Din datamaskins IP-adresse
const unsigned int confirmationPort = 54321;      // Din Python-skriptets lytteport
WiFiUDP udp;

// Function declaration for sendUDPMessage
void sendUDPMessage(const char* message, IPAddress ip, unsigned int port);

void setup() {
  Serial.begin(115200);

  pinMode(BUTTON_PIN, INPUT_PULLUP); // Intern pullup for knappen
  pinMode(ENABLE_PIN, OUTPUT);      // Enable pin som utgang
  pinMode(DONE_PIN, INPUT);         // Done pin som inngang

  digitalWrite(ENABLE_PIN, LOW);    // Sett enable-signal lavt ved oppstart
  Serial.println("ESP32 Ready");

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi!");
  Serial.print("Device IP Address: ");
  Serial.println(WiFi.localIP());
  // Start listening for UDP messages
  udp.begin(udpPort);
  Serial.println("Listening for UDP messages on port " + String(udpPort));
}

void loop() {
  
  // Wait for a UDP packet
  int packetSize = udp.parsePacket();
  if (packetSize) {
    char incomingPacket[255];
    int len = udp.read(incomingPacket, 254); // Reserve space for null terminator
    if (len > 0) {
      incomingPacket[len] = 0;  // Null-terminate the message
    }
    Serial.print("Received message: ");
    Serial.println(incomingPacket);
    // Capture sender's IP and port for sending confirmation
    IPAddress senderIP = udp.remoteIP();
    unsigned int senderPort = udp.remotePort();

    if (strcmp(incomingPacket, "Dispens Pills") == 0) {
      Serial.println("Knapp trykket - aktiverer enable-signal");
      digitalWrite(ENABLE_PIN, HIGH); // Sett enable-signal til HIGH
      enableActive = true;           // Marker at enable er aktivert
      delay(200);                    // Debounce for knappen
    }
  }
  // Sjekk om done-signalet mottas
  if (enableActive && digitalRead(DONE_PIN) == HIGH) {
    Serial.println("Done-signal mottatt - deaktiverer enable-signal");
    digitalWrite(ENABLE_PIN, LOW); // Sett enable-signal til LOW
    enableActive = false;          // Marker at enable er deaktivert
    sendUDPMessage("Pills Dispens", confirmationIP, confirmationPort);
    delay(100);                    // Kort forsinkelse for stabilitet
    
  }
}

// Function to send UDP messages
void sendUDPMessage(const char* message, IPAddress ip, unsigned int port) {
  Serial.print("Attempting to send UDP message: ");
  Serial.println(message);

  udp.beginPacket(ip, port);
  udp.print(message);  // Use udp.print instead of udp.write
  if (udp.endPacket()) {
    Serial.print("Sent UDP message: ");
    Serial.println(message);
  } else {
    Serial.println("Failed to send UDP message.");
  }
}