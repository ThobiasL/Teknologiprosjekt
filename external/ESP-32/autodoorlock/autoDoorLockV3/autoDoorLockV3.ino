#include <WiFi.h>
#include <WiFiUdp.h>
#include <ESP32Servo.h>

Servo myservo;

const int lockButton = 12;     // Pin for lock button
const int unlockButton = 13;   // Pin for unlock button
const unsigned long debounceDelay = 50;

int lockButtonState = HIGH;
int lastLockButtonState = HIGH;
int unlockButtonState = HIGH;
int lastUnlockButtonState = HIGH;

unsigned long lastDebounceTime = 0;

// Lock status
bool isLocked = false;  // Start unlocked

// Wi-Fi credentials
const char* ssid = "MakerSpace";
const char* password = "321drossap";

// UDP port
const int udpPort = 12345;

WiFiUDP udp;

void setup() {
  Serial.begin(115200);
  myservo.attach(14); // Attach servo to pin 14

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi!");
  Serial.print("Enhetens IP-adresse: ");
  Serial.println(WiFi.localIP());


  // Start listening for UDP messages
  udp.begin(udpPort);
  Serial.println("Listening for UDP messages on port " + String(udpPort));

  // Set button pins as input with pull-up resistors
  pinMode(lockButton, INPUT_PULLUP);
  pinMode(unlockButton, INPUT_PULLUP);
}

void loop() {
  // Handle button presses
  handleButtonPresses();

  // Wait for a UDP packet
  int packetSize = udp.parsePacket();
  if (packetSize) {
    char incomingPacket[255];
    int len = udp.read(incomingPacket, 255);
    if (len > 0) {
      incomingPacket[len] = 0;  // Null-terminate the message
    }

    Serial.print("Received message: ");
    Serial.println(incomingPacket);

    // Check for the "lock door" or "unlock door" message
    if (strcmp(incomingPacket, "unlock door") == 0) {
      lockDoor();
    } else if (strcmp(incomingPacket, "lock door") == 0) {
      unlockDoor();
    }
  }

  delay(100);  // Avoid busy-waiting
}

void handleButtonPresses() {
  // Read button states
  int readingLock = digitalRead(lockButton);
  int readingUnlock = digitalRead(unlockButton);

  // Debouncing for "lock"-button
  if (readingLock != lastLockButtonState) {
    lastDebounceTime = millis(); // Start debounce timer
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (readingLock != lockButtonState) {
      lockButtonState = readingLock;

      // If the "lock" button is pressed and the door is unlocked
      if (lockButtonState == LOW && !isLocked) {
        lockDoor();
      }
    }
  }

  // Debouncing for "unlock"-button
  if (readingUnlock != lastUnlockButtonState) {
    lastDebounceTime = millis(); // Start debounce timer
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (readingUnlock != unlockButtonState) {
      unlockButtonState = readingUnlock;

      // If the "unlock" button is pressed and the door is locked
      if (unlockButtonState == LOW && isLocked) {
        unlockDoor();
      }
    }
  }

  // Store the last button states for next loop
  lastLockButtonState = readingLock;
  lastUnlockButtonState = readingUnlock;
}

void lockDoor() {
  // Lock the door by turning the servo
  if (!isLocked) {
    myservo.attach(14);  // Activate servo
    myservo.write(0);    // Turn to 0 degrees (lock position)
    delay(500);          // Hold for 500ms
    myservo.write(90);   // Stop the servo at 90 degrees (neutral)
    delay(10);           // Small delay before detaching
    myservo.detach();    // Detach servo to save power
    isLocked = true;     // Update lock status
    Serial.println("Door locked!");
  }
}

void unlockDoor() {
  // Unlock the door by turning the servo
  if (isLocked) {
    myservo.attach(14);  // Activate servo
    myservo.write(180);  // Turn to 180 degrees (unlock position)
    delay(500);          // Hold for 500ms
    myservo.write(90);   // Stop the servo at 90 degrees (neutral)
    delay(10);           // Small delay before detaching
    myservo.detach();    // Detach servo to save power
    isLocked = false;    // Update lock status
    Serial.println("Door unlocked!");
  }
}
