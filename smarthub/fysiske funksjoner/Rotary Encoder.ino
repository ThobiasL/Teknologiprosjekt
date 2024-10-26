/*

*/

int pinA = 3; // Connected to CLK on KY-040
int pinB = 4; // Connected to DT on KY-040
int encoderPosCount = 0;
int pinALast;
int aVal;
boolean bCW;

void setup() {
  pinMode (pinA,INPUT);
  pinMode (pinB,INPUT);

  pinALast = digitalRead(pinA);
  Serial.begin (9600);
}

void loop() {
  aVal = digitalRead(pinA);
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
}
