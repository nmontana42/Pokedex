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

def declare_lists(pokemon):
    global type_list, gen_list

    type_list = ["Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting", "Fire", "Flying", "Ghost", "Grass",
             "Ground", "Ice", "Normal", "Poison", "Psychic", "Rock", "Steel", "Water"]
    gen_list = ['1','2','3','4','5','6']

    order = ["highest", "lowest"]

    names = []

    for row in pokemon:
        names.append(row[1])
    
    

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

def find_constraints(conn, response, type_list, gen_list):
    curr = conn.cursor()

    global gen_constraint, legend_constraint, type_constraint, gentype_constraint, generation_requested, type_requested
    type_requested = None
    generation_requested = None
    gen_constraint = None
    legend_constraint = None
    type_constraint = None
    gentype_constraint = None
    
    for generation_requested in gen_list:
        if re.search(generation_requested, response):
            gen_constraint = True
            for type_requested in type_list:
                if re.search(type_requested, response, re.IGNORECASE):
                    gentype_constraint = True
                    return gentype_constraint
            return gen_constraint, generation_requested
    if re.search('legendar(ies)?', response, re.IGNORECASE):
        legend_constraint = True
        return legend_constraint
    for type_requested in type_list:
        if re.search(type_requested, response, re.IGNORECASE):
            type_constraint = True
            return type_constraint, type_requested
        

def declare_variables(response):
    #declare sql select statements
    global gen_sel, gentype_sel, type_sel

    gen_sel = '''SELECT name, type_1, type_2 FROM pokemon WHERE Generation = ?'''
    gentype_sel = '''SELECT name, type_1, type_2 FROM pokemon WHERE ((type_1 = ?) or (type_2 = ?)) AND (Generation = ?)'''
    type_sel = '''Select name, type_1, type_2 FROM pokemon WHERE (type_1 = ?) OR (type_2 = ?)'''

    return gen_sel, gentype_sel, type_sel

#Use regular expressions to analyze request
def find(conn, gen_sel, generation_requested, gen_constraint, type_requested, type_sel, gentype_sel):
    cur = conn.cursor()

    if gentype_constraint is True:
        print("gen and type specific")
        cur.execute(gentype_sel, (type_requested, type_requested, generation_requested,))
        record1 = cur.fetchall()
        for row in record1:
            print(row)

    elif gen_constraint is True and type_constraint is None:
        print('Generation' + ' ' + generation_requested + ' requested')
        cur.execute(gen_sel, (generation_requested,))
        record = cur.fetchall()
        for row in record:
            print(row)
    elif type_constraint is True and gen_constraint is None:
        print(type_requested + ' ' + 'type' + ' ' + 'requested')
        cur.execute(type_sel, (type_requested, type_requested,))
        record = cur.fetchall()
        for row in record:
            print(row)
    
      


def order_request(response):
    order = ["highest", "lowest"]

    for word in order:
        if re.search(word, response, re.IGNORECASE):
            print("Order requested")
            return True
def main():
    database = 'pokemon.db'
    declare_lists(pokemon)
    conn = create_connection(database)
    if conn is not None:
        while user_input() == True:
            find_constraints(conn, response, type_list, gen_list)
            declare_variables(response)
            find(conn, gen_sel, generation_requested, gen_constraint, type_requested, type_sel, gentype_sel)
            order_request(response)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
