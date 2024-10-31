#include <LiquidCrystal.h>

// Rotary encoder
int pinA = 3; // Connected to CLK on KY-040
int pinB = 4; // Connected to DT on KY-040
int encoderPosCount = 0;
int pinALast;
int aVal;
boolean bCW;

// Knappe konfigurasjon
const int button_setAlarm = 14;
const int button_visit = 15;
const int button_editAlarm = 16;

// defienerer variabler som blir brukt i koden.
// variabler til alarm
int setAlarm = 0;
int setAlarm_State = 0;

// variabler til besok
int visit = 0;
int visit_State = 0;

// variabler til edit
int editAlarm = 0;
int editAlarm_State = 0;

// variabler til styring
int alarm_mode = 0;

// variabler til styring
int visit_mode = 0;

// variabler til styring
int editAlarm_mode = 0;

// LCD-skjerm
const int rs = 13;
const int rw = 12;
const int e = 11;
const int d4 = 10;
const int d5 = 9;
const int d6 = 8;
const int d7 = 7;

LiquidCrystal lcd(rs, rw, e, d4, d5, d6, d7);

int column = 0;
int row = 0;

void setup() {
  // Rotary encoder
  pinMode (pinA,INPUT);
  pinMode (pinB,INPUT);

  pinALast = digitalRead(pinA);

  // Knapper
  pinMode(button_setAlarm, INPUT);
  pinMode(button_visit, INPUT);
  pinMode(button_editAlarm, INPUT);

  Serial.begin (9600);

  // LCD-skjerm
  lcd.begin(16, 2);
  lcd.clear();
}

void loop() {
  // Avlesing av sensorer
  aVal = digitalRead(pinA); // variabel for Rotary encoder
  setAlarm = digitalRead(button_setAlarm); // variabel for knapper
  visit = digitalRead(button_visit); // variabel for knapper
  editAlarm = digitalRead(button_editAlarm); // variabel for knapper

  if (Serial.available() > 0) { 
    char type = Serial.read(); // Les datatype som blir brukt som en indikator

    // Rotary encoder
    if (aVal != pinALast){ 
      if (digitalRead(pinB) != aVal) {
        encoderPosCount --;
        bCW = true;
      } 
      else {
        bCW = false;
        encoderPosCount++;
      }

    Serial.print("Encoder Position: ");
    Serial.println(encoderPosCount);

    }
    pinALast = aVal;

    // Knapper
    // hvis trykker på en kanpp skal den skru på eller av manuel mode.
    if (setAlarm != setAlarm_State) {
      if (setAlarm == 1) {
        if (alarm_mode == 0){
          alarm_mode = 1;
          Serial.print("alarm_mode:");
          Serial.println(alarm_mode);
        }
      }
      else{
        alarm_mode = 0;
      }
      setAlarm_State = setAlarm;
      delay(100);
      }

    // hvis trykker på en kanpp skal den skru på eller av manuel mode.
    if (visit != visit_State) {
      if (visit == 1) {
        if (visit_mode == 0){
          visit_mode = 1;
          Serial.print("visit_mode:");
          Serial.println(visit_mode);
        }
      }
      else{
        visit_mode = 0;
      }
      visit_State = visit;
      delay(100);
    }

    // hvis trykker på en kanpp skal den skru på eller av manuel mode.
    if (editAlarm != editAlarm_State) {
      if (editAlarm == 1) {
        if (editAlarm_mode == 0){
          editAlarm_mode = 1;
          Serial.print("editAlarm_mode:");
          Serial.println(editAlarm_mode);
        }
      }
      else{
        editAlarm_mode = 0;
      }
      editAlarm_State = editAlarm;
      delay(100);
    }

    // LCD-skjerm
    if (type == 'K') {                  // indikator for kolonne
      while (Serial.available() == 0);  // Vent til kolonneverdien er tilgjengelig
        column = Serial.read();         // Les kolonneverdi
    }
    else if (type == 'R') {             // indikator for rad
      while (Serial.available() == 0);  // Vent til kolonneverdien er tilgjengelig
        row = Serial.read();            // Les radverdi
    }
    else if (type == 'T') {             // indikator for tekst
      String message = Serial.readStringUntil('\n');  // Les tekst til newline
      
      // Sett markøren på ønsket posisjon og skriv meldingen
      lcd.setCursor(column, row);
      lcd.print(message);
    }
    else if (type == 'C') {          // indikator for å fjerne alt på skjermen (clear)
      lcd.clear();
    }
  }
}