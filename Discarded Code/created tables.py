import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
    
def main():
    database = 'pokemon.db'
    table_1 = """CREATE TABLE name(
                    id integer,
                    name text,
                    type_1 text,
                    type_2 text,
                    PRIMARY KEY(id)
                    );"""

    table_2 = """CREATE TABLE stats(
                    pokemon_id
                    total integer
                    HP integer
                    Attack integer,
                    Defense integer,
                    Sp_Atk integer,
                    Sp_Def integer,
                    Speed integer,
                    FOREIGN KEY(pokemon_id) REFERENCES name (id)
                    );"""

    table_3 = """CREATE TABLE gen(
                    pokemon_id,
                    Generation integer,
                    Legendary text,
                    FOREIGN KEY(pokemon_id) REFERENCES name (id)
                    );"""
    conn = create_connection(database)

    if conn is not None:
        create_table(conn, table_1)
        create_table(conn, table_2)
        create_table(conn, table_3)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
