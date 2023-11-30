import os
import requests
from datetime import datetime
urlbase = "http://dataservice.accuweather.com"

class AccuWeather:
    started = False
    def __init__(self,key,citykey_file,cityname_file,timesremaintoday):
        self.timeremaining = timesremaintoday
        self.key = key
        self.citynamefile = cityname_file
        self.citykeyfile = citykey_file
        self.cityname = None
        if(os.path.exists(cityname_file)):
            with open(cityname_file,"r") as file:
                self.cityname = file.readline().strip()
        else:
            self.createFile(cityname_file,"Oliveira do Hospital")
            self.cityname = "Oliveira do Hospital"
        
        if(os.path.exists(citykey_file)):
            with open(citykey_file,"r") as file:
                self.city = file.readline().strip()
        else:
            self.createFile(citykey_file,"272831")
            self.city = "272831"

        self.raindata = None
        self.raindata = self.getRainStats()
        AccuWeather.started = True
    
    def createFile(self,path,cont):
        with open(path,"w") as file:
            file.write(cont)
    
    def getCityName(self):
        return self.cityname

    def getcurrentPrecProb(self):
        #2023-11-30T05:00:00+00:00
        
        if self.raindata != None:
            #print("Start")
            for data in self.raindata:
                
                if datetime.strptime(data["DateTime"].split("T")[1].split("+")[0],"%H:%M:%S").hour == datetime.now().hour+1:
                    return data["PrecipitationProbability"]
            #self.raindata
            #if datetime.strptime(self.raindata["DateTime"].split("T")[1].split("+")[0],"%H:%M:%S").hour == datetime.now().hour:
            #    return self.raindata["PrecipitationProbability"]
        return None
        

    def getRainStats(self):

        if self.raindata != None:
            if datetime.strptime(self.raindata[0]["DateTime"].split('T')[0],"%Y-%m-%d").day == datetime.now().day and self.getcurrentPrecProb() != None:
                return self.raindata
            elif self.timeremaining == 0:
                return self.raindata
        

        try:
            r = requests.get(url = urlbase+"/forecasts/v1/hourly/12hour/"+self.city+"?apikey="+self.key)
            self.timeremaining = r.headers.get("RateLimit-Remaining")
            self.raindata = r.json()

            print("Updating RainCast... " + "Remaining updates: " + self.timeremaining)
            print(self.raindata)
        except:
            print("There was an error")
        return self.raindata
    
    def __updateCityName(self):
        r = requests.get(url = urlbase+"/locations/v1/"+self.city+"?apikey="+self.key)
        self.timeremaining = r.headers.get("RateLimit-Remaining")
        value = r.json()["LocalizedName"]
        self.cityname = value
        with open(self.citynamefile,"w") as file:
            file.write(self.cityname)
        print("Updating City... " + "Remaining updates: " + self.timeremaining)

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
                self.__updateCityName()
            except:
                print("There was an error changing")
                return False
            
            with open(self.citykeyfile,"w") as file:
                file.write(self.city)
            return True
        except:
            print("There was an error")
        return False



