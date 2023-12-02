import threading
from time import sleep
import random
class Sensor:

    #O valor começa sempre a um valor fixo, decidi nao carregar a partir da base de dados já que este valor é essencial para o funcionamento da aplicacao
    def __init__(self):
        self.prevvalue = 60


    def updatevalorHumidade(self,regar):
        if random.uniform(0,100) <= regar:
            self.prevvalue = self.prevvalue + (0.5 * 0.1)
        else:
            self.prevvalue = self.prevvalue - (0.75 * 0.1)
        #A chance de regar é influenciada pela precipitacao


        if self.prevvalue >= 100:
            self.prevvalue = 100
        elif self.prevvalue <= 0:
            self.prevvalue = 0
            
    def valorHumidade(self):
        return self.prevvalue



