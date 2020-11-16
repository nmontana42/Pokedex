import csv
import sqlite3
from sqlite3 import Error

#open the pokedex data (retrieved from dataworld)
def open_csv():
    with open("I:\Python Projects\Python SQL\pokemon.csv") as pokemon_data:
        Pokemon_reader = csv.reader(pokemon_data, delimiter = ',')
        pokemon_list = list(Pokemon_reader)
        pokemon_sql = pokemon_list[1:]
    return pokemon_sql

pokemon = open_csv()

#Create the connection to sqlite
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

#insert data to the second table
def insertion(conn, pokemon):
    cur = conn.cursor()
    for row in pokemon:
        pdata = int(row[0])
        total = int(row[4])
        hp = int(row[5])
        attack = int(row[6])
        defense = int(row[7])
        sp_att = int(row[8])
        sp_def = int(row[9])
        speed = int(row[10])
        generation = int(row[11])


        cur.execute("INSERT OR IGNORE INTO pokemon(id, name, type_1, type_2, total, HP, Attack, Defense, Sp_Atk, Sp_Def, Speed, Generation, Legendary) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  (pdata, row[1], row[2], row[3], total, hp, attack,
                  defense, sp_att, sp_def, speed, generation, row[12]))
    conn.commit()
def main():
    database = 'pokemon.db'
    conn = create_connection(database)

    if conn is not None:
        insertion(conn, pokemon)
    conn.close()
if __name__ == '__main__':
    main()
