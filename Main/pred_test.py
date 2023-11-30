import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
import psycopg2

def train_linear_model(data,min):
    xval = []  
    yval = []  
    i = 0
    for item in data:
        yval.append(datetime.datetime.timestamp(item[1]))
        xval.append(item[0])
        
    
    
    xval = np.array(xval).reshape(-1, 1)
    yval = np.array(yval)
    #print(yval)

    model = LinearRegression()
    model.fit(xval, yval)
    prediction_input = np.array([[min]])
    y_predict = model.predict(prediction_input)
    print(datetime.datetime.fromtimestamp(y_predict[0]).strftime('%Y-%m-%d %H:%M:%S'))
    return y_predict[0]

def getStoredDataToday():
    conn = db_connection()
    if conn == None:
        return
    cur = conn.cursor()
    cur.execute("""SELECT * from get_data_for_day(%s,%s)""", (datetime.datetime.now().strftime('%Y-%m-%d'),False))
    result = cur.fetchall()
    cur.close()
    conn.close()

    return result

def db_connection():
    try:
        db = psycopg2.connect(host="yipiee.sytes.net" , dbname="LP_DB" ,user="postgres" ,password="postgres")
        return db
    except:
        print("Cant connect to postgres server... not saving")