from flask import *
import time
import psycopg2
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.secret_key = 'random string'
CORS(app=app)
app.config['CORS_HEADERS'] = 'Content-Type'


def connect_Postgres(database, user, password, host="localhost"):
    try:
        app.logger.info('Connecting to %s db @%s', database, host)
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        cur = conn.cursor()
        app.logger.info('PostgreSQL DB version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        app.logger.info(db_version)
        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        app.logger.info(error)
        return None
    return conn


@app.route("/get_Panchs", methods=["GET"])
def get_Panchayats():
    conn = connect_Postgres(
        host="localhost",
        database="Grameen_Library",
        user="grlib",
        password="password"
    )
    if conn is not None:
        cur = conn.cursor()
        panchayat_list_sql = """
            SELECT Village_Name from grlib.village order by village_name
            """
        cur.execute(panchayat_list_sql)
        panch_list = cur.fetchall()
        cur.close()
        conn.close()
        print([{"Village_Name": i[0]} for i in panch_list])
        s = jsonify([{"Village_Name": i[0]} for i in panch_list])
        return s


@app.route("/register/volunteer", methods=["POST"])
def vol_response():
    name = dict(request.form)['name']
    pmi_id = dict(request.form)['pmi_id']
    is_pmi_member = dict(request.form)['pmi_pcc_member']
    # Is there another table for extracting mobile number and other details with just the pml id and logic for this
    # part depends on that
    res = time.ctime()
    return jsonify({"response": res})


@app.route("/register/donor", methods=["POST"])
def don_response():
    name = dict(request.form)['Name'].split(maxsplit=1)
    if len(name) == 1:
        name.append("")
    email = dict(request.form)['Email']
    phone = dict(request.form)['Phone']
    password = dict(request.form)['Password']
    conn = connect_Postgres(
        host="localhost",
        database="Grameen_Library",
        user="grlib",
        password="password"
    )
    if conn is not None:
        cur = conn.cursor()
        donor_insert_sql = """
        INSERT INTO grlib.DONOR (Donor_ID,Donor_First_Name,Donor_Last_Name,Donor_Mobile,Donor_Email)
        VALUES (%s,%s,%s,%s,%s);
        """
        user_insert_sql = """
        INSERT INTO grlib.USER (Role_ID,User_First_Name,User_Last_Name,User_Mobile,password)
        VALUES (%s,%s,%s,%s,%s) RETURNING User_ID;
        """
        cur.execute(user_insert_sql, (2, name[0], name[1], phone,password,))
        # Assumption that 2 is role id for donor and so on
        user_id = cur.fetchone()[0]
        cur.execute(donor_insert_sql, (user_id, name[0], name[1], phone, email,))
        conn.commit()
        cur.close()
        conn.close()
        res = 1
    else:
        res = 0
        donor_id = -1
        user_id = -1
    return jsonify({"User ID": user_id, "Name": name[0], "response": res})


@app.route("/register/user", methods=["POST"])
def user_response():
    name = dict(request.form)['Name'].split(maxsplit=1)
    if len(name) == 1:
        name.append("")
    panchayat = dict(request.form)['Panchayat']
    #student = dict(request.form)['Student']
    email = dict(request.form)['Email']
    phone = dict(request.form)['Phone']
    #address = dict(request.form)['Address']
    #id_proof = dict(request.form)['ID_proof']
    #location_proof = dict(request.form)['Location_proof']
    password = dict(request.form)['Password']
    conn = connect_Postgres(
        host="localhost",
        database="Grameen_Library",
        user="grlib",
        password="password"
    )
    if conn is not None:
        cur = conn.cursor()
        village_select_query="""
            SELECT village_id from grlib.village where village_name= %s
            """
        borrower_insert_sql = """
            INSERT INTO grlib.Borrower_Profile (Borrower_First_Name,Borrower_Last_Name,Borrower_Mobile,Village_Id)
            VALUES (%s,%s,%s,%s);
            """
        # neede to include columns for id proof, address, email for the user as well but optional
        user_insert_sql = """
                INSERT INTO grlib.USER (Role_ID,User_First_Name,User_Last_Name,User_Mobile,password)
                VALUES (%s,%s,%s,%s,%s) RETURNING User_ID;
                """
        cur.execute(user_insert_sql, (4, name[0], name[1], phone,password,))
        user_id = cur.fetchone()[0]
        cur.execute(village_select_query,(panchayat,))
        village_id=cur.fetchone()[0]
        cur.execute(borrower_insert_sql,(name[0],name[1],phone,village_id))
        conn.commit()
        cur.close()
        conn.close()
        res = 1
    else:
        res = 0
        user_id = -1
    return jsonify({"User ID": user_id, "response": res})


@app.route("/register/panchayat", methods=["POST"])
def pan_response():
    name = dict(request.form)['PoC Name'].split(maxsplit=1)
    if len(name) == 1:
        name.append("")
    panchayat_name = dict(request.form)['Panchayat Name']
    email = dict(request.form)['Email']
    phone = dict(request.form)['Phone']
    address = dict(request.form)['Address']
    password = dict(request.form)['Password']
    conn = connect_Postgres(
        host="localhost",
        database="Grameen_Library",
        user="grlib",
        password="password"
    )
    if conn is not None:
        cur = conn.cursor()
        panchayat_insert_sql = """
                INSERT INTO grlib.Village (Village_id,Village_Name, Panchayat_Name, Village_Address, Village_Contact_Name, Village_Contact_Mobile, \"Village_Contact_Email\")
                VALUES (%s,%s,%s,%s,%s,%s,%s);
                """
        # Assuming Village and Panchayat names are same for now
        user_insert_sql = """
                    INSERT INTO grlib.USER (Role_ID,User_First_Name,User_Last_Name,User_Mobile,password)
                    VALUES (%s,%s,%s,%s,%s) RETURNING User_ID;
                    """
        cur.execute(user_insert_sql, (3, name[0], name[1], phone,password,))
        user_id = cur.fetchone()[0]
        cur.execute(panchayat_insert_sql,
                    (user_id, panchayat_name, panchayat_name, address, name[0] + name[1], phone, email))
        conn.commit()
        cur.close()
        conn.close()
        res = 1
    else:
        res = 0
        user_id = -1
    return jsonify({"User ID": user_id, "Name": name[0], "response": res})


@app.route("/login", methods=["POST"])
@cross_origin()
def login_response():
    print(dict(request.form))
    user_id = dict(request.form)['user_id']
    password = dict(request.form)['password']
    # Is there another table for extracting mobile number and other details with just the pml id and logic for this
    # part depends on that
    conn = connect_Postgres(
        host="localhost",
        database="Grameen_Library",
        user="grlib",
        password="password"
    )
    if conn is not None:
        cur = conn.cursor()
        user_check_sql = "select user_first_name,user_last_name,role_name from grlib.USER a join grlib.role b on a.role_id=b.role_id where user_id= %s and password= %s"
        cur.execute(user_check_sql, (user_id, password,))
        user = cur.fetchone()
        print(user)
        if user is not None:
            # the session can't be modified as it's signed,
            # so it's a safe place to store the user
            session['user_id'] = user_id
            cur.close()
            conn.close()
            return jsonify({"Response": 1, "Name": user[0]+" "+user[1], "Role":user[2]})
        else:
            cur.close()
            conn.close()
            return jsonify({"Response": 0})
    res = time.ctime()
    return jsonify({"Response": -1})


@app.route("/")
def hello_world():
    return "Hello World"


# app.add_url_rule('/','home',home)
if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
