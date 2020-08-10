from modules.worker1 import worker1_args
from modules.worker2 import worker2_args
from modules.led_statement import led_statement
import serial
import serial.tools.list_ports
import sys
import os
import time


class raspOne_core_init_withoutConsole:
    def __init__(self):
        # Init
        # Checking Files
        if os.path.exists('modules/worker1.py'):
            pass
        else:
            sys.exit(10)

        if os.path.exists('modules/worker2.py'):
            pass
        else:
            sys.exit(10)

        # Checking workers_args
        self.args = []
        self.args_workers = open('../modules/args/args_worker2.txt', 'r')
        self.args = self.args_workers.readlines()
        for i in range(len(self.args)):
            self.args[i] = self.args[i].replace('\n', '')
        self.port = self.args[0]
        self.baudrate = self.args[1]
        self.timeout = self.args[2]

        # Checking Arduino's connection
        self.worker1_port = worker1_args().getPort()
        self.worker1_baudrate = worker1_args().getBaudrate()
        self.worker1_timeout = worker1_args().getTimeout()
        self.worker2_port = worker2_args().getPort()
        self.worker2_baudrate = worker2_args().getBaudrate()
        self.worker2_timeout = worker2_args().getTimeout()
        self.ardWorker1_port = self.worker1_port
        self.ardWorker2_port = self.worker2_port
        self.ardWorker1 = serial.Serial(port=self.ardWorker1_port, baudrate=self.worker1_baudrate,
                                        timeout=self.worker1_timeout)
        self.ardWorker2 = serial.Serial(port=self.ardWorker2_port, baudrate=self.worker2_baudrate,
                                        timeout=self.worker2_timeout)

        # Set workers state
        self.state_file = open('../../states/state_workers.txt', 'w')

    def test_connection(self):
        for i in range(1, 10):
            led_statement().rgb(0, 1, 0)
            time.sleep(0.05)
            led_statement().rgb(0, 0, 0)
            time.sleep(0.05)
        if self.ardWorker1.isOpen():
            self.ardWorker1.close()
            self.state_file.write('wokers=true')
            self.state_file.close()
        else:
            sys.exit(10)

        if self.ardWorker2.isOpen():
            self.ardWorker2.close()
        else:
            sys.exit(10)

    def getArdWrokers(self):
        return self.ardWorker1


def init():
    raspOne_core_init_withoutConsole().test_connection()


if __name__ == '__main__':
    init()
