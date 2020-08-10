/* Copyright (c) 2020 Novus Space */

///////////////////////////////////
////  Radio Transmission Code  ////
///////////////////////////////////

#include <SPI.h>  
#include "RF24.h"

RF24 myRadio (9, 10);
byte addresses[][6] = {"0"};

struct package {
  int id = 1;
  float temperature = 18.3;
  char  text[300] = " ";
};


typedef struct package Package;
Package dataRecieve;
Package dataTransmit;

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  myRadio.begin();  
  myRadio.setChannel(115); 
  myRadio.setPALevel(RF24_PA_MAX);
  myRadio.setDataRate( RF24_250KBPS );
  
  myRadio.openReadingPipe(1, addresses[0]);
  myRadio.startListening();
}

void loop() {
  if ( myRadio.available()) {
    while (myRadio.available()){
      myRadio.read( &dataRecieve, sizeof(dataRecieve) );
    }
    Serial.println(dataRecieve.text);
    Serial.print("\n");
  }

  delay(1000);

  myRadio.stopListening();
  dataTransmit.id = dataTransmit.id + 1;
  dataTransmit.temperature = dataTransmit.temperature+0.1;
  char inData[300];
  int index = 0;
  while (Serial.available() >= 1) {
    if (index < 500) {
      inData[index] = Serial.read();
      index++;
      inData[index] = '\0';
      sprintf(dataTransmit.text, "%s", inData);
    }
  }
  myRadio.openWritingPipe(addresses[0]);
  myRadio.write(&dataTransmit, sizeof(dataTransmit));
  myRadio.openReadingPipe(1, addresses[0]);
  myRadio.startListening();
}
