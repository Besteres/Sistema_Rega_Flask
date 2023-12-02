from sensor import Sensor
from AccuWeather import AccuWeather
from time import sleep
import threading
import requests
import os
class Sistema:
    urlbase = ""
    def __init__(self,key,citykey,cityname,HumidityMin,HumidityMax,PrecipitationFile):
        self.rain = AccuWeather(key=key,citykey_file=citykey,cityname_file=cityname)
        self.cityname = self.rain.getCityName()
        self.sensor = Sensor() 
        
        self.humidityMax = HumidityMax
        self.regar = False

        self.precipitationMax = 50
        self.precipitationFile = PrecipitationFile

        self.humidityMinFile = HumidityMin
        self.humidityMin = 40

        if(os.path.exists(self.humidityMinFile)):
            with open(self.humidityMinFile,"r") as file:
                self.humidityMin = float(file.readline().strip())
        else:
            self.createFile(self.humidityMinFile,"40") #Carregado o valor minimo de humidade

        self.humidityMaxFile = HumidityMax
        self.humidityMax = 60
        if(os.path.exists(self.humidityMaxFile)):
            with open(self.humidityMaxFile,"r") as file:
                self.humidityMax = float(file.readline().strip())
        else:
            self.createFile(self.humidityMaxFile,"60") #Carregado o valor maximo de humidade

        if(os.path.exists(self.precipitationFile)):
            with open(self.precipitationFile,"r") as file:
                self.precipitationMax = float(file.readline().strip())
        else:
            self.createFile(self.precipitationFile,"50") #Carregado o valor maximo de precipitacao
        
        #Embora fazia sentido o sistema ter o logger aqui dentro, decidi seguir o codigo base e adaptar o meu codigo á volta do mesmo

        self.updateValues()

        self.daemon_thread = threading.Thread(target=self.SistemaLoop, name="values-thread", daemon=True)
        self.daemon_thread.start()

    def createFile(self,path,cont):
        with open(path,"w") as file:
            file.write(cont)

    def getCurrentMin(self): #O valor minimo onde uma rega pode começar varia muito dependente das regras definidas
        if self.currentPrecipitation <= self.precipitationMax: 
            return self.humidityMax - ((self.humidityMax-self.humidityMin)/2)#Quando o valor de precipitacao atual permite rega no valor ideal
        elif self.currentPrecipitation >= self.precipitationMax:
            return self.humidityMin #Quando o valor de precipitacao atual nao permite rega no valor ideal
        
    
    def SistemaLoop(self):
        while True:
            sleep(1)
            self.updateValues()#Atualiza todos os valores atuais (precipitacao, humidade, etc)

            if self.regar == False: #Logica se nao estiver a regar
                if self.currenthumidity <= self.humidityMin:
                    self.regar = True
                elif self.currenthumidity <= self.humidityMax - ((self.humidityMax-self.humidityMin)/2) and self.currentPrecipitation <= self.precipitationMax:
                    self.regar = True
            
            if self.regar == True: #Logica se estiver a regar
                #os dois algoritmos sao diferentes pois num pode ser permitido regar ate ao maximo
                #E noutro é so permitido ate ao valor ideal
                if self.currenthumidity >= self.humidityMax - ((self.humidityMax-self.humidityMin)/2) and self.currentPrecipitation >= self.precipitationMax:
                    self.regar = False
                elif self.currenthumidity >= self.humidityMax:
                    self.regar = False
                
    #Mudar definicoes de intervalo de humidades
    #Argumentos min e max servem para dizer se é o maximo ou minimo que mudaram
    def mudarIntervaloHumidade(self,data,min,max):
        if min:
            data["Min"] = float(data["Min"])
            if(data["Min"] <= 0):
                data["Min"] = 0
            if(data["Min"] >= 100):
                data["Min"] = 100
            self.humidityMin = data["Min"]
            with open(self.humidityMinFile,"w") as file:
                file.write(str(self.humidityMin))


        if max:
            data["Max"] = float(data["Max"])
            
            if(data["Max"] >= 100):
                data["Max"] = 100
            if(data["Max"] <= 0):
                data["Max"] = 0
            self.humidityMax = data["Max"]
            with open(self.humidityMaxFile,"w") as file:
                file.write(str(self.humidityMax))

    
        
                
    def getRuleValues(self):
        return {"Min": self.humidityMin,"Max": self.humidityMax}

    def getCityValues(self):
        print("Current City Code: " + self.rain.city)
        return {"CityName": self.cityname, "CityCode": self.rain.city}
    
    #Carregam novos valores (se aplicavel) na memoria
    #pois os valores sao buscados com getters
    def updateValues(self):
        self.currentPrecipitation = self.rain.getcurrentPrecProb()
        self.currenthumidity = self.sensor.valorHumidade()

        if self.currentPrecipitation != None:
            value = (int(self.regar) * 100) + (self.currentPrecipitation / 1.5) #Chance do valor de humidade subir calculada aqui
            self.sensor.updatevalorHumidade(value)
        else:
            self.sensor.updatevalorHumidade(int(self.regar) * 100)

    #Muda cidade e devolve novo valor (se mudado)
    #Normalmente nao muda cidade quando o nome é incompreensivel ou ja nao ha mais chamadas API
    def mudarCidade(self,nomecidade):
        result = self.rain.changeCity(nomecidade)
        if result == True:
            self.cityname = self.rain.getCityName()
        return result
    #Muda regras de precipitacao
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
    
    

