import requests
import json
#Um token sera usada para identificar um utilizador sem ter que mandar o user e password sempre que é preciso verificar a identidade
currenttoken = ""

def header():
    global currenttoken
    return {
        'Authorization': currenttoken,
        'Content-Type': 'application/json'
    }

URL = "http://2.83.255.244:5000"

def Informacao_Sistema():
    number = input("Numero do sistema")

    response = requests.get(f"{URL}/systeminfo_{number}")
    if response.status_code == 200:
        emps = response.json()
        for emp in emps:
            print(emp)
    else:
        print("Error occurred:", response.text) #funcao teste


def Informacao_Utilizador():
    number = input("Numero do Utilizador")

    response = requests.get(f"{URL}/userinfo_{number}")
    if response.status_code == 200:
        emps = response.json()
        for emp in emps:
            print(emp)
    else:
        print("Error occurred:", response.text) #funcao teste



#esta funcao ja nao e usada
def Menudef():
    print("1-Informacao de sistema")
    print("2-Informacao de utilizador")
    print("3-Sensores de um sistema")
    opcao = int(input(""))
    match(opcao):
        case 1:
            Informacao_Sistema()
        case 2:
            Informacao_Utilizador()

#interface login
def LoginHandler():
    global currenttoken
    username = input("Username: ")
    password = input("Password: ")
    jsoncontent = {
        "username":username,
        "password":password
    }
    url_ = f"{URL}/login"
    response = requests.get(url_,json=jsoncontent)
    if response.status_code == 200:
        emps = response.json()
        print(emps["token"])
        if emps["token"] != None:
            currenttoken = emps["token"]
#interface registo
def RegistHandler():
    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")
    jsoncontent = {
        "username":username,
        "password":password,
        "email":email
    }
    url_ = f"{URL}/regist"
    response = requests.post(url_,json=jsoncontent)
    if response.status_code == 200:
        print("Sucesso!")
    else:
        print("Erro a adicionar utilizador... email/username duplicado")
#lista de sistemas onde há qualquer tipo de acesso
def ListaSistemasDono():

    global currenttoken
    url_ = f"{URL}/systems_"
    response = requests.get(url_,headers=header())
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        print("Token inválido, faca login denovo")
        return None
        
#interface de menu de um sistema
def SystemMenu(id):
    global currenttoken

    while True:
        print("Sistema com ID: " + str(id))
        print("1-Adicionar Sensor")
        print("2-Adicionar Atuador")
        print("3-Listar sensores e os seus detalhes")
        print("4-Listar atuadores e os seus detalhes")
        print("5-Listar Alertas")
        print("0-Sair")
        opcao = int(input(""))
        match(opcao):
            case 1:
                sensorinfo = {
                    'operator': input("operador (</>): "),
                    'comparing_value': input("comparing_value: "),
                    'sensor_type': input("Tipo de sensor: ")
                }
                url_ = f"{URL}/system_{id}/addsensor"
                requests.post(url_,json=sensorinfo,headers=header())

            case 2:
                actuadorinfo = {
                    'actuator_type': input("Tipo de atuador: ")
                }
                url_ = f"{URL}/system_{id}/addactuator"
                requests.post(url_,json=actuadorinfo,headers=header())
            case 3:
                url_ = f"{URL}/system_{id}/sensors"
                

                response = requests.get(url_, headers=header())
                if response.status_code == 200:
                    emps = response.json()
                    for emp in emps:
                        print(emp)
                else:
                    print("Error occurred:", response.text)

            case 4:
                url_ = f"{URL}/system_{id}/actuators"

                response = requests.get(url_, headers=header())
                if response.status_code == 200:
                    emps = response.json()
                    for emp in emps:
                        print(emp)
                else: 
                    print("Error occurred:", response.text)
            
            
            case 5:
                url_ = f"{URL}/system_{id}/alerts"
                response = requests.get(url_,headers=header())
                if response.status_code == 200:
                    emps = response.json()
                    for emp in emps:
                        print(emp)

                else:
                    print("Error occurred: ", response.text)
            case 0:
                return





#Primeiro menu depois de dar login
def FirstMenu():
    global currenttoken
    while currenttoken is not None:
        print("Sistemas")
        counter = 1
        systems = ListaSistemasDono()
        if systems is None:
            LoginMenu()
            return
        for system in systems:
            print(
                str(counter)
                + ": "
                + str(system["system_id"])
                + " System, Admin Privileges: "
                + str(system["admin_privilege"])
            )
            counter += 1

        print(str(counter) + ": Criar Sistema novo")
        counter += 1
        print(str(counter) + ": Sair")
        opcao = input()

        try:
            opcao = int(opcao)
            if 1 <= opcao <= len(systems):
                SystemMenu(systems[opcao - 1]["system_id"])
            elif opcao == counter:
                exit(0)
            elif opcao == counter - 1:
                print("Criar sistema")
            else:
                # Handle invalid input
                print("Invalid input. Please enter a valid option.")
        except ValueError:
            # Handle invalid input (non-integer)
            print("Invalid input. Please enter a valid option.")





#Interface de login/registo
def LoginMenu():
    global currenttoken
    while currenttoken == "":
        print("1-Login")
        print("2-Registar")
        print("3-Sair")
        opcao = int(input(""))
        match(opcao):
            case 1:
                LoginHandler()
                print("CURRENT TOKEN IS "+currenttoken)
                FirstMenu()
            case 2:
                RegistHandler()

LoginMenu()






