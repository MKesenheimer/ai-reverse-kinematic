#include <AccelStepper.h>
#include <MultiStepper.h>
#include <TimerThree.h>
#include <GCodeParser.h>
#include "Sensors.h"

// Kalibrierung:
// 1. Zeile 223 (msteppers.moveTo(sollWert);) auskommentieren
// 2. sollWert in Zeile 17 auf Null setzen.
// 3. Nullpositionen bestimmen: Roboterarm auf seine Nullposition stellen, und dabei die motorPosition auslesen (siehe Zeile 217).
// 4. Nullpositionen in sollWert eintragen (Zeile 17)
// 5. Zeile 223 wieder einkommentieren

AccelStepper steppers[6];
MultiStepper msteppers;
int incomingByte = 0; // for incoming serial data
long sollWert[6] = {-53, 1087, 2861, 0, 0, 0}; 
long stepsPerFullTurn[6] = {16000, 16000, 16000, 16000, 16000, 16000};
GCodeParser GCode = GCodeParser();
//static double angle = 0;
int tokenPos = 0;
char token[10];
char whichAxis = NULL;
float moveTime = 0;
bool oldRun = false;
unsigned long delaytime = millis();

// tuning (Z, A, B, C, D, E)
double kp[6] = {0.1, 0.1, 0.1, 0, 0, 0};
double ki[6] = {0, 0, 0, 0, 0, 0};
double kd[6] = {0, 0, 0, 0, 0, 0};
double acc[6] = {0, 0, 0, 0, 0, 0};
double last[6] = {0, 0, 0, 0, 0, 0};

Sensors sensors;
// for optimization
const size_t numberOfSensors = 3;
const size_t numberOfMotors  = 3;

AccelStepper newStepper(int stepPin, int dirPin, int enablePin) {
  AccelStepper stepper = AccelStepper(stepper.DRIVER, stepPin,dirPin);
  stepper.setEnablePin(enablePin);
  stepper.setPinsInverted(false, false, true);
  stepper.setMaxSpeed(1200);
  stepper.setAcceleration(2000);
  stepper.enableOutputs();
  return stepper;
}

void setup() {
  while(!Serial);
  Serial.begin(115200);
  // init steppers based on RAMPS 1.4 pins
  steppers[0] = newStepper(26, 28, 24);
  steppers[1] = newStepper(36, 34, 30);
  steppers[2] = newStepper(54, 55, 38);
  steppers[3] = newStepper(60, 61, 56);
  steppers[4] = newStepper(32, 47, 45);
  steppers[5] = newStepper(46, 48, 62);

  msteppers.addStepper(steppers[0]);
  msteppers.addStepper(steppers[1]);
  msteppers.addStepper(steppers[2]);
  msteppers.addStepper(steppers[3]);
  msteppers.addStepper(steppers[4]);
  msteppers.addStepper(steppers[5]);

  // init all the position sensors
  sensors = Sensors();
  for (int i=0; i<numberOfSensors; i++) {
    sensors.init(i);
  }

  // run stepper motors every 0.5ms
  Timer3.initialize(500);
  Timer3.attachInterrupt(runSteppers);

  for (int i = 0; i < 6; ++i) {
    steppers[i].setCurrentPosition(sollWert[i]);
  }
}

void runSteppers(void) {
  msteppers.run();
}

void moveDegrees(int stepper, double degrees) {
  if (stepper < numberOfMotors) {
    Serial.print("Moving stepper ");
    Serial.print(stepper);
    Serial.print(" ");
    Serial.print(degrees);
    Serial.println(" degrees");
    double stepPos = stepsPerFullTurn[stepper] * degrees / 360.0 ;
    sollWert[stepper] = (long)stepPos;
  }
}

void readSerial() {
  if (Serial.available() > 0) {
    if (GCode.AddCharToLine(Serial.read())) {
      GCode.ParseLine();
      GCode.RemoveCommentSeparators();
      //Serial.println(GCode.line);
 
      if (GCode.HasWord('G')) {
        // shoulder yaw (beta)
        if (GCode.HasWord('Z')) {
          double angle = (double)GCode.GetWordValue('Z');
          moveDegrees(0, angle);
          if (GCode.HasWord('F')) {
            int feedrate = (int)GCode.GetWordValue('F');
            steppers[0].setMaxSpeed(feedrate);
          }
          Serial.println("ok");
        }
        
        // shoulder pitch (angle1)
        if (GCode.HasWord('A')) {
          double angle = (double)GCode.GetWordValue('A');
          moveDegrees(1, angle);
          if (GCode.HasWord('F')) {
            int feedrate = (int)GCode.GetWordValue('F');
            steppers[1].setMaxSpeed(feedrate);
          }
          Serial.println("ok");
        }

        // elbow (angle2)
        if (GCode.HasWord('B')) {
          double angle = (double)GCode.GetWordValue('B');
          moveDegrees(2, angle);
          if (GCode.HasWord('F')) {
            int feedrate = (int)GCode.GetWordValue('F');
            steppers[2].setMaxSpeed(feedrate);
          }
          Serial.println("ok");
        }

        // wrist (angle3)
        if (GCode.HasWord('C')) {
          double angle = (double)GCode.GetWordValue('C');
          moveDegrees(3, angle);
          if (GCode.HasWord('F')) {
            int feedrate = (int)GCode.GetWordValue('F');
            steppers[3].setMaxSpeed(feedrate);
          }
          Serial.println("ok");
        }

        // wrist (angle4)
        if (GCode.HasWord('D')) {
          double angle = (double)GCode.GetWordValue('D');
          moveDegrees(4, angle);
          if (GCode.HasWord('F')) {
            int feedrate = (int)GCode.GetWordValue('F');
            steppers[4].setMaxSpeed(feedrate);
          }
          Serial.println("ok");
        }
      }

      if (GCode.HasWord('M')) {
        if (GCode.HasWord('Z')) {
          Serial.println(sensors.getAngle(0));
          Serial.println("ok");
        }

        if (GCode.HasWord('A')) {
          Serial.println(sensors.getAngle(1));
          Serial.println("ok");
        }

        if (GCode.HasWord('B')) {
          Serial.println(sensors.getAngle(2));
          Serial.println("ok");
        }

        if (GCode.HasWord('C')) {
          Serial.println(sensors.getAngle(3));
          Serial.println("ok");
        }

        if (GCode.HasWord('D')) {
          Serial.println(sensors.getAngle(4));
          Serial.println("ok");
        }
      }
    }
  }
}

void loop() {
  readSerial();

  if (millis() - delaytime > 10) {
    //Serial.print("diff = ");
    for (int i=0; i<numberOfMotors; i++) {
      double sensorPosition = 0;
      double diff = 0;
      double istWert = steppers[i].currentPosition();
      double der = 0;
      if (i<numberOfSensors) {
        sensorPosition = sensors.getAngle(i) * stepsPerFullTurn[i] / 360.0;
        
        // pid correction
        diff = sensorPosition - istWert;
        acc[i] += diff;
        der = last[i] - diff;
        last[i] = diff;

        //Serial.print(diff);
        //Serial.print(" ");
      }
      steppers[i].setCurrentPosition(istWert + kp[i] * diff + ki[i] * acc[i] + kd[i] * der);

      //if (i == 0) {
      //  Serial.print(i);
      //  Serial.print(" = ");
      //  Serial.println(istWert);
      //}
    }
    msteppers.moveTo(sollWert);
    //Serial.println();
  }
}