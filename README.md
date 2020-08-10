# Aurora
Aurora project, started in 2019.
This project is based on self-learning to build an autonomous rocket.
To use those files, make sure to got 2 Arduino boards, 1 Raspberry-pi (I used Raspberry-pi zero w), Python3.0 minimum and those libraries (Flask, SocketIO, Serial and other you could see in the attach text) and Arduino's libraries

So you will need Arduino software, if you want you can go to the dowload page [here](https://www.arduino.cc/en/Main/Software)

Thanks to Teo, Trystan to help me in this project

## Aurora 3D files
Those files was created on Fusion360, please comment if you want the Fusion360 files
To print it, I used PLA basic (like Amazon Basic PLA, Nozzle Temp. 190-220°C and Bed Temp. 40-55°C)

## Aurora TVC
Thrust Vectoring Control system of Aurora is built on Arduino's Servo (you will need 2 of them).

Libraries required
```c++
#include <Servo.h>
#include "I2Cdev.h"
#include "MPU6050.h"

#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif
```
This system relies on iterations to adjust its trajectory, so you may have to make changes to the Servo calibration to adapt it to your system.
