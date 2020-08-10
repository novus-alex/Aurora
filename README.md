# Aurora
Aurora project, started in 2019.
This project is based on self-learning to build an autonomous rocket.
To use those files, make sure to got 2 Arduino boards, 1 Raspberry-pi (I used Raspberry-pi zero w), Python3.0 minimum and those libraries (Flask, SocketIO, Serial and other you could see in the attach text) and Arduino's libraries

So you will need Arduino software, if you want you can go to the dowload page [here](https://www.arduino.cc/en/Main/Software)

Thanks to Teo, Trystan to help me in this project

## Aurora 3D files
Those files was created on Fusion360.

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

## Aurora radio
The radio system is built for NRF24L01 Arduino's modules, you can change it but you will need to change the programm
Make sure your radio module can transmit more than minimum 500 meters

Libraries required
```c++
#include <SPI.h>  
#include "RF24.h"
```

## Aurora sensors
The sensors used are BMP180 and MPU-6050.

MPU-6050 is used in the TVC system too, he can transmit Gyro and Acc data.

BMP180 can transmit Alt and Baro data.

Libraries required
```c++
#include <SFE_BMP180.h>
#include <Wire.h>
#include "I2Cdev.h"
#include "MPU6050.h"
```

## Aurora server
The Aurora rocket got a web server to receive all the data and plot them.
You need another Arduino board to do the radio receiver.

The web server is built on Flask and SocketIO Python's modules

Libraries required
```python
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context, send_file, request, jsonify, redirect
from random import random
from time import sleep
from threading import Thread, Event
import serial
```

## Aurora system
The Aurora main system is built for Raspberry-pi (I got Raspberry-pi zero w for this project) in Python3.0 minimum.

The Raspberry-pi is the manager of the 2 Arduino boards, he receive the datya from one of them and transmit to the other to optimize the job.

You can change the Port, Baudrate and Timeout of the Arduino boards in the files Aurora_system/static/python/modules/args/args_worker1.txt and Aurora_system/static/python/modules/args/args_worker2.txt

Libraries required
```python
from threading import Thread, Event
import serial
import serial.tools.list_ports
import sys
import os
import time
from random import *
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[Novus Space](https://novussapce.inovaperf.me/License.html)
