#include <SPI.h> //standard library


const byte ANGLE_REG = 0x20; // Angler register for A1339.
const byte READ = 0b11111100;

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



int tmp_data = readRegister(0x20, 2);

float angle = ((float)tmp_data / 8);

Serial.println(angle);

delay(20);

}

//Read from register from the A1335:
unsigned int readRegister(byte thisRegister, int bytesToRead) {
  byte inByte = 0;           // incoming byte from the SPI
  unsigned int result = 0;   // result to return
  
  byte dataToSend = thisRegister & READ;
  //Serial.println(thisRegister, BIN);
  // take the chip select low to select the device:
  digitalWrite(ss_pin, LOW);
  // send the device the register you want to read:
  SPI.transfer(thisRegister);
  // send a value of 0 to read the first byte returned:
  result = SPI.transfer(0x00);
  // decrement the number of bytes left to read:
  bytesToRead--;
  // if you still have another byte to read:
  if (bytesToRead > 0) {
    // shift the first byte left, then get the second byte:
    result = result << 8;
    inByte = SPI.transfer(0x00);
    // combine the byte you just got with the previous one:
    result = result | inByte;
    // decrement the number of bytes left to read:
    bytesToRead--;
  }
  // take the chip select high to de-select:
  digitalWrite(ss_pin, HIGH);
  // return the result:
  return (result);
}
