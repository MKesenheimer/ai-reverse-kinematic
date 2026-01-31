#include "Sensors.h"

Sensors::Sensors(void) {
  Wire.begin();
}

// select the input of the I2C multiplexer
void Sensors::tcaselect(uint8_t i) {
  if (i > 7) return;
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();  
}

void Sensors::init(int id) {
  Serial.print("selecting id:");
  Serial.println(id);
  tcaselect(id);
  Serial.print("initialising AS5600 id:");
  Serial.println(id);
  if(ams5600.detectMagnet() == 0){
    while(1) {
      if(ams5600.detectMagnet() == 1 ){
        Serial.print("Current Magnitude: ");
        Serial.println(ams5600.readMagnitude());
        break;
      } else {
        Serial.print("Can not detect magnet from sensor with id ");
        Serial.println(id);
      }
      delay(1000);
    }
  }
}

double Sensors::getAngle(int id) {
  if (id < 0 || id > 6) return 0;

  tcaselect(id);
  /* Raw data reports 0 - 4095 segments, which is 0.087 of a degree */
  double retVal = direction[id] * ((ams5600.rawAngle() * 0.087) - amsOffsets[id]);

  // z-Achse ist von -180° - 180° definiert:
  if (id == 0 && retVal > 180.0) retVal = retVal - 360;
  if (id == 0 && retVal < -180.0) retVal = retVal + 360;

  // alle anderen Winkel sind von 0 - 360° definiert
  if (id != 0 && retVal > 360.0) retVal = retVal - 360;
  if (id != 0 && retVal < 0) retVal = retVal + 360;

  /*Serial.print("angle(");
  Serial.print(id);
  Serial.print(") = ");
  Serial.println(retVal);*/
  return retVal;
}