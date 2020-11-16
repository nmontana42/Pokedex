import sqlite3
from sqlite3 import Error

#Create the connection to sqlite
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

#create the tables
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = 'pokemon.db'

    table = """CREATE TABLE pokemon(id integer, name text, type_1 text,
                    type_2 text, total integer, HP integer, Attack integer, Defense integer, Sp_Atk integer, Sp_Def integer,
                    Speed integer, Generation integer, Legendary text)"""

    conn = create_connection(database)
    if conn is not None:
        create_table(conn, table)
    else:
        print("error")
if __name__ == '__main__':
    main()
