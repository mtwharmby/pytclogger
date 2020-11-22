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

// Running on software SPI
#define MAXDO   3
#define MAXCS   4
#define MAXCLK  5
Adafruit_MAX31855 thermocouple(MAXCLK, MAXCS, MAXDO);

// Example creating a thermocouple instance with hardware SPI
// on a given CS pin.
//#define MAXCS   10
//Adafruit_MAX31855 thermocouple(MAXCS);
// See here: https://learn.adafruit.com/circuitpython-basics-i2c-and-spi/spi-devices

void setup() {
  Serial.begin(9600);

  while (!Serial) delay(1); // wait for Serial on Leonardo/Zero, etc

  Serial.println("Stabilising MAX31855...");
  // wait for MAX chip to stabilize
  delay(500);
  Serial.print("Initialising sensor...");
  if (!thermocouple.begin()) {
    Serial.println("ERROR: Thermocouple not ready");
    while (1) delay(10);
  }
}

void loop() {
  //Serial.print("F = ");
  //Serial.println(thermocouple.readFahrenheit());
  double temp_c = thermocouple.readCelsius();
  if (isnan(temp_c)) {
    Serial.println("ERROR: Failed to read temperature");
  } else {
   Serial.print("int_temp=");
   Serial.print(thermocouple.readInternal());
   Serial.print(";tc_temp=");
   Serial.print(temp_c);
   Serial.println(";");
  }
  delay(1000);
}
