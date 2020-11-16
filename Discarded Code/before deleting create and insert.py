import csv
import sqlite3
from sqlite3 import Error
import re


gen_list = [1,2,3,4,5,6]

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

#create the tables
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

#insert data to the first table
def insertion_1(conn, pokemon):
    cur = conn.cursor()
    for row in pokemon:
        pdata = int(row[0])
        cur.execute("INSERT OR IGNORE INTO name (id, name, type_1, type_2) VALUES(?,?,?,?)",
                  (pdata, row[1], row[2], row[3]))
    conn.commit()

#insert data to the second table
def insertion_2(conn, pokemon):
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


        cur.execute("INSERT OR IGNORE INTO stats(pokemon_id, total, HP, Attack, Defense, Sp_Atk, Sp_Def, Speed) VALUES(?,?,?,?,?,?,?, ?)",
                  (pdata, total, hp, attack,
                  defense, sp_att, sp_def, speed))
    conn.commit()


#insert data to the second table
def insertion_3(conn, pokemon):
    cur = conn.cursor()
    for row in pokemon:
        pdata = int(row[0])
        generation = int(row[11])
        cur.execute("INSERT OR IGNORE INTO gen(pokemon_id, Generation, Legendary) VALUES(?,?,?)",
                  (pdata, generation, row[12]))
    conn.commit()

#prompt user for a request
def user_input():
    global response

    print("Welcome to the pokedex. Request information.")
    response = input()
    return True
    return response
    


#Use regular expressions to analyze request
def generation_request(conn, response):

    if re.search('generation', response, re.IGNORECASE):
        print('Generation requested')
        return True

def type_request(conn, response):
    test = '''Select name, type_1, type_2 FROM name WHERE (type_1 = ?) OR (type_2 = ?)'''
    cur = conn.cursor()

    type_list = ["Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting", "Fire", "Flying", "Ghost", "Grass",
             "Ground", "Ice", "Normal", "Poison", "Psychic", "Rock", "Steel", "Water"]

    for word in type_list:
        if re.search(word, response, re.IGNORECASE):
            print('Type requested')

            cur.execute(test, (word, word,))

            record = cur.fetchall()

            for row in record:
                print(row)
            

def legendary_request(conn, response):
    if re.search('legendar(ies)?', response, re.IGNORECASE):
        print('Legendary Requested')
        return True
def name_request(conn, pokemon, response):
    names = []
    for row in pokemon:
        names.append(row[1])
    for name in names:
        if re.search(name, response, re.IGNORECASE):
            print('name requested')
            return True
def order_request(response):
    order = ["highest", "lowest"]

    for word in order:
        if re.search(word, response, re.IGNORECASE):
            print("Order requested")
            return True
def main():
    database = 'pokemon.db'
    table_1 = """CREATE TABLE name(id integer, name text, type_1 text,
                    type_2 text,
                    PRIMARY KEY(id)
                    )"""

    table_2 = """CREATE TABLE stats(pokemon_id, total integer, HP integer, Attack integer, Defense integer, Sp_Atk integer, Sp_Def integer,
                    Speed integer,
                    FOREIGN KEY(pokemon_id) REFERENCES name(id)
                    )"""

    table_3 = """CREATE TABLE gen(pokemon_id, Generation integer, Legendary text,
                    FOREIGN KEY(pokemon_id) REFERENCES name(id)
                    )"""
    conn = create_connection(database)

    if conn is not None:
        create_table(conn, table_1)
        create_table(conn, table_2)
        create_table(conn, table_3)
    else:
        print("Error! cannot create the database connection.")
    insertion_1(conn, pokemon)
    insertion_2(conn, pokemon)
    insertion_3(conn, pokemon)
    while user_input() == True:
        generation_request(conn, response)
        type_request(conn, response)
        name_request(conn, pokemon, response)
        legendary_request(conn, response)
        order_request(response)
if __name__ == '__main__':
    main()
