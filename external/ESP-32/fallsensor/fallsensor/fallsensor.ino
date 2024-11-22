const int PIEZO_PIN = A0;       // dette er pinnen som sjokk sensoren er koblet til
const int BUTTON_PIN = 13;      // Button input
float VOLTAGE_THRESHOLD = 0.4; // Lav terskel for å detektere signaler
bool dropState = false;         // Status for å spore fall
bool lastDropState = false;     // Forrige tilstand av dropState
bool lastButtonState = HIGH;    // Forrige tilstand på knappen

void setup() {
  Serial.begin(115200);           // Sett opp seriell kommunikasjon
  pinMode(BUTTON_PIN, INPUT_PULLUP); // Sett knapp som inngang med pull-up motstand
  analogSetWidth(12);             // Sett ADC-oppløsning til 12-bit
  analogSetAttenuation(ADC_0db);  // Reduser spenningsområdet til 0-1.1V for økt sensitivitet
}

void loop() {
  // Les Piezo ADC-verdi og konverter til spenning
  int piezoADC = analogRead(PIEZO_PIN);
  float piezoV = piezoADC / 4095.0 * 1.1; // Bruk 12-bit og 1.1V inngangsområde

  // Sjekk om spenningen overskrider terskelen
  if (piezoV > VOLTAGE_THRESHOLD) {
    dropState = true; // Sett dropState til true hvis spenningsgrensen overskrides
  }

  // Les knappens tilstand
  bool currentButtonState = digitalRead(BUTTON_PIN);

  // Hvis knappen går fra HIGH til LOW, toggles dropState
  if (lastButtonState == HIGH && currentButtonState == LOW) { // Detekterer "falling edge"
    dropState = !dropState; // Toggle dropState
  }

  // Oppdater forrige knappetilstand
  lastButtonState = currentButtonState;

  // Sjekk om dropState har endret seg
  if (dropState != lastDropState) {
    Serial.println("Change!"); // her kan du legge wireless kode
    lastDropState = dropState;//denne må du ha med siden den oppdaterer dropstate, slik at denne henger med
  }

  // Skriv ut status til Serial Monitor
  Serial.print("Piezo Voltage: ");
  Serial.print(piezoV, 3); // Vis 3 desimaler
  Serial.print(" V, DropState: ");
  Serial.println(dropState ? "True" : "False");

  delay(10); // Kort forsinkelse for å sikre jevne målinger
}
