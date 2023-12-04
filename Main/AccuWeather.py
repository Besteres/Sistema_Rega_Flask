import os
import requests
from datetime import datetime
urlbase = "http://dataservice.accuweather.com"

class AccuWeather:
    started = False
    def __init__(self,key,citykey_file,cityname_file):
        self.timeremaining = 50 
        self.key = key
        self.citynamefile = cityname_file
        self.citykeyfile = citykey_file

        self.cityname = None #Carregar o nome da cidade se o ficheiro com o nome existir (poupado 1 API call)
        if(os.path.exists(cityname_file)):
            with open(cityname_file,"r") as file:
                self.cityname = file.readline().strip()
        else:
            self.createFile(cityname_file,"Oliveira do Hospital")
            self.cityname = "Oliveira do Hospital"
        
        if(os.path.exists(citykey_file)): #Carregar a chave da cidade se o ficheiro com a chave existir (poupado 1 API call)
            with open(citykey_file,"r") as file:
                self.city = file.readline().strip()
        else: 
            self.createFile(citykey_file,"272831")
            self.city = "272831"
        #Se algum dos dois nao existir é carregado um valor por defeito

        self.raindata = None
        self.raindata = self.getRainStats() 
        AccuWeather.started = True
    
    def createFile(self,path,cont):
        with open(path,"w") as file:
            file.write(cont)
    
    def getCityName(self):
        return self.cityname

    def getcurrentPrecProb(self):
        result = None
        list_ = self.getRainStats()
        if list_ != None:
            for data in list_:
                if datetime.strptime(data["DateTime"].split("T")[1].split("+")[0],"%H:%M:%S").hour == datetime.now().hour+1:
                    result = data["PrecipitationProbability"]
                #A partir dos dados carregados é buscado a chance de precipitacao da hora a seguir (a API devolve dados a partir da proxima hora atual)
        
        if result == None:
            list_ = self.getRainStats(bypass=True)
            if list_ != None:
                for data in list_:
                    if datetime.strptime(data["DateTime"].split("T")[1].split("+")[0],"%H:%M:%S").hour == datetime.now().hour+1:
                        result = data["PrecipitationProbability"]
        if result == None:        
            print("There was an error getting precipitation data, probably ran out of API calls")
        return result
    
    #Dados da precipitacao são carregados a partir da API (proximas 12 horas)
    def getRainStats(self,bypass=False):
        while bypass == False:
            if self.raindata != None:
                if datetime.strptime(self.raindata[0]["DateTime"].split('T')[0],"%Y-%m-%d").day == datetime.now().day:
                    return self.raindata
                elif self.timeremaining == 0:
                    return self.raindata
            break 
            #Verificar se é preciso atualizar os dados atuais ou se podemos devolver os dados na memória
        
        self.raindata = None
        try:
            r = requests.get(url = urlbase+"/forecasts/v1/hourly/12hour/"+self.city+"?apikey="+self.key)
            self.timeremaining = r.headers.get("RateLimit-Remaining")
            if r.status_code == 200:
                self.raindata = r.json()
                print("Updating RainCast... " + "Remaining updates: " + self.timeremaining)
        except Exception as e:
            print(e)
        return self.raindata
    
    #Atualizar nome da cidade, normalmente chamado com a funcao changeCity()
    def __updateCityName(self):
        if self.timeremaining == 0:
            print("Ran out of times per day")
            return
        try:
            r = requests.get(url = urlbase+"/locations/v1/"+self.city+"?apikey="+self.key)
            self.timeremaining = r.headers.get("RateLimit-Remaining")
            value = r.json()["LocalizedName"]
            self.cityname = value
            with open(self.citynamefile,"w") as file:
                file.write(self.cityname)
            print("Updating City... " + "Remaining updates: " + self.timeremaining)
        except Exception as e:
            print(e)

    #Mudar cidade a partir do argumento "name"
    def changeCity(self,name):
        if self.timeremaining == 0:
            print("Ran out of times per day")
            return False
        elif self.cityname == name:
            return True
        try:
            r = requests.get(url=urlbase+"/locations/v1/cities/search?apikey="+self.key+"&q="+name)
            self.city = r.json()[0]["Key"]
            print("City changed")
            try:
                r = requests.get(url = urlbase+"/currentconditions/v1/"+self.city+"?apikey="+self.key)
                self.timeremaining = r.headers.get("RateLimit-Remaining")
                self.currtemperature = r.json()[0]["Temperature"]["Metric"]["Value"]
                self.__updateCityName()
            except Exception as e:
                print("There was an error changing")

                print(e)
                return False
            
            with open(self.citykeyfile,"w") as file:
                file.write(self.city)
            self.raindata = self.getRainStats(bypass=True) 

            if self.raindata == None:
                return False
            
            return True
        except Exception as e:
            print("Error finding city, it probably doesnt exist")
            print(e)
        return False



