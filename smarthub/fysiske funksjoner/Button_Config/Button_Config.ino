/*
Denne koden skal
*/

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

void setup() {
  pinMode(button_setAlarm, INPUT);
  pinMode(button_visit, INPUT);
  pinMode(button_editAlarm, INPUT);
  
  Serial.begin(9600);
}

void loop() {

  setAlarm = digitalRead(button_setAlarm);
  visit = digitalRead(button_visit);
  editAlarm = digitalRead(button_editAlarm);

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

}
