import os
import requests
from datetime import datetime
urlbase = "http://dataservice.accuweather.com"

class Temperatura:
    started = False
    def __init__(self,key,citykey_file,timesremaintoday):
        self.timeremaining = timesremaintoday
        self.key = key
        if(os.path.exists(citykey_file)):
            with open(citykey_file,"r") as file:
                self.city = file.readline().strip()
        else:
            self.createFile(citykey_file)
            self.city = "272831"
        self.currtemperature = 0
        self.lastupdatedminute = -50
        self.currtemperature = self.updateTemp()
        Temperatura.started = True
    
    def createFile(self,path):
        with open(path,"w") as file:
            file.write("272831")
        

    def getTemp(self):
        return self.currtemperature
    
    def getCityName(self):
        r = requests.get(url = urlbase+"/locations/v1/"+self.city+"?apikey="+self.key)
        self.timeremaining = r.headers.get("RateLimit-Remaining")
        value = r.json()["LocalizedName"]
        return value


    def updateTemp(self):
        if self.timeremaining == 0:
            return self.currtemperature
        print("Trying To Update on time " + str(datetime.now().minute))
        access = False
        minutes = datetime.now().minute
        if (minutes == 30 or minutes == 00) and self.lastupdatedminute != minutes:
            access = True
            print("Access true!")
            self.lastupdatedminute = minutes

        if access == False and Temperatura.started == True:
            return self.currtemperature
        
        

        try:
            r = requests.get(url = urlbase+"/currentconditions/v1/"+self.city+"?apikey="+self.key)
            self.timeremaining = r.headers.get("RateLimit-Remaining")
            self.currtemperature = r.json()[0]["Temperature"]["Metric"]["Value"]
            print("Updating Temperature... " + "Remaining updates: " + self.timeremaining)
        except:
            print("There was an error")
        return self.currtemperature
    

    def changeCity(self,name):
        if self.timeremaining == 0:
            print("Ran out of times per day")
            return False
        try:
            r = requests.get(url=urlbase+"/locations/v1/cities/search?apikey="+self.key+"&q="+name)
            self.city = r.json()[0]["Key"]
            print("City changed")
            try:
                r = requests.get(url = urlbase+"/currentconditions/v1/"+self.city+"?apikey="+self.key)
                self.timeremaining = r.headers.get("RateLimit-Remaining")
                self.currtemperature = r.json()[0]["Temperature"]["Metric"]["Value"]
                print("Updating Temperature... " + "Remaining updates: " + self.timeremaining)
            except:
                print("There was an error changing")
                return False
            return True
        except:
            print("There was an error")
        return False



