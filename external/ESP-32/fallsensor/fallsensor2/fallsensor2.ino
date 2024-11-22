#include <WiFi.h>
#include <WiFiUdp.h>

const int PIEZO_PIN = A2;       // dette er pinnen som sjokk sensoren er koblet til
const int BUTTON_PIN = 13;      // Button input
float VOLTAGE_THRESHOLD = 0.4; // Lav terskel for å detektere signaler
bool dropState = false;         // Status for å spore fall
bool lastDropState = false;     // Forrige tilstand av dropState
bool lastButtonState = HIGH;    // Forrige tilstand på knappen

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
  Serial.begin(115200);           // Sett opp seriell kommunikasjon
  pinMode(BUTTON_PIN, INPUT_PULLUP); // Sett knapp som inngang med pull-up motstand
  analogSetWidth(12);             // Sett ADC-oppløsning til 12-bit
  analogSetAttenuation(ADC_0db);  // Reduser spenningsområdet til 0-1.1V for økt sensitivitet

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

    // Process incoming message
    // You can add logic here to process different commands from incomingPacket
  }

  // Read Piezo ADC value and convert to voltage
  int piezoADC = analogRead(PIEZO_PIN);
  float piezoV = piezoADC / 4095.0 * 1.1; // Use 12-bit ADC and 1.1V range

  // Check if the voltage exceeds the threshold
  if (piezoV > VOLTAGE_THRESHOLD) {
    dropState = true; // Set dropState to true if voltage exceeds threshold
  }

  // Read button state
  bool currentButtonState = digitalRead(BUTTON_PIN);

  // If the button goes from HIGH to LOW, toggle dropState
  if (lastButtonState == HIGH && currentButtonState == LOW) { // Detect "falling edge"
    dropState = !dropState; // Toggle dropState
  }

  // Update previous button state
  lastButtonState = currentButtonState;

  // Check if dropState has changed
  if (dropState != lastDropState) {
    Serial.println("Change!"); // Here you can add wireless code
    if (dropState){
      sendUDPMessage("fall_detected", confirmationIP, confirmationPort);
    }
    else{
      sendUDPMessage("false_alarm", confirmationIP, confirmationPort);
    }
    lastDropState = dropState; // Update the previous state of dropState
  }

  // Print status to Serial Monitor
  Serial.print("Piezo Voltage: ");
  Serial.print(piezoV, 3); // Display 3 decimal places
  Serial.print(" V, DropState: ");
  Serial.println(dropState ? "True" : "False");

  delay(10); // Short delay for smooth measurements
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
