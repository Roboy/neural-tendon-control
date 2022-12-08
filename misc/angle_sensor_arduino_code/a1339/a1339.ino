#include <SPI.h> //standard library


const byte ANGLE_REG = 0x20; // Angler register for A1339.
const byte TURN_REG = 0x2C; // Angler register for A1339.


const int ss_pin = 53;




void setup(void) {

  Serial.begin(9600);

 
  SPI.begin();

  pinMode(ss_pin,OUTPUT);

  //code below is attempting to read from the A1335

  SPI.beginTransaction(SPISettings(10000000, MSBFIRST, SPI_MODE3)); // start the SPI library for A1335, settings out of datasheet
  delay(100); //give A1335 sensor time to setup
  
  digitalWrite (ss_pin, HIGH); //sets select slave low to allow for communication


}


void loop(void) {
  int angle = 0;
  
  digitalWrite(ss_pin, LOW);
  delay(2);


  byte angle_msb = SPI.transfer(ANGLE_REG);
  byte angle_lsb = SPI.transfer(0x00); // useless
  
  delay(2);
  digitalWrite(ss_pin, HIGH);
 

  angle = angle_lsb + 256 * (angle_msb & 0b00001111);

  Serial.println(angle);

  delay(10);

}
