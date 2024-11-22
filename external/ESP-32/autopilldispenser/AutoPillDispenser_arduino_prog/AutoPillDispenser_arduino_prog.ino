#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Stepper.h>
#include <Adafruit_NeoPixel.h>

// Definerer verdier for hardwaren
#define STEPS 200
#define BUTTON_PIN 2
#define LED_PIN 8
#define LED_COUNT 12
#define ENABLE_PIN 3
#define DONE_PIN 9
#define MOTOR_PIN_1 4
#define MOTOR_PIN_2 5
#define MOTOR_PIN_3 6
#define MOTOR_PIN_4 7

Stepper stepper(STEPS, MOTOR_PIN_1, MOTOR_PIN_2, MOTOR_PIN_3, MOTOR_PIN_4);
Adafruit_NeoPixel ring(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
LiquidCrystal_I2C lcd(0x27, 16, 2);

int motorSteps = 44;
bool reverseDirection = true;
bool buttonPressed = false;

// Tilpasset tegn for "å"
byte custom_aa[8] = {
  0b00100,
  0b00000,
  0b01110,
  0b00001,
  0b01111,
  0b10001,
  0b01111,
  0b00000
};

void setup() {
  stepper.setSpeed(60);

  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(ENABLE_PIN, INPUT);
  pinMode(DONE_PIN, OUTPUT);
  pinMode(MOTOR_PIN_1, OUTPUT);
  pinMode(MOTOR_PIN_2, OUTPUT);
  pinMode(MOTOR_PIN_3, OUTPUT);
  pinMode(MOTOR_PIN_4, OUTPUT);

  digitalWrite(DONE_PIN, LOW);

  ring.begin();
  ring.show();
  ring.setBrightness(100);

  lcd.init();
  lcd.backlight();

  // Laste opp tilpasset tegn
  lcd.createChar(0, custom_aa);

  lcd.clear();
}

void loop() {
  if (digitalRead(ENABLE_PIN) == LOW) {
    disableMotor();  // Deaktiver motor og spoler
    idleMode();      // Idle mode når enable ikke er aktiv
  } else {
    enableMode();    // Blink rødt når enable er aktiv
  }

  if (digitalRead(ENABLE_PIN) == HIGH && digitalRead(BUTTON_PIN) == LOW) {
    buttonPressed = true;
  }

  if (buttonPressed) {
    enableMotor();   // Aktiver motoren
    dispensePills(); // Håndterer dosering og lys under dosering
    buttonPressed = false;  // Resett knappstatus
    delay(30000);           // Vent 30 sekunder før maskinen tillater ny aktivering
  }
}

void idleMode() {
  static uint16_t colorIndex = 0;

  lcd.setCursor(0, 0);
  lcd.print("Ingen dosering  ");
  lcd.setCursor(0, 1);
  lcd.print("n");
  lcd.write(byte(0));  // Bruker tilpasset "å"
  lcd.print("               "); // Sørger for å fylle opp linjen

  for (int i = 0; i < ring.numPixels(); i++) {
    ring.setPixelColor(i, Wheel((i * 256 / ring.numPixels() + colorIndex) & 255));
  }
  ring.show();
  colorIndex++;
  delay(50);
}

void enableMode() {
  static bool isRed = false;

  lcd.setCursor(0, 0);
  lcd.print("Trykk for ");
  lcd.write(byte(0));  // Bruker tilpasset "å"
  lcd.print("       ");
  lcd.setCursor(0, 1);
  lcd.print("dosere medisiner ");

  for (int i = 0; i < ring.numPixels(); i++) {
    ring.setPixelColor(i, isRed ? ring.Color(255, 0, 0) : ring.Color(0, 0, 0));
  }
  ring.show();
  isRed = !isRed;
  delay(500);
}

void dispensePills() {
  lcd.setCursor(0, 0);
  lcd.print("Doserer...      ");
  lcd.setCursor(0, 1);
  lcd.print("                ");

  // Motoren flyttes for dosering
  stepper.step(reverseDirection ? -motorSteps : motorSteps);

  // Roterende grønt lys
  for (int j = 0; j < 2; j++) {
    for (int i = 0; i < ring.numPixels(); i++) {
      ring.setPixelColor(i, ring.Color(0, 255, 0));
      ring.show();
      delay(50);
      ring.setPixelColor(i, ring.Color(0, 0, 0));
    }
  }

  // Solid grønt lys etter dosering
  for (int i = 0; i < ring.numPixels(); i++) {
    ring.setPixelColor(i, ring.Color(0, 255, 0));
  }
  ring.show();

  lcd.setCursor(0, 0);
  lcd.print("Ta medisinene   ");
  lcd.setCursor(0, 1);
  lcd.print("dine!           ");

  // Hold solid grønn en kort stund
  delay(3000);

  // Send DONE-signal til ESP32
  digitalWrite(DONE_PIN, HIGH);
  delay(100);
  digitalWrite(DONE_PIN, LOW);
}

void enableMotor() {
  // Aktiver spoler
  digitalWrite(MOTOR_PIN_1, HIGH);
  digitalWrite(MOTOR_PIN_2, HIGH);
  digitalWrite(MOTOR_PIN_3, HIGH);
  digitalWrite(MOTOR_PIN_4, HIGH);
}

void disableMotor() {
  // Deaktiver spoler for å redusere varme
  digitalWrite(MOTOR_PIN_1, LOW);
  digitalWrite(MOTOR_PIN_2, LOW);
  digitalWrite(MOTOR_PIN_3, LOW);
  digitalWrite(MOTOR_PIN_4, LOW);
}

uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if (WheelPos < 85) {
    return ring.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else if (WheelPos < 170) {
    WheelPos -= 85;
    return ring.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  } else {
    WheelPos -= 170;
    return ring.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  }
}
