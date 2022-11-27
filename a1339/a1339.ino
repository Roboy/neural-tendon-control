#include <SPI.h> //standard library


const byte ANGLE_REG = 0x20; // Angler register for A1339.

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

  
  SPI.transfer(ANGLE_REG);
  byte angle_msb = SPI.transfer(0x00);
  byte angle_lsb = SPI.transfer(0x00);
  
  //angle_lsb = angle_lsb & 0b11110000; // mask off flags
  //angle_msb = angle_msb & 0b00001111; // mask off flags
  angle = angle_msb;
  
  
  //angle = angle << 8;
  //angle = angle | angle_msb;

  delay(2);

  digitalWrite(ss_pin, HIGH);


  Serial.println(angle);
  
  delay(20);

}
