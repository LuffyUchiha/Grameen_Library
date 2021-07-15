import time
import psycopg2
from datetime import date


def connect_Postgres(database, user, password, host="localhost"):
    try:
        # print('Connecting to {} db @{}'.format(database, host))
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        cur = conn.cursor()
        # print('PostgreSQL DB version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        # print(db_version)
        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    return conn


# donor

def donate_book(donor_id, book_title, no_of_copies, author_name, ISBN, category, start_date, end_date):
    # print(donor_id)
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
        # print(donate_date)
        book_sql = """
        SELECT ISBN from grlib.book_details where UPPER(book_title) = UPPER(%s)
        """
        cur.execute(book_sql, (book_title,))
        ISBN = cur.fetchone()
        # TODO after confirming ISBNs, need to incorporate category logic
        if ISBN is None:
            ISBN = "UNSORTED"
        book_category_sql = """
        SELECT category_id
        FROM grlib.book_category
        WHERE category_name = %s
        """
        cur.execute(book_category_sql, (category,))
        category_id = cur.fetchone()
        if category_id:
            category_id = category_id[0]
        book_ins_sql = """
        INSERT INTO grlib.book_to_be_collected(
        book_title, author_name, isbn, category_id, donor_id, donation_date, available_date_start, available_date_end)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        no_of_copies = int(no_of_copies) if no_of_copies != None and int(no_of_copies) > 0 else 1
        for _ in range(int(no_of_copies)):
            cur.execute(book_ins_sql, (
                book_title if book_title else 'null',
                author_name if author_name else 'null',
                ISBN if ISBN else 'null',
                category_id if category_id else 'null',
                donor_id if donor_id else 'null',
                donate_date if donate_date else 'null',
                start_date if start_date else 'null',
                end_date if end_date else 'null',
            )
                        )
        if ISBN != "UNSORTED":
            book_check_sql = """
            SELECT no_of_copies_actual, no_of_copies_current from grlib.BOOK b right join grlib.book_details bd on b.ISBN=bd.ISBN where bd.ISBN=%s
            """
            cur.execute(book_check_sql, (ISBN,))
            res = cur.fetchone()
            if res is not None:
                (actual_copies, current_copies) = (res[0], res[1])
                actual_copies += 1
                current_copies += 1
                book_update_sql = """
                UPDATE grlib.BOOK_DETAIL set no_of_copies_actual=%s, no_of_copies_current=%s where ISBN=%s
                """
                cur.execute(book_update_sql, (actual_copies, current_copies, ISBN,))
            else:
                book_detail_ins_sql = """
                        INSERT INTO grlib.BOOK_DETAILS (Book_Title,ISBN,Author_Name,no_of_copies_actual,no_of_copies_current)
                        VALUES (%s,%s,%s,%s,%s)
                        """
                cur.execute(book_detail_ins_sql, (book_title, ISBN, author_name, 1, 1,))
        cur.close()
        conn.commit()
        conn.close()
        return book_dtl_id
    else:
        return -1


def get_donor_details(id):
    """
    Returns the list of book details donated by the donor with the id = id.
    :param id: integer
    :return: Dictionery
            {
            "book_list": list of dictionaries of the form {"Book ID": __, "Book Name": __, "Donate Date": __, "isIdentified": __}
             "donor_details":[donor_name, donor_mobile, donor_email, is_pmi_member, donor_address, city, state, pincode]
             }
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
            SELECT donor_name, donor_mobile, donor_email, is_pmi_member, donor_address, donor_city, donor_state, donor_pincode
                FROM grlib.donor
                WHERE donor_id=%s
        """
        cur.execute(book_num_sql, (id,))
        res = cur.fetchall()
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


def get_donor_donations():
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        donor_list_sql = """
        SELECT books.donor_id, donors.donor_name, books.donation_date, books.available_date_start, books.available_date_end, count(books.donor_id) as no_of_books_donated, books.assigned_volunteer_id
        FROM grlib.book_to_be_collected as books LEFT JOIN grlib.donor as donors ON books.donor_id=donors.donor_id
        GROUP BY books.donor_id, donors.donor_name, books.donation_date, books.available_date_start, books.available_date_end, books.assigned_volunteer_id
        ORDER BY donors.donor_name;
        """
        cur.execute(donor_list_sql)
        donor_list = cur.fetchall() #returns (donor_id, donor_name, donation_date, available_date_start, available_date_end, count(donor_id)
        ret_list = []
        for donor in donor_list:
            temp = {'donor_id': donor[0], 'donor_name': donor[1], 'donation_date': donor[2],
                    'available_date_start': donor[3], 'available_date_end': donor[4], 'no_of_books': donor[5],
                    'assigned_volunteer_id':donor[6] if donor[6] else -1}
            ret_list.append(temp)
        return ret_list

def get_donor_donations_by_id(user_id):
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        donor_donation_list_sql = """
        SELECT books.book_title, books.author_name, books.isbn, books.category_id, books.donor_id, books.donation_date, books.available_date_start, books.available_date_end, books.collection_id, books.assigned_volunteer_id, vol.volunteer_name
        FROM grlib.book_to_be_collected as books Left JOIN grlib.volunteer as vol on books.assigned_volunteer_id=vol.volunteer_id
        Where donor_id = %s
        """
        cur.execute(donor_donation_list_sql, (user_id,))
        donation_list = cur.fetchall()
        ret_list = []
        for donation  in donation_list:
            ret_list.append({
                'book_name': donation[0],
                'author_name': donation[1],
                'isbn': donation[2],
                'category_id': donation[3],
                'donation_date': donation[5],
                'start_date': donation[6],
                'end_date': donation[7],
                'volunteer_name': donation[10] if donation[9] else 'Not Assigned'
            })
        return ret_list


def update_donor_details_backend(user_id, username, email, mobile, address, city, state, pincode):
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
        SET donor_name=%s, donor_mobile=%s, donor_email=%s, donor_address=%s, donor_city=%s, donor_state=%s, donor_pincode=%s
        WHERE donor_id = %s
        RETURNING donor_name as new_username, donor_mobile as new_mobile, donor_email as new_email, donor_address as new_address, 
        donor_city as new_city, donor_state as new_state, donor_pincode as new_pincode
	    """
        user_details_update_sql = """
        UPDATE grlib."user"
        SET username=%s, user_mobile=%s
        WHERE user_id = %s
        """
        cur.execute(donor_details_update_sql,
                    (username, mobile, email, address, city, state, pincode if pincode != None else 0, user_id,))
        retval = cur.fetchone()
        cur.execute(user_details_update_sql, (username, mobile, user_id,))
        cur.close()
        conn.commit()
        conn.close()
        print(retval)
        return {'state': 'Success', 'username': retval[0], 'donor_mobile': retval[1], 'email': retval[2],
                'donor_address': retval[3], 'donor_city': retval[4], 'donor_state': retval[5],
                'donor_pincode': retval[6]}
    else:
        return {'state': 'Fail'}


# panchayat

def get_panchayats():
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        panchayat_list_sql = """
            SELECT * from grlib.village order by village_name
            """
        cur.execute(panchayat_list_sql)
        panch_list = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        s = [
            {
                'village_id': i[0],
                'village_name': i[1],
                'panchayat_name':i[2],
                'village_address':i[3],
                'poc_name':i[4],
                'poc_number':i[5],
                'poc_mail':i[6]
            }
            for i in panch_list
        ]
        return s
    else:
        return -1

def add_panchayat(village_name, panchayat_name, village_address, poc_name, poc_number, poc_mail):
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        panchayat_insert_sql = """
        INSERT INTO grlib.village(
        village_name, panchayat_name, village_address, village_contact_name, village_contact_mobile, village_contact_email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.execute(panchayat_insert_sql, (village_name, panchayat_name, village_address, poc_name, poc_number, poc_mail,))
        conn.commit()
        cur.close()
        conn.close()
        return{'state': 'success'}
    else:
        return {'state': 'failure'}


# volunteer

def vol_response(name, pmi_id, is_pmi_member):
    # Is there another table for extracting mobile number and other details with just the pml id and logic for this
    # part depends on that
    res = time.ctime()
    return res


def get_volunteer_details(user_id):
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        volunteer_details_sql = """
            SELECT volunteer_id, volunteer_name, volunteer_mobile, volunteer_address, volunteer_city, volunteer_state, volunteer_pincode, email, books_collected, donors_reached
            FROM grlib.volunteer 
            WHERE volunteer_id = %s
        """
        volunteer_ack_sql = """
            SELECT volunteer_id, content, "from", from_reference
            FROM grlib.volunteer_acknowledgements 
            WHERE volunteer_id = %s
        """
        cur.execute(volunteer_details_sql, (int(user_id),))
        vol_details = cur.fetchone()
        cur.execute(volunteer_ack_sql, (int(user_id),))
        acks = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        return {'state': 'Success', 'user_id': vol_details[0], 'volunteer_name': vol_details[1],
                'volunteer_mobile': vol_details[2],
                'volunteer_address': vol_details[3], 'volunteer_city': vol_details[4],
                'volunteer_state': vol_details[5],
                'volunteer_pincode': vol_details[6], 'email': vol_details[7], 'books_collected': vol_details[8],
                'donors_reached': vol_details[9], 'acknowledgements': acks}
    else:
        return {'state': 'Fail'}

def get_collections(user_id):
    """
    What donors to collect from
    :return:
    """
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        collections_sql = """
        SELECT 
        donor_name as donor_name,
        available_date_start as start_date,
        available_date_end as end_date,
        donor_address,
        donor_mobile,
        COUNT(collection_id) as no_of_books
            FROM
            (SELECT * FROM
                grlib.book_to_be_collected as books
                    INNER JOIN
                    grlib.donor as donors
                    on
                    books.donor_id=donors.donor_id
                WHERE books.assigned_volunteer_id=%s
            ) as donors_and_books
                
            GROUP BY donor_name, available_date_start, available_date_end, donor_address, donor_mobile
            ORDER BY donor_name
        """
        cur.execute(collections_sql, (user_id,))
        donors = cur.fetchall()
        cur.close()
        conn.close()
        ret_list = []
        for donor in donors:
            ret_list.append({'donor_name':donor[0], 'address':donor[3], 'start_date': donor[1], 'end_date': donor[2], 'donor_mobile': donor[4], 'no_of_books':donor[5]})
        return ret_list




def get_active_volunteers():
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        volunteer_list_sql = """
        SELECT volunteer_id, volunteer_name, email, books_collected, donors_reached, last_active_date
        FROM grlib.volunteer
        where EXTRACT(HOUR from AGE(last_active_date)) < 720
        """
        cur.execute(volunteer_list_sql)
        ret_list = []
        volunteer_list = cur.fetchall()
        for volunteer in volunteer_list:
            temp = {'volunteer_id': volunteer[0], 'volunteer_name': volunteer[1], 'email': volunteer[2],
                    'books_collected': volunteer[3], 'donors_reached': volunteer[4], 'last_active_date': volunteer[5]}
            ret_list.append(temp)
        return ret_list


def enter_book(donor_id, book_name, isbn, volunteer_id):
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        enter_book_sql = """
        INSERT INTO grlib.book(
        donor_id, donate_date, isbn, book_name, volunteer_id)
        VALUES (%s, CURRENT_DATE, %s, %s, %s)
        """
        remove_to_be_donated_sql = """
        DELETE FROM grlib.book_to_be_collected
	    WHERE donor_id=%s and book_title=%s
        """
        volunteer_contribution_update_sql = """
        UPDATE grlib.volunteer
        SET	books_collected=(SELECT count(book_id)
            FROM grlib.book
            where volunteer_id=%s), donors_reached=(SELECT count(donor_id)
        FROM grlib.book
        where volunteer_id=%s)
        WHERE volunteer_id=%s
        """
        cur.execute(enter_book_sql, (donor_id, isbn, book_name, volunteer_id,))
        cur.execute(remove_to_be_donated_sql, (donor_id, book_name,))
        cur.execute(volunteer_contribution_update_sql,(volunteer_id, volunteer_id, volunteer_id,))
        conn.commit()
        cur.close()
        conn.close()

# borrower


def don_registration_response(name, email, phone, password, donor_address, donor_city, donor_state, donor_pincode,
                              pmi_number):
    """

    :param name: String
    :param email: String
    :param phone: String/int
    :param password: String
    :param donor_address: String
    :return: {"User ID": user_id, "Name": name[0], "response": 1}, response code, 1 for success
            {"response": 2, "message": Username already exists, choose a different name"}, 2 for conflicting username
    """
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()

        donor_check_sql = """
        SELECT user_id, username
        FROM grlib."user"
        WHERE username=%s
        """

        cur.execute(donor_check_sql, (name,))
        if cur.fetchone():
            return {"response": 2, "message": "Username already exists, choose a different name"}

        donor_insert_sql = """
        INSERT INTO grlib.DONOR (Donor_ID,Donor_Name,Donor_Mobile, Donor_Email, Donor_Address, donor_city, donor_state, donor_pincode, is_pmi_member)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """
        user_insert_sql = """
        INSERT INTO grlib.USER (Role_ID,username,User_Mobile,password)
        VALUES (%s,%s,%s,%s) RETURNING User_ID;
        """
        cur.execute(user_insert_sql, (2, name, phone, password,))
        # Assumption that 2 is role id for donor and so on
        user_id = cur.fetchone()[0]
        cur.execute(donor_insert_sql, (
            user_id, name, phone, email, donor_address, donor_city, donor_state, donor_pincode,
            pmi_number != None,))
        conn.commit()
        cur.close()
        conn.close()
        res = 1
    else:
        res = 0
        donor_id = -1
        user_id = -1
    return {"User ID": user_id, "Name": name[0], "response": res}


def user_registration_response(name, panchayat, email, phone, password, id_proof, location_proof, address, student):
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
        # needs to include columns for id proof, address, email for the user as well but optional
        user_insert_sql = """
                INSERT INTO grlib.USER (Role_ID,username,User_Last_Name,User_Mobile,password)
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
                    INSERT INTO grlib.USER (Role_ID,usernameUser_Mobile,password)
                    VALUES (%s,%s,%s,%s,%s) RETURNING User_ID;
                    """
        cur.execute(user_insert_sql, (3, name, phone, password,))
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


def vol_registration_response(name, password, address, city, state, pincode, email, phone_number, pmi_number):
    # TODO where to input PMI_ID
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()

        volunteer_check_sql = """
            SELECT user_id, username
            FROM grlib."user"
            WHERE username=%s
            """

        cur.execute(volunteer_check_sql, (name,))
        if cur.fetchone():
            return {"response": 2, "message": "Username already exists, choose a different name"}

        volunteer_insert_sql = """
            INSERT INTO grlib.volunteer(
            volunteer_id, volunteer_name, volunteer_mobile, volunteer_address, volunteer_city, volunteer_state, volunteer_pincode, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
        user_insert_sql = """
            INSERT INTO grlib.USER (Role_ID,username,User_Mobile,password)
            VALUES (%s,%s,%s,%s) RETURNING User_ID;
            """
        cur.execute(user_insert_sql, (5, name, phone_number, password,))
        user_id = cur.fetchone()[0]
        cur.execute(volunteer_insert_sql, (
            user_id, name, phone_number, address, city, state, pincode, email,))
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
            user_check_sql = "select user_id,username,role_name" \
                             " from grlib.USER a join grlib.role b on a.role_id=b.role_id" \
                             " where (user_id=%s OR user_mobile=%s) and password= %s"
            cur.execute(user_check_sql, (user_id, user_id, password,))
        else:
            user_check_sql = "select user_id,username,role_name" \
                             " from grlib.USER a join grlib.role b on a.role_id=b.role_id" \
                             " where (username=%s) and password= %s"
            cur.execute(user_check_sql, (user_id, password,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user is not None:
            return {"Response": True, "Name": user[1], "Role": user[2], "ID": user[0]}
        else:
            return {"Response": False}
    else:
        return {"Response": False}

#admin

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

def appreciate_volunteer(volunteer_id, appreciation, admin_name):
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        appreciate_sql = """
        INSERT INTO grlib.volunteer_acknowledgements(
        volunteer_id, content, "from")
        VALUES (%s, %s, %s)
        """
        cur.execute(appreciate_sql, (volunteer_id, appreciation, admin_name,))
        conn.commit()
        cur.close()
        conn.close()
        return {'Response': True}

def assign_volunteer(volunteer_id, donor_id, donation_date, available_from, available_till):
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        volunteer_assign_sql ="""
        UPDATE grlib.book_to_be_collected
        SET assigned_volunteer_id=%s
        WHERE donor_id=%s and donation_date=%s and available_date_start=%s and available_date_end=%s 
        """
        cur.execute(volunteer_assign_sql, (volunteer_id, donor_id, donation_date, available_from, available_till,))
        conn.commit()
        cur.close()
        conn.close()
        return {'Response': 'Update Successful'}

def get_books_list():
    conn = connect_Postgres(
        host="localhost",
        database="postgres",
        user="grlib",
        password="pass"
    )
    if conn is not None:
        cur = conn.cursor()
        books_sql = """
        SELECT * FROM grlib.book ORDER BY book_id
        """
        cur.execute(books_sql)
        books_list = cur.fetchall()
        ret_list = []
        for book in books_list:
            ret_list.append({
                'book_id':book[0],
                'donor_id':book[1],
                'donation_date':book[2],
                'isbn':book[3],
                'book_title':book[4],
                'volunteer_id': book[5],
            })
        return ret_list




def get_book_categories():
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
    print(get_books_list())
