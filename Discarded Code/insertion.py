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

def create_connection(Pokemon.db):
    conn = None
    try:
        conn = sqlite3.connect('Pokemon.db')
        return conn
    except Error as e:
        print(e)
    return conn

def create_project(conn, pokemon, first_table):



    for row in pokemon:
        c.execute("INSERT INTO name/type (id, name, type_1, type_2)VALUES(?,?,?,?)",
                  row[1], row[2], row[3], row[4])
        c.execute("INSERT INTO stats(pokemon_id, total, HP, Attack, Defense, Sp. Atk, Sp. Def, Speed) VALUES(?,?,?,?,?,?,?)", row[1], row[5], row[6], row[7],
                  row[8], row[9], row[10], row[11])
        c.execute("INSERT INTO gen/leg(pokemon_id, Generation, Legendary) VALUES(?,?,?)", row[1], row[12], row[13])
