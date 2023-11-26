from .sensor import Sensor
from .temperatura import Temperatura
from time import sleep
import threading
import requests
class Sistema:
    urlbase = ""
    def __init__(self,key,citykey,timesremain,HumidityMin,HumidityMax):
        self.temp = Temperatura(key=key,citykey_file=citykey,timesremaintoday=timesremain)
        self.cityname = self.temp.getCityName()
        self.sensor = Sensor()
        self.updateValues()
        self.humidityMin = HumidityMin
        self.humidityMax = HumidityMax
        self.regar = False
        self.daemon_thread = threading.Thread(target=self.SistemaLoop, name="values-thread", daemon=True)
        self.daemon_thread.start()


    def SistemaLoop(self):
        while True:
            sleep(15)
            self.updateValues()
            if self.regar == True:
                if(self.currenthumidity >= self.humidityMax):
                    self.regar = False
            elif(self.currenthumidity <= self.humidityMin):
                self.regar = True
                
    def getRuleValues(self):
        return {"Min": self.humidityMin,"Max": self.humidityMax}

    def getCityValues(self):
        print("Current City Code: " + self.temp.city)
        return {"CityName": self.cityname, "CityCode": self.temp.city}
    def updateValues(self):
        self.currenttemperature = self.temp.updateTemp()
        self.currenthumidity = self.sensor.valorHumidade()
        #r = requests.post(url = Sistema.urlbase+"/uploadvalues",json={"Temperatura":self.currenttemperature,"Humidade":self.currenthumidity})

    def mudarCidade(self,nomecidade):
        result = self.temp.changeCity(nomecidade)
        if result == True:
            self.cityname = self.temp.getCityName()
        return result
    
    def getValues(self):
        if(self.currenthumidity == None):
            self.updateValues()
        return {"Temperatura":self.currenttemperature,"Humidade":self.currenthumidity}
    
    

