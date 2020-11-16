import csv
import sqlite3
from sqlite3 import Error
import re

#open the pokedex data (retrieved from dataworld)
def open_csv():
    with open("I:\Python Projects\Python SQL\pokemon.csv") as pokemon_data:
        Pokemon_reader = csv.reader(pokemon_data, delimiter = ',')
        pokemon_list = list(Pokemon_reader)
        pokemon_sql = pokemon_list[1:]
    return pokemon_sql

pokemon = open_csv()

def declare_lists(pokemon):
    global type_list, gen_list, order, leg, names, stat_list

    type_list = ["Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting", "Fire", "Flying", "Ghost", "Grass",
             "Ground", "Ice", "Normal", "Poison", "Psychic", "Rock", "Steel", "Water"]
    gen_list = ['1','2','3','4','5','6']

    order = ["highest", "lowest"]

    stat_list = ["total", "HP", "Attack", "Defense", "Speed"]

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

#user input
def user_input():
    global response

    print("Welcome to the pokedex. Request information.")
    response = input()
    return True
    return response

def find_constraints(conn, response, type_list, gen_list, names):
    curr = conn.cursor()

    global gen_constraint, legend_constraint, type_constraint, gentype_constraint, generation_requested, type_requested
    global genleg_constraint, typeleg_constraint, name_constraint, name_requested 
    
    type_requested = None
    generation_requested = None
    gen_constraint = None
    legend_constraint = None
    type_constraint = None
    gentype_constraint = None
    genleg_constraint = None
    typeleg_constraint = None
    name_constraint = None
    name_requested = None

    #Find user requests using regular expressions
    for generation_requested in gen_list:
        if re.search(generation_requested, response):
            gen_constraint = True
            for type_requested in type_list:
                if re.search(type_requested, response, re.IGNORECASE):
                    gentype_constraint = True
                    return gentype_constraint
            if re.search('legend(ary)?', response, re.IGNORECASE):
                genleg_constraint = True
                return genleg_constraint
            return gen_constraint, generation_requested
    
    if re.search('legendar(ies)?', response, re.IGNORECASE):
        for type_requested in type_list:
            if re.search(type_requested, response, re.IGNORECASE):
                typeleg_constraint = True
                return typeleg_constraint
        legend_constraint = True
        return legend_constraint
    for type_requested in type_list:
        if re.search(type_requested, response, re.IGNORECASE):
            type_constraint = True
            return type_constraint, type_requested
    for name_requested in names:
        if re.search(name_requested, response, re.IGNORECASE):
            name_constraint = True
            return name_constraint, name_requested
def find_stat_constraints(conn, resposne, order, stat_list):
    global order_constraint, stat_constraint, order_requested, stat_requested

    order_constraint = None
    stat_constraint = None
    order_requested = None
    stat_requested = None

    if re.search('sp(ecial)?( )?att(ack)?', response, re.IGNORECASE):
        print('Special Attack Stat Request')
        stat_requested = 'Sp_Atk'
        stat_constraint = True
        return stat_requested, stat_constraint

    elif re.search('sp(ecial)?( )?def(ense)?', response, re.IGNORECASE):
        print('Special Defense Stat Request')
        stat_requested = 'Sp_Def'
        stat_constraint = True
        return stat_requested, stat_constraint
    elif re.search('total', response, re.IGNORECASE):
        stat_requested = 'total'
        stat_constraint = True
        return stat_constraint, stat_requested
    elif re.search('HP', response, re.IGNORECASE):
        stat_requested = 'HP'
        stat_constraint = True
        return stat_constraint, stat_requested
    elif re.search('Attack', response, re.IGNORECASE):
        stat_requested = 'Attack'
        stat_constraint = True
        return stat_constraint, stat_requested
    elif re.search('Defense', response, re.IGNORECASE):
        stat_requested = 'Defense'
        stat_constraint = True
        return stat_constraint, stat_requested
    elif re.search('speed', response, re.IGNORECASE):
        stat_requested = 'Speed'
        stat_constraint = True
        return stat_constraint, stat_requested

def declare_variables(response):
    #declare sql select statements
    global gen_sel, gentype_sel, type_sel, leg_sel, genleg_sel, typeleg_sel, name_sel, sa_sel, sd_sel, total_sel, att_sel, def_sel, speed_sel, hp_sel

    gen_sel = '''SELECT name, type_1, type_2 FROM pokemon WHERE Generation = ?'''
    gentype_sel = '''SELECT name, type_1, type_2 FROM pokemon WHERE ((type_1 = ?) or (type_2 = ?)) AND (Generation = ?)'''
    type_sel = '''Select name, type_1, type_2 FROM pokemon WHERE (type_1 = ?) OR (type_2 = ?)'''
    leg_sel = '''SELECT name, type_1, type_2 FROM pokemon WHERE Legendary = "TRUE"'''
    genleg_sel = '''SELECT name, type_1, type_2 FROM pokemon WHERE (Generation = ?) AND (Legendary = "TRUE")'''
    typeleg_sel = '''SELECT name, type_1, type_2 FROM pokemon WHERE ((type_1 = ?) or (type_2 = ?)) AND (Legendary = 'TRUE')'''
    name_sel = '''SELECT type_1, type_2, total, HP, Attack, Defense, Sp_Atk, Sp_Def, Speed, Generation FROM pokemon WHERE (name = ?) '''
    sa_sel = '''SELECT name, type_1, type_2, Sp_Atk FROM pokemon ORDER BY Sp_Atk DESC LIMIT 10'''
    sd_sel = '''SELECT name, type_1, type_2, Sp_Def FROM pokemon ORDER BY Sp_Def DESC LIMIT 10'''
    total_sel = '''SELECT name, type_1, type_2, total FROM pokemon ORDER BY total DESC LIMIT 10'''
    att_sel = '''SELECT name, type_1, type_2, Attack FROM pokemon ORDER BY Attack DESC LIMIT 10'''
    def_sel = '''SELECT name, type_1, type_2, Defense FROM pokemon ORDER BY Defense DESC LIMIT 10'''
    speed_sel = '''SELECT name, type_1, type_2, Speed FROM pokemon ORDER BY Speed DESC LIMIT 10'''
    hp_sel = '''SELECT name, type_1, type_2, HP FROM pokemon ORDER BY HP DESC LIMIT 10'''
    return gen_sel, gentype_sel, type_sel, leg_sel, genleg_sel, typeleg_sel, name_sel, sa_sel, sd_sel, total_sel, att_sel, def_sel, speed_sel, hp_sel

#Use regular expressions to analyze request
def find_function_one(conn, gen_sel, generation_requested, gen_constraint, type_requested, type_sel, gentype_sel, order, leg_sel, legend_constraint,
         genleg_sel, genleg_constraint, typeleg_sel, typeleg_constraint):
    cur = conn.cursor()

    if gentype_constraint is True:
        print("gen and type specific")
        cur.execute(gentype_sel, (type_requested, type_requested, generation_requested,))
        record = cur.fetchall()
        for row in record:
            print(row)
    elif genleg_constraint is True:
        print("Generation specific legendary request")
        cur.execute(genleg_sel, (generation_requested,))
        record = cur.fetchall()
        for row in record:
            print(row)
    elif typeleg_constraint is True:
        print("Type specific legendary request")
        cur.execute(typeleg_sel, (type_requested, type_requested,))
        record = cur.fetchall()
        for row in record:
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
    elif legend_constraint is True and typeleg_constraint is None:
        print('Legendary Request')
        cur.execute(leg_sel)
        record = cur.fetchall()
        for row in record:
            print(row)

#Find more requests
def find_function_two(conn, name_sel, name_requested, name_constraint):
    cur = conn.cursor()


    if name_constraint is True:
        print('Name Request:', name_requested)
        cur.execute(name_sel, (name_requested,))
        record = cur.fetchall()
        for row in record:
            print("types, total, attack, defense, special attack, special defense, speed, and generation: \n",  row)
        
def find_order_requests(conn, order_requested, order_constraint, stat_constraint, stat_requested, sa_sel, sd_sel,
                        speed_sel, hp_sel, def_sel, att_sel, total_sel):
    cur = conn.cursor()
    

    if stat_constraint is True:
        print('stat requested')
        if stat_requested == "total":
            cur.execute(total_sel)
            record = cur.fetchall()
            for row in record:
                print(row)
        elif stat_requested == "Attack":
            cur.execute(att_sel)
            record = cur.fetchall()
            for row in record:
                print(row)
        elif stat_requested == "Defense":
            cur.execute(def_sel)
            record = cur.fetchall()
            for row in record:
                print(row)
        elif stat_requested == "Sp_Atk":
            cur.execute(sa_sel)
            record = cur.fetchall()
            for row in record:
                print(row)
        elif stat_requested == "Sp_Def":
            cur.execute(sd_sel)
            record = cur.fetchall()
            for row in record:
                print(row)
        elif stat_requested == "HP":
            cur.execute(hp_sel)
            record = cur.fetchall()
            for row in record:
                print(row)
        elif stat_requested == "Speed":
            cur.execute(speed_sel)
            record = cur.fetchall()
            for row in record:
                print(row)

def main():
    database = 'pokemon.db'
    declare_lists(pokemon)
    conn = create_connection(database)
    if conn is not None:
        while user_input() == True:
            find_constraints(conn, response, type_list, gen_list, names)
            find_stat_constraints(conn, response, stat_list, order)
            declare_variables(response)
            find_function_one(conn, gen_sel, generation_requested, gen_constraint, type_requested, type_sel, gentype_sel, order, leg_sel, legend_constraint,
                 genleg_sel, genleg_constraint, typeleg_sel, typeleg_constraint)
            find_function_two(conn, name_sel, name_requested, name_constraint)
            find_order_requests(conn, order_requested, order_constraint, stat_constraint, stat_requested, sa_sel, sd_sel,
                        speed_sel, hp_sel, def_sel, att_sel, total_sel)

    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()