import threading
from time import sleep
import random
class Sensor:

    def __init__(self):
        self.prevvalue = 60

    def updatevalorHumidade(self,regar):
        if random.uniform(0,100) <= regar:
            self.prevvalue = self.prevvalue + (0.5 * 0.1)
        else:
            self.prevvalue = self.prevvalue - (0.75 * 0.1)


        if self.prevvalue >= 100:
            self.prevvalue = 100
        elif self.prevvalue <= 0:
            self.prevvalue = 0
    def valorHumidade(self):
        return self.prevvalue



