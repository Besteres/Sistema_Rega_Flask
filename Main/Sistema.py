from sensor import Sensor
from AccuWeather import AccuWeather
from time import sleep
import threading
import requests
import os
class Sistema:
    urlbase = ""
    def __init__(self,key,citykey,cityname,timesremain,HumidityMin,HumidityMax,PrecipitationFile):
        self.rain = AccuWeather(key=key,citykey_file=citykey,cityname_file=cityname,timesremaintoday=timesremain)
        self.cityname = self.rain.getCityName()
        self.sensor = Sensor()
        self.humidityMin = HumidityMin
        self.humidityMax = HumidityMax
        self.regar = False

        self.precipitationMax = 50
        self.precipitationFile = PrecipitationFile

        if(os.path.exists(self.precipitationFile)):
            with open(self.precipitationFile,"r") as file:
                self.precipitationMax = float(file.readline().strip())
        else:
            self.createFile(self.precipitationFile,"50")
        

        self.updateValues()
        self.daemon_thread = threading.Thread(target=self.SistemaLoop, name="values-thread", daemon=True)
        self.daemon_thread.start()

    def createFile(self,path,cont):
        with open(path,"w") as file:
            file.write(cont)

    def getCurrentMin(self):
        if self.currentPrecipitation <= self.precipitationMax:
            return self.humidityMax - ((self.humidityMax-self.humidityMin)/2)
        elif self.currentPrecipitation >= self.precipitationMax:
            return self.humidityMin
    def SistemaLoop(self):
        while True:
            sleep(1)
            self.updateValues()

            if self.regar == False:
                if self.currenthumidity <= self.humidityMin:
                    self.regar = True
                elif self.currenthumidity <= self.humidityMax - ((self.humidityMax-self.humidityMin)/2) and self.currentPrecipitation <= self.precipitationMax:
                    self.regar = True
            
            if self.regar == True:
                #35 >= (60-40)
                if self.currenthumidity >= self.humidityMax - ((self.humidityMax-self.humidityMin)/2) and self.currentPrecipitation >= self.precipitationMax:
                    self.regar = False
                elif self.currenthumidity >= self.humidityMax:
                    self.regar = False
                

    def mudarIntervaloHumidade(self,data):
        data["Min"] = float(data["Min"])
        data["Max"] = float(data["Max"])
        if(data["Min"] <= 0):
            data["Min"] = 0
        if(data["Max"] >= 100):
            data["Max"] = 100
        if(data["Max"] <= 0):
            data["Max"] = 0
        if(data["Min"] >= 100):
            data["Min"] = 100
        self.humidityMin = data["Min"]
        self.humidityMax = data["Max"]

        
                
    def getRuleValues(self):
        return {"Min": self.humidityMin,"Max": self.humidityMax}

    def getCityValues(self):
        print("Current City Code: " + self.rain.city)
        return {"CityName": self.cityname, "CityCode": self.rain.city}
    
    def updateValues(self):
        self.currentPrecipitation = self.rain.getcurrentPrecProb()
        self.currenthumidity = self.sensor.valorHumidade()

        #print(str(self.regar) + " " + str(self.currentPrecipitation >= 50))
        if self.currentPrecipitation != None:
            value = (int(self.regar) * 100) + (self.currentPrecipitation / 1.5)
            self.sensor.updatevalorHumidade(value)
        else:
            self.sensor.updatevalorHumidade(int(self.regar) * 100)
        #r = requests.post(url = Sistema.urlbase+"/uploadvalues",json={"Temperatura":self.currenttemperature,"Humidade":self.currenthumidity})

    def mudarCidade(self,nomecidade):
        result = self.rain.changeCity(nomecidade)
        if result == True:
            self.cityname = self.rain.getCityName()
        return result
    def mudarPrecipitacaoMax(self,data):
        data = float(data)
        if data >= 100:
            data = 100
        if data <= 0:
            data = 0
        self.precipitationMax = data
        with open(self.precipitationFile,"w") as file:
            file.write(str(self.precipitationMax))



    def getCurrentValues(self):
        if(self.currenthumidity == None):
            self.updateValues()
        return {"Precipitation":self.currentPrecipitation,"Humidade":self.currenthumidity}
    
    

