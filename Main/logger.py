
import threading
import datetime
import csv
import os
from sensor import Sensor
from AccuWeather import AccuWeather
from time import sleep
from Sistema import Sistema
import psycopg2

key = "NK6kGCNYAE2l1Dhu8Jv775xKd1SPCEpk"



class Logger(object):
    def __init__(self, filename='data.csv'):
        self.sistema = Sistema(key=key,citykey="currentcityKey.txt",cityname="currentcityName.txt",timesremain=50,HumidityMin=40,HumidityMax=60)
        #self.rain = AccuWeather(key=key,citykey_file="currentcityKey.txt",cityname_file="currentcityName.txt",timesremaintoday=50)
        self.sensor = Sensor()
        self.filename = filename
        self.clb = None
        
        self.regar = False


        self.thr = threading.Thread(target=self.read_data)
        self.thr.daemon = True
        self.thr.start()
    
    def read_data(self):
        while True:
            obj = {}
            currentvalues = self.sistema.getCurrentValues()
            cityValues = self.sistema.getCityValues()
            ruleValues = self.sistema.getRuleValues()

            obj['City Name'] = cityValues["CityName"]
            obj['Rules'] = {"Min": ruleValues["Min"], "Max": ruleValues["Max"]}
            obj['EstadoRega'] = self.sistema.regar
            obj['raininfo'] = currentvalues["Precipitation"]
            obj['moisture'] = float(currentvalues["Humidade"])
            self.store_data(obj)
            if self.clb is not None:
                self.clb(obj)

            sleep(1)
    
    def store_data(self, data):
        conn = self.db_connection()
        cur = conn.cursor()
        cur.execute("""call insert_registo(%s, %s)""", (data["raininfo"],data["moisture"]))
        #cur.execute("""call get_data_for_day(%s)""", (datetime.datetime.now().strftime('%Y-%m-%d'),))
        cur.execute("""call update_estado_rega(%s)""", (data["EstadoRega"],))
        
    
        conn.commit()
        cur.close()
        conn.close()

        '''
        file_exists = os.path.isfile(self.filename)
        with open(self.filename, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
        '''


    def on_data_updated(self, clb):
        self.clb = clb

    def db_connection(self):
        db = psycopg2.connect(host="yipiee.sytes.net" , dbname="LP_DB" ,user="postgres" ,password="postgres")
        return db
