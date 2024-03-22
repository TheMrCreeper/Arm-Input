#include <ArxContainer.h>
#include <Timer.h>
#include <TimerOne.h>
//#include <BraccioV2.h>
#include <Braccio.h>
using namespace arx::stdx;

#define TIMER_FREQ 10

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

// Variablen zur Speicherung der Werte
int values[] = {0, 0, 0, 0, 0, 0, 0}; // Initialisierung mit 7 Nullen

// Arrays für Variablennamen
const char* axisNames[] = {"Axis_0", "Axis_1", "Axis_2", "Axis_3", "Axis_4", "Axis_5"};
int axes[] = {0, 0, 0, 0, 0, 0, 0}; // Zeiger auf die Variablen

void parseInput(String str) {
    vector<String> v;
    int startIndex = 0;

    for (int i = 0; i < str.length(); ++i) {
        if (str[i] == ',') {
            v.push_back(str.substring(startIndex, i));
            startIndex = i + 1;
        }
    }
    v.push_back(str.substring(startIndex)); // Letztes Element hinzufügen

    // Überprüfen, ob genügend Werte vorhanden sind
    if (v.size() == 7) {
        for (int i = 0; i < 6; ++i) {
            int val = v[i].toInt();
            // Prüfen, ob der Wert im Bereich von 0 bis 100 liegt
            if (i == 4 || i == 5) {
                values[i] = constrain(val, 0, 100); // Begrenzung auf den Bereich 0-100
            } else {
                values[i] = constrain(val, -100, 100); // Begrenzung auf den Bereich -100 bis 100
            }
            if (i == 4){
              values[i] = values[i] * -1;
            
            }
            axes[i] = values[i]/TIMER_FREQ;
            }

          axes[6] = values[6];


    } else {
        Serial.println("Ungültiges Eingabeformat!");
    }
}

void Servomove(){
  Braccio.ServoMovementRelativeImmediate(axes[0], axes[1], axes[2], axes[3], axes[4] + axes[5],axes[6]);
  Serial.println(axes[0]);
  Serial.println(axes[1]);
  Serial.println(axes[2]);
  Serial.println(axes[3]);
  Serial.println(axes[4]);
  Serial.println(axes[5]);
  Serial.println(axes[6]);
  //arm.updateImmediate();
    

  //Bracio

}

void setup() {
  Timer1.initialize(1000000/TIMER_FREQ);
    // Initialisierung der seriellen Kommunikation
  Serial.begin(9600);
  Timer1.attachInterrupt(Servomove);
  
  //arm.setJointCenter(WRIST_ROT, 80);
  //arm.setJointCenter(WRIST, 90);
  //arm.setJointCenter(ELBOW, 80);
  //arm.setJointCenter(SHOULDER, 85);
  //arm.setJointCenter(BASE_ROT, 118);
  //arm.setJointCenter(GRIPPER, 50);
  //arm.setJointMax(GRIPPER, 65);//Gripper closed, can go further, but risks damage to servos
  //arm.setJointMin(GRIPPER, 15);//Gripper open, can't open further
  
  Braccio.begin();
  Timer1.start();

}

void loop() {
    // Überprüfen, ob Daten verfügbar sind
    if (Serial.available() > 0) {
        // Lesen der Daten bis zum Zeilenumbruch
        String input = Serial.readStringUntil('\n');

        // Entfernen des Zeilenumbruchs
        input.trim();

        // Daten verarbeiten
        parseInput(input);

        /* 
        for (int i = 0; i < 6; ++i) {
            Serial.print(axisNames[i]);
            Serial.print(": ");
            Serial.println(*axes[i]);
        */
        
    }
}
