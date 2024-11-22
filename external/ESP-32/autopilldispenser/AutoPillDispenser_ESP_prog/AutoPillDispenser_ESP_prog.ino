#define BUTTON_PIN 12    // Knapp for å aktivere enable-signal
#define ENABLE_PIN 13    // Pin som sender enable-signal til Arduino
#define DONE_PIN 14      // Pin som mottar done-signal fra Arduino

bool enableActive = false;

void setup() {
  Serial.begin(115200);

  pinMode(BUTTON_PIN, INPUT_PULLUP); // Intern pullup for knappen
  pinMode(ENABLE_PIN, OUTPUT);      // Enable pin som utgang
  pinMode(DONE_PIN, INPUT);         // Done pin som inngang

  digitalWrite(ENABLE_PIN, LOW);    // Sett enable-signal lavt ved oppstart
  Serial.println("ESP32 Ready");
}

void loop() {
  // Sjekk om knappen trykkes inn
  if (digitalRead(BUTTON_PIN) == LOW && !enableActive) {
    Serial.println("Knapp trykket - aktiverer enable-signal");
    digitalWrite(ENABLE_PIN, HIGH); // Sett enable-signal til HIGH
    enableActive = true;           // Marker at enable er aktivert
    delay(200);                    // Debounce for knappen
  }

  // Sjekk om done-signalet mottas
  if (enableActive && digitalRead(DONE_PIN) == HIGH) {
    Serial.println("Done-signal mottatt - deaktiverer enable-signal");
    digitalWrite(ENABLE_PIN, LOW); // Sett enable-signal til LOW
    enableActive = false;          // Marker at enable er deaktivert
    delay(100);                    // Kort forsinkelse for stabilitet
  }
}
