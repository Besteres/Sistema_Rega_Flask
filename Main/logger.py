
import threading
import datetime
import csv
import os
from sensor import Sensor
from AccuWeather import AccuWeather
from time import sleep
from Sistema import Sistema
import psycopg2
from sklearn.linear_model import LinearRegression
import numpy as np
import pred_test


key = "NK6kGCNYAE2l1Dhu8Jv775xKd1SPCEpk"



class Logger(object):
    saveDB = True
    def __init__(self, filename='data.csv'):
        
        self.sistema = Sistema(key=key,citykey="currentcityKey.txt",cityname="currentcityName.txt",HumidityMin="HumidityMin.txt",HumidityMax="HumidityMax.txt",PrecipitationFile="PrecipitationMax.txt")
        #self.rain = AccuWeather(key=key,citykey_file="currentcityKey.txt",cityname_file="currentcityName.txt",timesremaintoday=50)
        self.sensor = Sensor()
        self.filename = filename
        self.clb = None
        
        self.linear_model = LinearRegression()
        self.regar = False

        self.registos_pre_rega = [] #Lista de regas antes da próxima para o modelo de previsão

        self.thr = threading.Thread(target=self.read_data)
        self.thr.daemon = True
        self.thr.start()
    
    def read_data(self):
        while True:
            
            obj = {}
            currentvalues = self.sistema.getCurrentValues()
            cityValues = self.sistema.getCityValues()
            ruleValues = self.sistema.getRuleValues()

            obj['CityName'] = cityValues["CityName"]
            obj['Rules'] = {"Min": ruleValues["Min"], "Max": ruleValues["Max"]}
            obj['EstadoRega'] = self.sistema.regar
            obj['raininfo'] = currentvalues["Precipitation"]
            obj['moisture'] = float(currentvalues["Humidade"])
            obj['PrecMax'] = self.sistema.precipitationMax

            self.registos_pre_rega.append((obj['moisture'],datetime.datetime.now()))
            
            if obj['EstadoRega'] == False:
                try:
                    rules = self.sistema.getCurrentMin()
                    print("Predicting for value " + str(rules))
                    obj['Predicion'] = datetime.datetime.fromtimestamp(pred_test.train_linear_model(self.registos_pre_rega,rules)).strftime('%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    print(e)
            else:
                self.registos_pre_rega = [] #reiniciar Lista pois estamos a regar agora

            self.store_data(obj)
            if self.clb is not None:
                self.clb(obj)
            sleep(1)


    def store_data(self, data):
        self.thr = threading.Thread(target=self.save_data,args=(data,))
        self.thr.daemon = True
        self.thr.start()

        '''
        file_exists = os.path.isfile(self.filename)
        with open(self.filename, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
        '''

    def save_data(self,data):
        if Logger.saveDB == False:
            return
        
        conn = self.db_connection()
        if conn == None:
            return
        cur = conn.cursor()
        cur.execute("""call insert_registo(%s, %s,%s)""", (data["raininfo"],data["moisture"],data["EstadoRega"]))
        #cur.execute("""call get_data_for_day(%s)""", (datetime.datetime.now().strftime('%Y-%m-%d'),))
        
    
        conn.commit()
        cur.close()
        conn.close()


    def on_data_updated(self, clb):
        self.clb = clb

    def db_connection(self):
        try:
            db = psycopg2.connect(host="yipiee.sytes.net" , dbname="LP_DB" ,user="postgres" ,password="postgres")
            return db
        except:
            print("Cant connect to postgres server... not saving")
            Logger.saveDB = False
        
