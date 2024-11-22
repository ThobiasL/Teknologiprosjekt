/*dette er en fungerende "offline" kode for autodoorlock, den har inkludert knappefunksjoner, servobevegelse og "minne" på hvilken posisjon låsen står i */

#include <Servo.h>

Servo myservo;

const int lockButton = 4;     //definerer pinnen for lås knappen
const int unlockButton = 3;   //definerer pinnen for lås-opp knappen  
const unsigned long debounceDelay = 50; // bruker debounce for å unngå dobbeltrykk eller "fantom" trykk 


//setter buttonstates
int lockButtonState = HIGH;
int lastLockButtonState = HIGH;
int unlockButtonState = HIGH;
int lastUnlockButtonState = HIGH;

unsigned long lastDebounceTime = 0;

//setter startstatus for låsen til ulåst, enheten vil da bli montert mens døra er ulåst slik at den vil vite hvilken posisjon låsen er i
bool isLocked = false; // Startstatus: Ulåst

void setup() {
  myservo.attach(5); //servo kobles til digital pinne 5
  pinMode(lockButton, INPUT_PULLUP);
  pinMode(unlockButton, INPUT_PULLUP);

  myservo.detach(); // Frigjør servoen til å begynne med, dette for å sørge for at ikke servoen står å holder, det vil føre til økt strømbruk
}

void loop() {
  int readingLock = digitalRead(lockButton);
  int readingUnlock = digitalRead(unlockButton);

  // Debouncing for "lås" knapp
  if (readingLock != lastLockButtonState) {
    lastDebounceTime = millis(); // Start debouncing-timer
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (readingLock != lockButtonState) {
      lockButtonState = readingLock;

      // Hvis "lås" knapp er trykket og servoen er ulåst
      if (lockButtonState == LOW && !isLocked) {
        myservo.attach(5); // Aktiver servoen
        myservo.write(0);   // Full hastighet mot klokka for å låse
        delay(500);         // Roter i 500 ms
        myservo.write(90);  // Stopp servoen
        delay(10);          // Kort forsinkelse før frigjøring
        myservo.detach();   // Frigjør servoen
        isLocked = true;    // Oppdater status til låst
      }
    }
  }

  // Debouncing for "lås opp" knapp
  if (readingUnlock != lastUnlockButtonState) {
    lastDebounceTime = millis(); // Start debouncing-timer
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (readingUnlock != unlockButtonState) {
      unlockButtonState = readingUnlock;

      // Hvis "lås opp" knapp er trykket og servoen er låst
      if (unlockButtonState == LOW && isLocked) {
        myservo.attach(5); // Aktiver servoen
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
