#include <LiquidCrystal.h>

// Rotary encoder
const int pinA = 3;  // Connected to CLK on KY-040
const int pinB = 4;  // Connected to DT on KY-040
int encoderPosCount = 0, pinALast, aVal;
bool bCW;

// Knapp-konfigurasjon
const int button_setAlarm = 14;
const int button_editAlarm = 15;
const int button_visit = 16;

// Tilstandsvariabler for knapper
int setAlarmState = 0;
int editAlarmState = 0;
int visitState = 0;

int alarm_mode = 1;
int visit_mode = 1;
int editAlarm_mode = 2;

// Maksverdi for rotary-encoderen
int encoderMax = 100;  // Standard maksverdi

// LCD-skjerm
const int rs = 13, rw = 12, e = 11, d4 = 10, d5 = 9, d6 = 8, d7 = 7;
LiquidCrystal lcd(rs, rw, e, d4, d5, d6, d7);

int column = 0, row = 0;

void setup() {
  pinMode(pinA, INPUT);
  pinMode(pinB, INPUT);
  pinALast = digitalRead(pinA);

  pinMode(button_setAlarm, INPUT_PULLUP);
  pinMode(button_editAlarm, INPUT_PULLUP);
  pinMode(button_visit, INPUT_PULLUP);

  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.clear();

  delay(500);  // Debounce delay
}

void loop() {
  // Oppdater maksimal verdi basert på editAlarm_mode
  if (editAlarm_mode == 1) {
    encoderMax = 23;
  } else if (editAlarm_mode == 2) {
    encoderMax = 59;
  } else {
    encoderMax = 100;
  }

  // Avlesing av sensorer
  aVal = digitalRead(pinA);
  readEncoder();
  readButton(button_setAlarm, setAlarmState, alarm_mode, "alarm_mode");
  readButton(button_editAlarm, editAlarmState, editAlarm_mode, "editAlarm_mode");
  readButton(button_visit, visitState, visit_mode, "visit_mode");

  if (Serial.available() > 0) {
    handleSerialInput();
  }
}

// Funksjon for avlesing og oppdatering av Rotary encoder
void readEncoder() {
  if (aVal != pinALast) {
    bCW = (digitalRead(pinB) != aVal) ? true : false;
    encoderPosCount += bCW ? -1 : 1;

    // Begrens encoderPosCount til å være mellom 0 og encoderMax
    if (encoderPosCount > encoderMax) {
      encoderPosCount = encoderMax;
    } else if (encoderPosCount < 0) {
      encoderPosCount = 0;
    }

    Serial.print("Encoder Position: ");
    Serial.println(encoderPosCount);
    pinALast = aVal;
  }
}

void readButton(int buttonPin, int &currentState, int &currentMode, const char* modeName) {
  int buttonReading = digitalRead(buttonPin);

  if (buttonReading != currentState) {
    if (buttonReading == HIGH) {
      // Hvis knapp for visit_mode, så bruk 0, 1, 2-syklusen
      if (strcmp(modeName, "editAlarm_mode") == 0) {
        currentMode = (currentMode + 1) % 3;  // Veksle mellom 0, 1 og 2
      } 
      else {
        currentMode = !currentMode;  // For andre, veksle mellom 0 og 1
      }
      if (strcmp(modeName, "alarm_mode") == 0) {
        Serial.print("editAlarm_mode");
        Serial.print(": ");
        Serial.println(0);
      }
      else if (strcmp(modeName, "alarm_mode") == 1) {
        Serial.print("editAlarm_mode");
        Serial.print(": ");
        Serial.println(1);
      }
      Serial.print(modeName);
      Serial.print(": ");
      Serial.println(currentMode);
    }
    currentState = buttonReading;
    delay(50);  // Debounce delay
  }
}

// Funksjon for å håndtere Serial Input for LCD
void handleSerialInput() {
  char type = Serial.read();
  String message;

  switch (type) {
    case 'C':
      while (Serial.available() == 0);
      column = Serial.read();
      break;

    case 'R':
      while (Serial.available() == 0);
      row = Serial.read();
      break;

    case 'T':
      message = Serial.readStringUntil('\n');
      lcd.setCursor(column, row);
      lcd.print(message);
      break;
  }
}
