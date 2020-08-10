#include <Servo.h>
#include "I2Cdev.h"
#include "MPU6050.h"

#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

MPU6050 accelgyro;

int16_t AcX,AcY,AcZ,GyX,GyroY,GyroZ;

#define OUTPUT_READABLE_ACCELGYRO
bool blinkState = false;

Servo servox;
Servo servoy;

int pos = 0;
int xmid = 125;
int ymid = 30;
int pitch;
int accAngleX;
int accAngleY;
int yaw;
int GyroX;
int gyroAngleX;
int gyroAngleY;
int valueX;
int valueY;

float elapsedTime, currentTime, previousTime;
float kp = 1;
float ki = 1;
float kd = 1;

void setup() {
  Serial.begin(9600);
  servoy.attach(14);
  servox.attach(12);
  servox.write(xmid);
  servoy.write(ymid);
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
      Wire.begin();
  #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
      Fastwire::setup(400, true);
  #endif
  accelgyro.initialize();
 
}

void loop() {
  filter();
  map();
  previousTime = currentTime;        
  currentTime = millis();            
  elapsedTime = (currentTime - previousTime) / 1000; 
  accAngleX = (atan(AcY / sqrt(pow(AcX, 2) + pow(AcZ, 2))) * 180 / PI) - 0.58;
  accAngleY = (atan(-1 * AcX / sqrt(pow(AcY, 2) + pow(AcZ, 2))) * 180 / PI) + 1.58;
 
  accelgyro.getMotion6(&AcX, &AcY, &AcZ, &GyX, &GyroY, &GyroZ);
  
  gyroAngleX = gyroAngleX + GyroZ * elapsedTime;
  gyroAngleY = gyroAngleY + GyroY * elapsedTime;

}

void filter () {
 Serial.print(GyroX);
 pitch = 0.9 * gyroAngleX + 0.1 * accAngleX;
 yaw = 0.9 * gyroAngleY + 0.1 * accAngleY;
}

void map () {
 valueY = map(yaw, -2000, 2000, 0, 50);
 valueX = map(pitch, -2000, 2000, 70, 150);
 servox.write(valueX);
 servoy.write(valueY); 
}
