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
    conn = create_connection(database)

    if conn is not None:
        while user_input() == True:
            generation_request(conn, response)
            type_request(conn, response)
            name_request(conn, pokemon, response)
            legendary_request(conn, response)
            order_request(response)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
