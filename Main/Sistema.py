from sensor import Sensor
from AccuWeather import AccuWeather
from time import sleep
import threading
import requests
class Sistema:
    urlbase = ""
    def __init__(self,key,citykey,cityname,timesremain,HumidityMin,HumidityMax):
        self.rain = AccuWeather(key=key,citykey_file=citykey,cityname_file=cityname,timesremaintoday=timesremain)
        self.cityname = self.rain.getCityName()
        self.sensor = Sensor()
        self.humidityMin = HumidityMin
        self.humidityMax = HumidityMax
        self.regar = False
        self.updateValues()
        self.daemon_thread = threading.Thread(target=self.SistemaLoop, name="values-thread", daemon=True)
        self.daemon_thread.start()


    def SistemaLoop(self):
        while True:
            sleep(1)
            self.updateValues()

            if self.regar == False:
                if self.currenthumidity <= self.humidityMin:
                    self.regar = True
                elif self.currenthumidity <= (self.humidityMax-self.humidityMin) and self.currentPrecipitation <= 50:
                    self.regar = True
            
            if self.regar == True:
                if self.currenthumidity >= (self.humidityMax-self.humidityMin) and self.currentPrecipitation >= 50:
                    self.regar = False
                elif self.currenthumidity >= self.humidityMax:
                    self.regar = False
                

            

        
                
    def getRuleValues(self):
        return {"Min": self.humidityMin,"Max": self.humidityMax}

    def getCityValues(self):
        print("Current City Code: " + self.rain.city)
        return {"CityName": self.cityname, "CityCode": self.rain.city}
    
    def updateValues(self):
        self.currentPrecipitation = self.rain.getcurrentPrecProb()
        self.currenthumidity = self.sensor.valorHumidade()

        print(str(self.regar) + " " + str(self.currentPrecipitation >= 50))
        if self.currentPrecipitation != None:
            self.sensor.updatevalorHumidade(self.regar or self.currentPrecipitation >= 50)
        else:
            self.sensor.updatevalorHumidade(self.regar)
        #r = requests.post(url = Sistema.urlbase+"/uploadvalues",json={"Temperatura":self.currenttemperature,"Humidade":self.currenthumidity})

    def mudarCidade(self,nomecidade):
        result = self.rain.changeCity(nomecidade)
        if result == True:
            self.cityname = self.rain.getCityName()
        return result
    
    def getCurrentValues(self):
        if(self.currenthumidity == None):
            self.updateValues()
        return {"Precipitation":self.currentPrecipitation,"Humidade":self.currenthumidity}
    
    

