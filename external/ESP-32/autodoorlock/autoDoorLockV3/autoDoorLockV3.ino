#include <ESP32Servo.h>

Servo myservo;

const int lockButton = 13;     // Definerer pinnen for lås-knappen
const int unlockButton = 12;   // Definerer pinnen for lås-opp-knappen
const unsigned long debounceDelay = 50; // Bruker debounce for å unngå dobbeltrykk eller "fantom" trykk

// Setter button states
int lockButtonState = HIGH;
int lastLockButtonState = HIGH;
int unlockButtonState = HIGH;
int lastUnlockButtonState = HIGH;

unsigned long lastDebounceTime = 0;

// Setter startstatus for låsen til ulåst
bool isLocked = false; // Startstatus: Ulåst

void setup() {
  myservo.attach(14); // Koble servoen til pin 5
  pinMode(lockButton, INPUT_PULLUP);
  pinMode(unlockButton, INPUT_PULLUP);

  myservo.detach(); // Frigjør servoen ved oppstart for å spare strøm
}

void loop() {
  int readingLock = digitalRead(lockButton);
  int readingUnlock = digitalRead(unlockButton);

  // Debouncing for "lås"-knapp
  if (readingLock != lastLockButtonState) {
    lastDebounceTime = millis(); // Start debouncing-timer
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (readingLock != lockButtonState) {
      lockButtonState = readingLock;

      // Hvis "lås"-knappen er trykket og servoen er ulåst
      if (lockButtonState == LOW && !isLocked) {
        myservo.attach(14); // Aktiver servoen
        myservo.write(0);   // Full hastighet mot klokka for å låse
        delay(500);         // Roter i 500 ms
        myservo.write(90);  // Stopp servoen
        delay(10);          // Kort forsinkelse før frigjøring
        myservo.detach();   // Frigjør servoen
        isLocked = true;    // Oppdater status til låst
      }
    }
  }

  // Debouncing for "lås opp"-knapp
  if (readingUnlock != lastUnlockButtonState) {
    lastDebounceTime = millis(); // Start debouncing-timer
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (readingUnlock != unlockButtonState) {
      unlockButtonState = readingUnlock;

      // Hvis "lås opp"-knappen er trykket og servoen er låst
      if (unlockButtonState == LOW && isLocked) {
        myservo.attach(14); // Aktiver servoen
        myservo.write(180); // Full hastighet med klokka for å låse opp
        delay(500);         // Roter i 500 ms
        myservo.write(90);  // Stopp servoen
        delay(10);          // Kort forsinkelse før frigjøring
        myservo.detach();   // Frigjør servoen
        isLocked = false;   // Oppdater status til ulåst
      }
    }
  }

  // Lagre den siste tilstanden for neste loop
  lastLockButtonState = readingLock;
  lastUnlockButtonState = readingUnlock;

  delay(10); // Kort forsinkelse for å stabilisere knappeinput
}
