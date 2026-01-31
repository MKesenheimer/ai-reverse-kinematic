#pragma once
#include "Arduino.h" 
#include <Wire.h>
#include <AS5600.h>

#define TCAADDR 0x70

class Sensors {
  public:
	  Sensors();
    void init(int);
    double getAngle(int);
  private:
    // AS5600 with address 0x36
    AS5600 ams5600;
    // AS5600L with address 0x40, address changeable with ams5600.setAddress(uint8_t address)
    //AS5600L ams5600;
    // Reihenfolge: beta, alpha1, alpha2, alpha3, ...
    double amsOffsets[6] = {30, 195, -102, 0, 0, 0};
    int direction[6] = {-1, 1, 1, 1, 1, 1};
    void tcaselect(uint8_t);
};