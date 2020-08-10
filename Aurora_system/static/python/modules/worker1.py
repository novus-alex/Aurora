class worker1_args:
    def __init__(self):
        self.args = []
        self.args_worker1 = open('../args/args_worker1.txt', 'r')
        self.args = self.args_worker1.readlines()
        for i in range(len(self.args)):
            self.args[i] = self.args[i].replace('\n', '')
        self.port = self.args[0]
        self.baudrate = self.args[1]
        self.timeout = self.args[2]

    def getPort(self):
        return self.port

    def getBaudrate(self):
        return self.baudrate

    def getTimeout(self):
        self.timeout = int(self.timeout)
        return self.timeout
