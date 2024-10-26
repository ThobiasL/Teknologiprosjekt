void setup() {
  Serial.begin(9600);  // Sett opp samme baud rate som Raspberry Pi
}

void loop() {
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');  // Les innkommende data
    Serial.println("Received: " + message);  // Skriv ut mottatt data til Serial Monitor
  }
}
