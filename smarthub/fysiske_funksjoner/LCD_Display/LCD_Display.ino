#include <LiquidCrystal.h>

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
  Serial.begin(9600);  // Sett opp samme baud rate som Raspberry Pi
  lcd.begin(16, 2);
  lcd.clear();
}

void loop() {
  if (Serial.available() > 0) {
    char type = Serial.read(); // Les datatype som blir brukt som en indikator

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
      // Rydd linjen før ny tekst
      lcd.setCursor(0, row);            // Rydd linjen før ny tekst
      lcd.print("                ");
      
      // Sett markøren på ønsket posisjon og skriv meldingen
      lcd.setCursor(column, row);
      lcd.print(message);
    }
    else if (type == 'C') {          // indikator for å fjerne alt på skjermen (clear)
      lcd.clear();
    }
  }
}