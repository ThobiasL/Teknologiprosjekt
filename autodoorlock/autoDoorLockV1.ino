/* dette er en test for maskinvaren til den automatiske dørlåsen, 
denne koden vil vidreutvikles med funksjonene for å styre låsen både manuellt via "knapper" og automatisk via webapp/hovedenheten i prosjektet*/

#include <Servo.h>

Servo myservo; 

int pos = 0;

//definerer knpper for lås/lås opp
const int lockButton = 1;
const int unlockButton = 2;

// variabler for status til knappene
int lockButtonState = 0;
int unlockButtonState = 0;


void setup() {

  
  // velger pinnen control på servo skal kobles til
  myservo.attach(5);
  // servo står stille
  myservo.write(90);

  //definerer kanpper for lås og lås opp

}

void loop() {
  // Servo spins forward at full speed for 1 second.
  myservo.write(360);
  delay(1000);
  // Servo is stationary for 1 second.
  myservo.write(0);
  delay(1000);

}