from get_values import *

conn = connect_Postgres(
    host="localhost",
    database="postgres",
    user="grlib",
    password="pass"
)

print(conn)