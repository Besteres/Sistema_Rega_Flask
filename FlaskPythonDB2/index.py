from flask import Flask, jsonify, request, abort
import psycopg2

def db_connection():
    db = psycopg2.connect(host="2.83.255.244" , dbname="Projeto" ,user="postgres" ,password="postgres")
    return db

app = Flask(__name__)
app.debug = True
def getUserID(token):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM f_get_user_id_from_token(%s)""", (token,))

    for emp_tuple in cur.fetchall():
        return emp_tuple[0]


@app.route('/system_create',methods=['POST'])
def create_system():
    conn = db_connection()
    cur = conn.cursor()
    j_body = request.get_json()
    token = request.headers.get('Authorization')
    userID = getUserID(token)
    if userID == -1:
        abort(401, "Invalid token")

    cur.execute("""call f_criar_sistema(f_inserir_regras_sistema(%s), %s, %s, %s)""", (j_body['timestamp'],str(j_body['user_id']),str(j_body['localizacao']),str(j_body['descricao'])))
    
    conn.commit()
    cur.close()
    conn.close()
    return "OK"



@app.route('/systems_',methods=['GET'])
def systeminfo():
    conn = db_connection()
    cur = conn.cursor()
    token = request.headers.get('Authorization')
    print("SErver given token: " + token)
    userID = getUserID(token)
    if userID == -1:
        abort(401, "Invalid token")

    cur.execute("""SELECT * FROM f_get_user_systems(%s)""", (str(userID),))
    emps = []

    for emp_tuple in cur.fetchall():
        emp = {
            "system_id": emp_tuple[0],
            "system_rule_id": emp_tuple[1],
            "user_id": emp_tuple[2],
            "location": emp_tuple[3],
            "description": emp_tuple[4],
            "admin_privilege": emp_tuple[5]
        }
        emps.append(emp)

    cur.close()
    conn.close()
    return jsonify(emps)



@app.route('/sensor_<int:id>/reading',methods=['POST'])
def sensor_reading(id):
    conn = db_connection()
    cur = conn.cursor()
    j_body = request.get_json()
    cur.execute("""CALL f_insert_sensor_reading(%s,%s)""",(str(id),str(j_body['value'])))
    conn.commit()
    cur.close()
    conn.close()

    return 'OK'


@app.route('/actuator_<int:id>/setactive',methods=['POST'])
def actuator_setactive(id):
    conn = db_connection()
    cur = conn.cursor()
    j_body = request.get_json()
    cur.execute("""SELECT f_change_atuador(%s,%s)""",(str(id),str(j_body['value'])))
    conn.commit()
    cur.close()
    conn.close()

    return "OK"






    
@app.errorhandler(Exception)
def handle_error(error):

    description = 'Internal Server Error'

    response = {
        'error': description,
        'message': str(error)
    }
    return jsonify(response),400

@app.route('/system_<int:number>/actuators', methods=['GET'])
def actuators(number):
    conn = db_connection()
    cur = conn.cursor()
    token = request.headers.get('Authorization')
    userID = getUserID(token)
    if userID == -1: #continue
        abort(401, "Invalid token")

    cur.execute("""SELECT f_check_read_access(%s, %s)""",(str(number),str(userID)))
    for emp_tuple in cur.fetchall():
        if emp_tuple[0] == False:
            abort(402,"User does not have access to this system")

    cur.execute("""SELECT * FROM f_get_system_actuators(%s)""",(str(number),))
    emps = []

    for emp_tuple in cur.fetchall():
        emp = {
            "actuator_id": emp_tuple[0],
            "actuator_type": emp_tuple[3]
        }
        emps.append(emp)

    cur.close()
    conn.close()
    return jsonify(emps)


@app.route('/system_<int:number>/addactuator', methods=['POST'])
def addactuator(number):
    conn = db_connection()
    cur = conn.cursor()
    j_body = request.get_json()
    token = request.headers.get('Authorization')
    userID = getUserID(token)
    if userID == -1:
        abort(401, "Invalid token")

    cur.execute("""SELECT * FROM check_admin_access(%s,%s)""",(str(number),str(userID)))

    for emp_tuple in cur.fetchall():
        if emp_tuple == False:
            abort(1004,"This user does not have access to this system")

    cur.execute("""SELECT f_add_actuator(%s,%s,%s)""",(str(number),str(userID),j_body['actuator_type']))
    conn.commit()
    cur.close()
    conn.close()
    return "OK"

@app.route('/system_<int:number>/addsensor', methods=['POST'])
def addsensor(number):
    conn = db_connection()
    cur = conn.cursor()
    j_body = request.get_json()
    token = request.headers.get('Authorization')
    userID = getUserID(token)
    if userID == -1:
        abort(401, "Invalid token")

    cur.execute("""SELECT * FROM check_admin_access(%s,%s)""",(str(number),str(userID)))

    for emp_tuple in cur.fetchall():
        if emp_tuple == False:
            abort(1004,"This user does not have access to this system")

    cur.execute("""SELECT f_add_sensor(f_create_sensor_rule(%s,%s),%s,%s,%s)""",(str(j_body["operator"]),str(j_body['comparing_value']),str(userID),str(number),str(j_body["sensor_type"])))
    conn.commit()
    cur.close()
    conn.close()
    return "OK"


@app.route('/actuador_<int:id>/setalert',methods=['POST'])
def actuator_set_alert(id):
    conn = db_connection()
    cur = conn.cursor()
    j_body = request.get_json()
    cur.execute("""CALL f_set_alert_actuator(%s,%s,%s)""",(str(id),str(j_body['ruleid']),str(j_body['status'])))
    conn.commit()
    cur.close()
    conn.close()
    return "OK"


@app.route('/system_<int:id>/setgroup',methods=['POST'])
def set_group_to_sys(id):
    conn = db_connection()
    cur = conn.cursor()
    j_body = request.get_json()
    token = request.headers.get('Authorization')
    print(token)
    userID = getUserID(token)
    if userID == -1:
        abort(401, "Invalid token")

    cur.execute("""SELECT * FROM check_admin_access(%s,%s)""",(str(id),str(userID)))

    for emp_tuple in cur.fetchall():
        if emp_tuple == False:
            abort(1004,"This user does not have access to this system")

    cur.execute("""SELECT f_check_read_access(%s, %s)""",(str(id),str(userID)))
    for emp_tuple in cur.fetchall():
        if emp_tuple[0] == False:
            abort(402,"User does not have access to this system")

    cur.execute("""CALL f_set_group_to_system(%s,%s,%s)""",(str(j_body["group_id"]),str(id),str(j_body["admin_perm"])))

    conn.commit()
    cur.close()
    conn.close()
    return "OK"




@app.route('/group_create',methods=['POST'])
def create_group():
    conn = db_connection()
    cur = conn.cursor()
    j_body = request.get_json()
    cur.execute("""SELECT f_insert_group(%s);""",(str(j_body["groupname"]),))
    conn.commit()
    cur.close()
    conn.close()
    return "OK"

@app.route('/system_<int:id>/checkstatus',methods=['GET'])
def system_checkstatus(id):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("""SELECT f_verifica_estado_do_sistema(%s)""",(str(id),))
    for emp_tuple in cur.fetchall():
        return jsonify(emp_tuple[0])
    
    return "This system does not exist"


@app.route('/alert_<int:id>/atuadores')
def alert_atuadores(id):
    conn = db_connection()
    cur = conn.cursor()
    token = request.headers.get('Authorization')
    userID = getUserID(token)
    if userID == -1:
        abort(401, "Invalid token")
    sysnumber = -1

    cur.execute("""SELECT * FROM f_get_system_from_sensor_alert(%s)""",(str(id),))
    for emp_tuple in cur.fetchall():
        sysnumber = emp_tuple[0]
        
    if sysnumber == -1:
        abort(1002,"System not found")

    found = False

    cur.execute("""SELECT * FROM f_get_user_systems(%s)""",(str(userID),))
    for emp_tuple in cur.fetchall():
        if sysnumber == emp_tuple[0]:
            found = True
            break

    if not found:
        abort(1003,"This user does not have access to any systems")

    cur.execute("""SELECT * FROM f_get_alert_reactions(%s)""",(str(id),))
    result = []
    for emp_tuple in cur.fetchall():
        result.append({
            "atuador_id": emp_tuple[0]
        })

    cur.close()
    conn.close()
    
    return jsonify(result)
            

@app.route('/system_<int:id>/alerts',methods=['GET'])
def system_alerts(id):
    conn = db_connection()
    cur = conn.cursor()
    token = request.headers.get('Authorization')
    
    userID = getUserID(token)
    if userID == -1:
        abort(401, "Invalid token")

    

    cur.execute("""SELECT f_check_read_access(%s, %s)""",(str(id),str(userID)))
    for emp_tuple in cur.fetchall():
        if emp_tuple[0] == False:
            abort(402,"User does not have access to this system")

    result = []
    cur.execute("""SELECT * FROM f_get_alertas_de_sistema(%s,%s)""",(str(id),str(userID)))
    for emp_tuple in cur.fetchall():
        result.append({
            'alert_id': emp_tuple[0],
            'reading_id': emp_tuple[1],
            'alert_name': emp_tuple[2],
            'datetime': emp_tuple[3],
            'alert_rule_id': emp_tuple[4]
        })


    conn.commit()
    cur.close()
    conn.close()
    return jsonify(result)


@app.route('/login')
def loginuser():
    conn = db_connection()
    cur = conn.cursor()
    j_body = request.get_json()
    cur.execute("""SELECT * FROM f_validate_login_and_generate_token(%s,%s)""",(j_body["username"],j_body["password"]))
    conn.commit()
    for emp_tuple in cur.fetchall():
        if emp_tuple[1] != None:
            print("TOKEN AQUIRED: "+ emp_tuple[1] + " FOR USER ID " + str(emp_tuple[0]))
            cur.close()
            conn.close()
            return {"user_id":emp_tuple[0],"token":emp_tuple[1]}
        else:
            cur.close()
            conn.close()
            return {"token": None,"user_id": None}
        
    

@app.route('/regist', methods=['POST'])
def registuser():
    try:
        conn = db_connection()
        cur = conn.cursor()
        j_body = request.get_json()
        cur.execute("""SELECT f_register_user(%s, %s, %s)""", (j_body["username"], j_body["password"], j_body["email"]))
        conn.commit()
        cur.close()
        conn.close()
        return "User registered successfully", 200
    except psycopg2.Error as e:
        cur.close()
        conn.close()
        return str(e), 400
    
    
@app.route('/group_<int:id>/userjoin',methods=['POST'])
def group_join(id):
    conn = db_connection()
    cur = conn.cursor()
    token = request.headers.get('Authorization')
    userID = getUserID(token)
    cur.execute("""call f_adiciona_user_ao_grupo(%s,%s)""",(str(userID),str(id)))
    conn.commit()
    cur.close()
    conn.close()
    return "OK"





@app.route('/userinfo')
def userinfo():
    conn = db_connection()
    cur = conn.cursor()
    token = request.headers.get('Authorization')
    userID = getUserID(token)
    if userID == -1:
        abort(401, "Invalid token")

    cur.execute("""SELECT * FROM f_get_user_info(%s)""",(str(userID),))
    emps = []

    for emp_tuple in cur.fetchall():
        emp = {
            "user_name": emp_tuple[0],
            "email": emp_tuple[1]
        }
        emps.append(emp)

    cur.close()
    conn.close()
    return jsonify(emps)




@app.route('/system_<int:number>/sensors')
def systemsensors(number):
    conn = db_connection()
    cur = conn.cursor()
    token = request.headers.get('Authorization')
    userID = getUserID(token)
    if userID == -1:
        abort(401, "Invalid token")


    cur.execute("""SELECT f_check_read_access(%s, %s)""",(str(number),str(userID)))
    for emp_tuple in cur.fetchall():
        if emp_tuple[0] == False:
            abort(402,"User does not have access to this system")

    cur.execute("""SELECT * FROM f_get_system_sensors(%s)""",(str(number)))
    emps = []

    for emp_tuple in cur.fetchall():
        emp = {
            "sensor_id": emp_tuple[0],
            "sensor_type": emp_tuple[1]
        }
        emps.append(emp)

    cur.close()
    conn.close()
    return jsonify(emps)





if __name__ == "__main__":
    app.run(host='192.168.1.75', port=5000)
    


