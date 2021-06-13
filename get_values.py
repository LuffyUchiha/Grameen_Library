import time
import psycopg2
from datetime import date


def connect_Postgres(database, user, password, host="localhost"):
    try:
        print('Connecting to {} db @{}'.format(database, host))
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        cur = conn.cursor()
        print('PostgreSQL DB version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    return conn


# donor

def donate_book(book_id, book_title, author_name, ISBN, category):
    print(book_id)
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        book_dtl_id = 0
        donate_date = str(date.today())
        print(donate_date)
        if len(ISBN) == 0:
            book_sql = """
            SELECT ISBN from grlib.book_details where UPPER(book_title) = UPPER(%s)
            """
            cur.execute(book_sql, (book_title,))
            if cur.fetchone() is None:
                ISBN = "UNSORTED"
            else:
                ISBN = cur.fetchone()
        book_ins_sql = """
        INSERT INTO grlib.BOOK (Donor_ID,Donate_Date,ISBN,Book_Name)
        VALUES (%s,%s,%s,%s) RETURNING book_id
        """
        print(book_ins_sql, (book_id, donate_date, ISBN, book_title,))
        cur.execute(book_ins_sql, (book_id, donate_date, ISBN, book_title,))
        book_dtl_id = cur.fetchone()
        if ISBN != "UNSORTED":
            book_check_sql = """
            SELECT no_of_copies_actual, no_of_copies_current from grlib.BOOK b right join grlib.book_details bd on b.ISBN=bd.ISBN where bd.ISBN=%s
            """
            print(book_check_sql, (ISBN,))
            cur.execute(book_check_sql, (ISBN,))
            res = cur.fetchone()
            print(res)
            if res is not None:
                (actual_copies, current_copies) = (res[0], res[1])
                actual_copies += 1
                current_copies += 1
                book_update_sql = """
                UPDATE grlib.BOOK_DETAIL set no_of_copies_actual=%d, no_of_copies_current=%d where ISBN
                """
                cur.execute(book_update_sql, (actual_copies, current_copies, book_id,))
            else:
                book_detail_ins_sql = """
                        INSERT INTO grlib.BOOK_DETAILS (Book_Title,ISBN,Author_Name,no_of_copies_actual,no_of_copies_current)
                VALUES (%s,%s,%s,%s,%s)
                        """
                print(book_detail_ins_sql, (book_title, ISBN, author_name, 1, 1,))
                cur.execute(book_detail_ins_sql, (book_title, ISBN, author_name, 1, 1,))
        cur.close()
        conn.commit()
        conn.close()
        print(book_dtl_id)
        return book_dtl_id
    else:
        return -1


def get_donor_details(id):
    """
    Returns the list of book details donated by the donor with the id = id.
    :param id: integer
    :return: Dictionery
            {"book_list": list of dictionaries of the form {"Book ID": __, "Book Name": __, "Donate Date": __, "isIdentified": __}
             "donor_details":
    """

    if id == '0':
        return []
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        book_num_sql = """
            SELECT d.no_of_books_donated,b.donate_date,b.book_id,b.ISBN,b.book_name 
            from grlib.donor d join grlib.book b on d.donor_id=b.donor_id 
            where d.donor_id=%s order by donate_date
            """
        donor_details_sql = """
            SELECT donor_first_name, donor_mobile, donor_email, is_pmi_member, donor_address
                FROM grlib.donor
                WHERE donor_id=%s
        """
        cur.execute(book_num_sql, (id,))
        res = cur.fetchall()
        num = res[0][0]
        detail_list = []
        for i in res:
            isIdentified = True
            if type(i[3]) == str and i[3].strip() == "UNSORTED":
                isIdentified = False
            detail_list.append(
                dict({"Book ID": i[2], "Book Name": i[4], "Donate Date": i[1], "isIdentified": isIdentified}))
        cur.execute(donor_details_sql, (id,))
        donor_details = list(cur.fetchone())
        cur.close()
        conn.commit()
        conn.close()
        return {'book_details': detail_list, 'donor_details': donor_details}


def update_donor_details_backend(user_id, username, email, mobile, address):
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        donor_details_update_sql = """
        UPDATE grlib.donor
        SET donor_first_name=%s, donor_mobile=%s, donor_email=%s, donor_address=%s
        WHERE donor_id = %s
        RETURNING donor_first_name as new_username, donor_mobile as new_mobile, donor_email as new_email, donor_address as new_address
	    """
        cur.execute(donor_details_update_sql, (username, mobile, email, address, user_id,))
        retval = cur.fetchone()
        cur.close()
        conn.commit()
        conn.close()
        return {'state': 'Success', 'username': retval[0], 'donor_mobile': retval[1], 'email': retval[2],
                'donor_address': retval[3]}
    else:
        return {'state': 'Fail'}


# panchayat

def get_Panchayats():
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        panchayat_list_sql = """
            SELECT Village_Name from grlib.village order by village_name
            """
        cur.execute(panchayat_list_sql)
        panch_list = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        print([{"Village_Name": i[0]} for i in panch_list])
        s = [{"Village_Name": i[0]} for i in panch_list]
        return s


# volunteer

def vol_response(name, pmi_id, is_pmi_member):
    # Is there another table for extracting mobile number and other details with just the pml id and logic for this
    # part depends on that
    res = time.ctime()
    return res


def don_registration_response(name, email, phone, password, donor_address):
    """

    :param name: String
    :param email: String
    :param phone: String/int
    :param password: String
    :param donor_address: String
    :return: {"User ID": user_id, "Name": name[0], "response": res}, res=response code (1 for success)
    """
    name = name.split(maxsplit=1)
    if len(name) == 1:
        name.append("")
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        donor_insert_sql = """
        INSERT INTO grlib.DONOR (Donor_ID,Donor_First_Name,Donor_Last_Name,Donor_Mobile, Donor_Email, Donor_Address)
        VALUES (%s,%s,%s,%s,%s,%s);
        """
        user_insert_sql = """
        INSERT INTO grlib.USER (Role_ID,User_First_Name,User_Last_Name,User_Mobile,password)
        VALUES (%s,%s,%s,%s,%s) RETURNING User_ID;
        """
        cur.execute(user_insert_sql, (2, name[0], name[1], phone, password, donor_address))
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
    return {"User ID": user_id, "Name": name[0], "response": res}


def user_registration_response(name, panchayat, email, phone, password):
    name = name.split(maxsplit=1)
    if len(name) == 1:
        name.append("")
    # student = dict(request.form)['Student']
    # address = dict(request.form)['Address']
    # id_proof = dict(request.form)['ID_proof']
    # location_proof = dict(request.form)['Location_proof']
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        village_select_query = """
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
        cur.execute(user_insert_sql, (4, name[0], name[1], phone, password,))
        user_id = cur.fetchone()[0]
        cur.execute(village_select_query, (panchayat,))
        village_id = cur.fetchone()[0]
        cur.execute(borrower_insert_sql, (name[0], name[1], phone, village_id))
        conn.commit()
        cur.close()
        conn.close()
        res = 1
    else:
        res = 0
        user_id = -1
    return user_id


def pan_registration_response(name, panchayat_name, email, phone, address, password):
    name = name.split(maxsplit=1)
    if len(name) == 1:
        name.append("")
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        panchayat_insert_sql = """
                INSERT INTO grlib.Village 
                (Village_id,Village_Name, Panchayat_Name, Village_Address, Village_Contact_Name, Village_Contact_Mobile, Village_Contact_Email)
                VALUES (%s,%s,%s,%s,%s,%s,%s);
                """
        # Assuming Village and Panchayat names are same for now
        user_insert_sql = """
                    INSERT INTO grlib.USER (Role_ID,User_First_Name,User_Last_Name,User_Mobile,password)
                    VALUES (%s,%s,%s,%s,%s) RETURNING User_ID;
                    """
        cur.execute(user_insert_sql, (3, name[0], name[1], phone, password,))
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
    return {"User ID": user_id, "Name": name[0], "response": res}


def login_response(user_id, password):
    """

    :param user_id: String/int
    :param password: String
    :return: {"Response": True, "Name": user[1], "Role": user[2], "ID": user[0]} if success
            {"Response": False} if fail
    """
    # Is there another table for extracting mobile number and other details with just the pml id and logic for this
    # part depends on that
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        if user_id.isnumeric():
            user_check_sql = "select user_id,user_first_name,role_name" \
                             " from grlib.USER a join grlib.role b on a.role_id=b.role_id" \
                             " where (user_id=%s OR user_mobile=%s) and password= %s"
            cur.execute(user_check_sql, (user_id, user_id, password,))
        else:
            user_check_sql = "select user_id,user_first_name,role_name" \
                             " from grlib.USER a join grlib.role b on a.role_id=b.role_id" \
                             " where (user_first_name=%s) and password= %s"
            cur.execute(user_check_sql, (user_id, password,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        print(user)
        if user is not None:
            return {"Response": True, "Name": user[1], "Role": user[2], "ID": user[0]}
        else:
            return {"Response": False}
    else:
        return {"Response": False}


def admin_login_response(user_id, password):
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        admin_check_sql = "select admin_id, admin_name, admin_roles " \
                          "from grlib.ADMIN " \
                          "where (admin_id=%s or admin_name=%s) and password=%s"
        cur.execute(admin_check_sql, (
            -1 if type(user_id) == str else user_id,
            '' if type(user_id) == int else user_id,
            password,
        ))
        admin = cur.fetchone()
        cur.close()
        conn.close()
        if admin is not None:
            return {"Response": True, "Name": admin[1], "Roles": admin[2]}
        else:
            return {"Response": False}


def get_categories():
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        category_sql = """
            SELECT category_name
            FROM grlib.book_category;
        """
        cur.execute(category_sql)
        categories = cur.fetchall()
        category_list = [x[0] for x in categories]
        return category_list


if __name__ == "__main__":
    print(get_categories())
