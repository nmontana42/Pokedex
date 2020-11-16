import csv
import sqlite3
from sqlite3 import Error

def open_csv():
    with open("I:\Python Projects\Python SQL\pokemon.csv") as pokemon_data:
        Pokemon_reader = csv.reader(pokemon_data, delimiter = ',')
        pokemon_list = list(Pokemon_reader)
        pokemon_sql = pokemon_list[1:]
    return pokemon_sql
pokemon = open_csv()

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
    database = 'Pokemon.db'

    table_1 = """CREATE TABLE name/type(
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
                    Sp. Atk integer,
                    Sp. Def integer,
                    Speed integer,
                    FOREIGN KEY(pokemon_id) REFERENCES name/type (id)
                    );"""

    table_3 = """CREATE TABLE gen/leg(
                    pokemon_id,
                    Generation integer,
                    Legendary text,
                    FOREIGN KEY(pokemon_id) REFERENCES name/type (id)
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
