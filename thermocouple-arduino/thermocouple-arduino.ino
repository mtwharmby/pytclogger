/***************************************************
  This is an example for the Adafruit Thermocouple Sensor w/MAX31855K

  Designed specifically to work with the Adafruit Thermocouple Sensor
  ----> https://www.adafruit.com/products/269

  These displays use SPI to communicate, 3 pins are required to
  interface
  Adafruit invests time and resources providing this open source code,
  please support Adafruit and open-source hardware by purchasing
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include <SPI.h>
#include "Adafruit_MAX31855.h"
#include "max6675.h"

// Running on software SPI
#define MAXDO2  6
#define MAXCS2  7
#define MAXCLK2 8
#define MAXDO1   3
#define MAXCS1   4
#define MAXCLK1  5

Adafruit_MAX31855 thermocouple1(MAXCLK1, MAXCS1, MAXDO1);
MAX6675 thermocouple2(MAXCLK2, MAXCS2, MAXDO2);

// Example creating a thermocouple instance with hardware SPI
// on a given CS pin.
//#define MAXCS   10
//Adafruit_MAX31855 thermocouple(MAXCS);
// See here: https://learn.adafruit.com/circuitpython-basics-i2c-and-spi/spi-devices

void setup() {
  Serial.begin(9600);

  while (!Serial) delay(1); // wait for Serial on Leonardo/Zero, etc

  Serial.println("Stabilising thermocouple amplifiers...");
  // wait for MAX chip to stabilize
  delay(500);
  Serial.println("Initialising sensors...");
  if (!thermocouple1.begin()) {
    // Only for MAX31855 chips!
    Serial.println("ERROR: MAX31855 not ready");
    while (1) delay(10);
  }
}

void loop() {
  //Serial.print("F = ");
  //Serial.println(thermocouple.readFahrenheit());
  double temp1_c = thermocouple1.readCelsius();
  double temp2_c = thermocouple2.readCelsius();
  if (isnan(temp1_c) || isnan(temp2_c)) {
    Serial.println("ERROR: Failed to read temperature");
  } else {
   Serial.print("int_temp=");
   Serial.print(thermocouple1.readInternal());
   Serial.print(";tc1_temp=");
   Serial.print(temp1_c);
   Serial.print(";tc2_temp=");
   Serial.print(temp2_c);
   Serial.println(";");
  }
  delay(1000);
}
