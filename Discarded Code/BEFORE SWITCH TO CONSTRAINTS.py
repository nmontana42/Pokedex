import csv
import sqlite3
from sqlite3 import Error
import re

#open the pokedex data (retrieved from dataworld)
def open_csv():
    with open("E:\Python Projects\Python SQL\pokemon.csv") as pokemon_data:
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
def generation_request(conn, response, type_list):
    #base case if user only specifies a generation
    sql = '''SELECT name, type_1, type_2 FROM pokemon WHERE Generation = ?'''
    gen_list = ['1','2','3','4','5','6']
    global generation_requested

    if re.search('generation', response, re.IGNORECASE):
        for generation_requested in gen_list:
            if re.search(generation_requested, response):
                print('Generation' + ' ' + generation_requested + ' requested')
                cur = conn.cursor()
                cur.execute(sql, (generation_requested,))

                record = cur.fetchall()
                for row in record:
                    print(row)

                return generation_requested
                return True
    else:
        generation_requested = 0
        return generation_requested

def type_request(conn, response, generation_request, generation_requested):
    global type_list
    test = '''Select name, type_1, type_2 FROM pokemon WHERE (type_1 = ?) OR (type_2 = ?)'''
    test2 = '''SELECT name, type_1, type_2 FROM pokemon WHERE ((type_1 = ?) or (type_2 = ?)) AND (Generation = ?)'''
    cur = conn.cursor()
    type_list = ["Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting", "Fire", "Flying", "Ghost", "Grass",
             "Ground", "Ice", "Normal", "Poison", "Psychic", "Rock", "Steel", "Water"]


    if generation_requested == 0:
        for word in type_list:
            if re.search(word, response, re.IGNORECASE):
                print(word + ' ' + 'type' + ' ' + 'requested')
                cur.execute(test, (word, word,))
                record = cur.fetchall()
                for row in record:
                    print(row)
                

    else:
        for word in type_list:
            if re.search(word, response, re.IGNORECASE):
                print("gen and type specific")
                cur.execute(test2, (word, word, generation_requested,))
                record1 = cur.fetchall()
                for row in record1:
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
            type_request(conn, response, generation_request, generation_requested, type_list)
            name_request(conn, pokemon, response)
            legendary_request(conn, response)
            order_request(response)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
