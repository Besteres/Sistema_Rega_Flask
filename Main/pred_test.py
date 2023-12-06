import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
import psycopg2

#Devolver a hora prevista para o valor "min" ocorrer a partir de uma lista de valores anteriores ao longo de horas passadas
def train_linear_model(data,min):
    xval = []  
    yval = []  

    for item in data:
        xval.append(item[0])
        yval.append(datetime.datetime.timestamp(item[1]))
    #Construir as duas listas x é os valores de humidade, y é o valor de tempo relativo a esse valor de humidade
    
    xval = np.array(xval).reshape(-1, 1) #remover erro -> Expected 2D array, got 1D array instead
    yval = np.array(yval)

    model = LinearRegression()
    model.fit(xval, yval)
    prediction_input = np.array([[min]])
    y_predict = model.predict(prediction_input)
    #Regressao Linear é usada para prever o valor minimo

    #print(datetime.datetime.fromtimestamp(y_predict[0]).strftime('%Y-%m-%d %H:%M:%S'))
    return y_predict[0]

#Funcao que devolve os dados guardados na base de dados dado um dia especificado em "date"
def getStoredDataDay(date):
    conn = db_connection()
    if conn == None:
        return
    cur = conn.cursor()
    cur.execute("""SELECT * from get_data_for_day(%s,%s)""", (date,False))
    #O segundo argumento é redundante, fazia parte de uma funcionalidade antiga mas agora não faz diferença
    result = []
    i = 0
    for val in cur.fetchall():
        result.append(list(val))
        result[i][2] = result[i][2].strftime('%Y-%m-%d %H:%M:%S')
        i = i+1
    cur.close()
    conn.close()

    return result

#Conexao a base de dados, antigamente usada para o algoritmo de previsão, agora só é usado para buscar e guardar históricos guardados
def db_connection():
    try:
        db = psycopg2.connect(host="yipiee.sytes.net" , dbname="LP_DB" ,user="postgres" ,password='EpicPassword123')
        return db
    except Exception as e:
        print("Cant connect to postgres server... not saving ")
        print(e)