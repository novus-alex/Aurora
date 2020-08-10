# Copyright (c) 2020 Novus Space

###############################
########  Init System  ########
###############################
# UTF-8
# Only available for raspberry pi zero configuration
# Require Python3 minimum, Python3.7 or 3.8 are the best

# -----------------------------#

######### Credentials #########
# Creating for the Aurora Project, can be bought for other project but need to be adapt

from modules.worker1 import worker1_args
from modules.worker2 import worker2_args
from modules.led_statement import led_statement
from threading import Thread, Event
import serial
import serial.tools.list_ports
import sys
import os
import time
from random import *

__author__ = 'alex'
__company__ = 'Novus Space'


class Aurora_core_init:
    def __init__(self):
        # Init
        self.state = '\033[33m[core@init]\033[0m'
        sys.stdout.write(self.state + '\033[32m Starting Aurora_data_core...\033[0m')
        sys.stdout.write("\n")
        sys.stdout.write(self.state + ' Checking files..')
        sys.stdout.write("\n")
        sys.stdout.write(self.state + ' worker1.py : ')

        # Checking Files
        if os.path.exists('modules/worker1.py'):
            sys.stdout.write('\033[32mDone\033[0m')
            sys.stdout.write("\n")
        else:
            sys.stdout.write("\n")
            sys.stdout.write('\033[31mworker1.py missing !\033[0m')
            sys.exit(10)

        sys.stdout.write(self.state + ' worker2.py : ')

        if os.path.exists('modules/worker2.py'):
            sys.stdout.write('\033[32mDone\033[0m')
            sys.stdout.write("\n")
        else:
            sys.stdout.write("\n")
            sys.stdout.write('\033[31mworker2.py missing !\033[0m')
            sys.exit(10)

        # Checking workers_args
        self.args_worker1 = []
        self.args_worker_1 = open('modules/args/args_worker1.txt', 'r')
        self.args_worker1 = self.args_worker_1.readlines()
        for i in range(len(self.args_worker1)):
            self.args_worker1[i] = self.args_worker1[i].replace('\n', '')
        self.port_worker1 = self.args_worker1[0]
        self.baudrate_worker1 = self.args_worker1[1]
        self.timeout_worker1 = self.args_worker1[2]

        self.args_worker2 = []
        self.args_worker_2 = open('modules/args/args_worker2.txt', 'r')
        self.args_worker2 = self.args_worker_2.readlines()
        for i in range(len(self.args_worker2)):
            self.args_worker2[i] = self.args_worker2[i].replace('\n', '')
        self.port_worker2 = self.args_worker2[0]
        self.baudrate_worker2 = self.args_worker2[1]
        self.timeout_worker2 = self.args_worker2[2]

        sys.stdout.write(self.state + ' args_worker1.txt : ')
        sys.stdout.write('\n')
        sys.stdout.write(self.port_worker1)
        sys.stdout.write('\n')
        sys.stdout.write(self.baudrate_worker1)
        sys.stdout.write('\n')
        sys.stdout.write(self.timeout_worker1)
        sys.stdout.write('\n')
        sys.stdout.write(self.state + ' args_worker1.txt : \033[32mDone\033[0m')
        sys.stdout.write('\n')

        sys.stdout.write(self.state + ' args_worker2.txt : ')
        sys.stdout.write('\n')
        sys.stdout.write(self.port_worker2)
        sys.stdout.write('\n')
        sys.stdout.write(self.baudrate_worker2)
        sys.stdout.write('\n')
        sys.stdout.write(self.timeout_worker2)
        sys.stdout.write('\n')
        sys.stdout.write(self.state + ' args_worker2.txt : \033[32mDone\033[0m')
        sys.stdout.write('\n')

        # Checking Arduino's connection
        self.worker1_port = worker1_args().getPort()
        self.worker1_baudrate = worker1_args().getBaudrate()
        self.worker1_timeout = worker1_args().getTimeout()
        self.worker2_port = worker2_args().getPort()
        self.worker2_baudrate = worker2_args().getBaudrate()
        self.worker2_timeout = worker2_args().getTimeout()
        sys.stdout.write(self.state + ' Do you want to use port ')
        sys.stdout.write(self.worker1_port)
        sys.stdout.write("\n")
        self.response = input(self.state + ' [y/n] ')
        if self.response == 'y':
            self.ardWorker1_port = self.worker1_port
            self.ardWorker2_port = self.worker2_port
        else:
            self.ardWorker1_port = input(self.state + ' Type a new port : ')
            self.ardWorker2_port = input(self.state + ' Type a new port : ')
        self.ardWorker1 = serial.Serial(port=self.ardWorker1_port, baudrate=self.worker1_baudrate,
                                        timeout=self.worker1_timeout)
        self.ardWorker2 = serial.Serial(port=self.ardWorker2_port, baudrate=self.worker2_baudrate,
                                        timeout=self.worker2_timeout)

        # Set workers state
        self.state_file = open('../states/state_workers.txt', 'w')

    def test_connection(self):
        sys.stdout.write(self.state + ' Testing connection with Arduino (worker1) : ')
        for i in range(1, 10):
            led_statement().rgb(0, 1, 0)
            time.sleep(0.1)
            led_statement().rgb(0, 0, 0)
            time.sleep(0.1)
        if self.ardWorker1.isOpen():
            sys.stdout.write("\033[32mDone\033[0m")
            sys.stdout.write("\n")
            sys.stdout.write(self.state + " worker1 : ")
            sys.stdout.write("\033[36mconnected\033[0m")
            sys.stdout.write("\n")
            self.ardWorker1.close()
            self.state_file.write('wokers=true')
            self.state_file.close()
        else:
            sys.stdout.write("\n")
            sys.stdout.write("\033[31mCannot communicate with the Arduino !\033[0m")
            sys.exit(10)

        sys.stdout.write(self.state + ' Testing connection with Arduino (worker2) : ')
        if self.ardWorker2.isOpen():
            sys.stdout.write("\033[32mDone\033[0m")
            sys.stdout.write("\n")
            sys.stdout.write(self.state + " worker2 : ")
            sys.stdout.write("\033[36mconnected\033[0m")
            sys.stdout.write("\n")
            self.ardWorker2.close()
        else:
            sys.stdout.write("\n")
            sys.stdout.write("\033[31mCannot communicate with the Arduino !\033[0m")
            sys.exit(10)

    def getArdWrokers(self):
        return self.ardWorker1


class Aurora_core_dataManagement:
    def __init__(self):
        # Worker 1
        self.worker1_port = worker1_args().getPort()
        self.worker1_baudrate = worker1_args().getBaudrate()
        self.worker1_timeout = worker1_args().getTimeout()
        self.worker1_serial = serial.Serial(port=self.worker1_port, baudrate=self.worker1_baudrate,
                                            timeout=self.worker1_timeout)

        # Worker 2
        self.worker2_port = worker2_args().getPort()
        self.worker2_baudrate = worker2_args().getBaudrate()
        self.worker2_timeout = worker2_args().getTimeout()
        self.worker2_serial = serial.Serial(port=self.worker2_port, baudrate=self.worker2_baudrate,
                                            timeout=self.worker2_timeout)

        # Workers State
        self.state_workers_list = []
        self.state_workers = open('../states/state_workers.txt', 'r')
        self.state_workers_list = self.state_workers.readlines()
        for i in range(len(self.state_workers_list)):
            self.state_workers_list[i] = self.state_workers_list[i].replace('\n', '')
        self.state_worker1 = self.state_workers_list[0]

        # Data var
        self.data_received = self.worker1_serial.readline()
        self.rawData = self.data_received.decode('ascii')
        self.rawDataList = []
        self.radio_state = '\033[33m[radio@test]\033[0m'

        # Thread
        self.thread_state = '\033[33m[thread@init]\033[0m'
        self.thread = Thread()
        self.thread_stop_event = Event()

    def state(self):
        if self.state_worker1 == 'workers=true':
            return True

    def receive(self):
        if self.data_received < 0:
            sys.exit(10)
        else:
            pass
        sys.stdout.write(self.data_received)

    def test_radioData(self):
        sys.stdout.write(self.radio_state + " input data here : ")
        sys.stdout.write('\n')
        data = input('> ')
        self.worker1_serial.write(bytes(data, encoding='utf8'))
        sys.stdout.write(self.radio_state + ' Checking radio transmission : ')
        if self.worker1_serial.isOpen():
            sys.stdout.write("\033[32mDone\033[0m")
        else:
            sys.stdout.write("\033[31mCannot transmit data !\033[0m")

    def radioData(self, arg):
        if arg == 1:
            self.radio_state = '\033[33m[radio@shell]\033[0m'
            sys.stdout.write(self.radio_state + " welcome on the real radio shell : ")
            sys.stdout.write('\n')
        data = self.worker2_serial.readline().decode('ascii')
        if data == '':
            sys.stdout.write("\033[31mCannot transmit data ! (Check the wires)\033[0m")
            console(1)
        self.worker1_serial.write(bytes(data, encoding='utf8'))
        Aurora_core_dataManagement().radioData(2)

    def testSensor(self):
        global data
        self.radio_state = '\033[33m[sensor@test]\033[0m'
        sys.stdout.write(self.radio_state)
        sys.stdout.write('\n')
        for i in range(1, 10):
            data = self.worker2_serial.readline().decode('ascii')
            sys.stdout.write(data)
            time.sleep(1)
        if data == '':
            sys.stdout.write("\033[31mCannot transmit data ! (Check the wires)\033[0m")
            sys.stdout.write('\n')
            console(1)
        self.worker1_serial.write(bytes(data, encoding='utf8'))

    def received_data_threading(self):
        while not self.thread_stop_event.isSet():
            self.rawDataList.append(self.rawData)

    def start_threading(self):
        if not self.thread.is_alive():
            sys.stdout.write(self.thread_state + "\033[32m Starting Thread...\033[0m")
            sys.stdout.write("\n")
            sys.stdout.write(self.thread_state + "\033[32m Thread alive\033[0m")
            sys.stdout.write("\n")
            console(2)
            self.thread = Thread(target=Aurora_core_dataManagement().sending_threading())
            self.thread.start()

    def data_threading(self):
        if not self.thread.is_alive():
            sys.stdout.write(self.thread_state + "\033[32m Starting Thread...\033[0m")
            sys.stdout.write("\n")
            sys.stdout.write(self.thread_state + "\033[32m Thread alive\033[0m")
            sys.stdout.write("\n")
            console(2)
            self.thread = Thread(target=Aurora_core_dataManagement().sending_threading())
            self.thread.start()

    def sending_threading(self):
        while not self.thread_stop_event.isSet():
            data = self.worker2_serial.readline().decode('ascii')
            self.worker1_serial.write(bytes(data, encoding='utf8'))

    def check_threading(self):
        sys.stdout.write(self.thread_state + " Checking thread : ")
        if self.thread.is_alive():
            sys.stdout.write("\033[32mDone\033[0m")
            sys.stdout.write("\n")
        else:
            sys.stdout.write("\033[31m Thread is not alive !\033[0m")
            sys.stdout.write("\n")


class Aurora_TVC:
    def __init__(self):
        self.controller_port = worker2_args().getPort()
        self.controller_baudrate = worker2_args().getBaudrate()
        self.controller_timeout = worker2_args().getTimeout()
        self.controller = serial.Serial(port=self.controller_port, baudrate=self.controller_baudrate,
                                        timeout=self.controller_timeout)
        self.xaxis = '1'
        self.yaxis = '2'

    def sendCommands(self, command):
        self.controller.write(bytes(command, encoding='utf8'))

    def start_test(self, arg):
        start_tvc_test = 'start_tvc_test ' + arg
        self.sendCommands(start_tvc_test)


def console(arg):
    # Init / Info
    if arg == 1:
        sys.stdout.write('\033[36mAurora Data Core [Version 1.1.0]')
        sys.stdout.write('\n')
        sys.stdout.write('type help for more commands\033[0m')
        sys.stdout.write('\n')
    console_input = input('> ')

    # Commands
    # Help
    if console_input == 'help':
        sys.stdout.write('\033[33m[test_commands]\033[0m')
        sys.stdout.write('\n')
        sys.stdout.write('  test_connection [test connection with arduino]')
        sys.stdout.write('\n')
        sys.stdout.write('  test_radio [test sending data with radio module]')
        sys.stdout.write('\n')
        sys.stdout.write('  test_threading [test starting threading]')
        sys.stdout.write('\n')
        sys.stdout.write('  test_sensor [testing the sensors]')
        sys.stdout.write('\n')
        sys.stdout.write('\033[33m[apps_commands]\033[0m')
        sys.stdout.write('\n')
        sys.stdout.write('  radioShell [start the radio shell]')
        sys.stdout.write('\n')
        sys.stdout.write('  threadingShell [start the threading shell]')
        sys.stdout.write('\n')
        sys.stdout.write('\033[33m[shell_commands]\033[0m')
        sys.stdout.write('\n')
        sys.stdout.write('  clear [clear the shell]')
        sys.stdout.write('\n')
        sys.stdout.write('  quit [quit shell]')
        sys.stdout.write('\n')

    # Test commands
    elif console_input == 'test_connection':
        Aurora_core_init().test_connection()
    elif console_input == 'test_radio':
        Aurora_core_dataManagement().test_radioData()
        sys.stdout.write("\n")
    elif console_input == 'test_threading':
        Aurora_core_dataManagement().start_threading()
        Aurora_core_dataManagement().check_threading()
    elif console_input == 'test_sensor':
        Aurora_core_dataManagement().testSensor()

    # App commands
    elif console_input == 'radioShell':
        Aurora_core_dataManagement().radioData(1)
    elif console_input == 'threadingShell':
        Aurora_core_dataManagement().data_threading()

    # Shell management
    elif console_input == '':
        console(2)
    elif console_input == 'clear':
        os.system('clear')
        console(1)

    # Led
    elif console_input == 'led_init':
        led_statement().rgb(0, 1, 0)
    elif console_input == 'led_idle':
        led_statement().rgb(0, 0, 1)
    elif console_input == 'led_error':
        led_statement().rgb(1, 0, 0)
    elif console_input == 'led_cleanup':
        led_statement().cleanup(0)

    # Quit
    elif console_input == 'quit':
        os.system('clear')
        sys.exit(10)

    # Unknown command
    else:
        sys.stdout.write("[ " + console_input + " ] ," + "\033[31mUnknown command\033[0m")
        sys.stdout.write("\n")
    console(2)


if __name__ == '__main__':
    led_statement().cleanup(0)
    os.system('clear')
    console(1)
