import threading
from time import sleep
import random
class Sensor:

    def __init__(self):
        self.running = False
    def Run(self):
        self.running = True
        self.daemon_thread = threading.Thread(target=self.__LoopSensor, name="sensor-thread", daemon=True)
        self.daemon_thread.start()
    def Stop(self):
        self.running = False

    def __LoopSensor(self):
        while self.running:
            print(self.valorHumidade())
            sleep(1)

    def valorHumidade(self):
        return random.uniform(0,100)



