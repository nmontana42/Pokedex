import csv
import sqlite3
from sqlite3 import Error
import re

#open the pokedex data (retrieved from data.world)
def open_csv():
    with open("I:\Python Projects\Pokedex\pokemon.csv") as pokemon_data:
        Pokemon_reader = csv.reader(pokemon_data, delimiter = ',')
        pokemon_list = list(Pokemon_reader)
        pokemon_sql = pokemon_list[1:]
    return pokemon_sql
names_list = []
pokemon = open_csv()

for row in pokemon:
    names_list.append(row[1])

#Search finds base data, returns requests, constraints, executes SQL commands
class Search:
    #SQL select statements
    GEN_SELECT = '''SELECT name, type_1, type_2 FROM pokemon WHERE Generation = ?'''
    TYPE_SELECT = '''Select name, type_1, type_2 FROM pokemon WHERE (type_1 = ?) OR (type_2 = ?)'''
    GENTYPE_SELECT = '''SELECT name, type_1, type_2 FROM pokemon WHERE ((type_1 = ?) or (type_2 = ?)) AND (Generation = ?)'''
    LEG_SELECT = '''SELECT name, type_1, type_2 FROM pokemon WHERE Legendary = "TRUE"'''
    GENLEG_SELECT = '''SELECT name, type_1, type_2 FROM pokemon WHERE (Generation = ?) AND (Legendary = "TRUE")'''
    TYPE_LEG_SELECT = '''SELECT name, type_1, type_2 FROM pokemon WHERE ((type_1 = ?) or (type_2 = ?)) AND (Legendary = 'TRUE')'''
    NAME_SELECT = '''SELECT type_1, type_2, total, HP, Attack, Defense, Sp_Atk, Sp_Def, Speed, Generation FROM pokemon WHERE (name = ?) '''

    #Stat select statements
    sa_sel = '''SELECT name, type_1, type_2, Sp_Atk FROM pokemon ORDER BY Sp_Atk (DESC (LIMIT = 10)'''
    sd_sel = '''SELECT name, type_1, type_2, Sp_Def FROM pokemon ORDER BY Sp_Def (DESC (LIMIT =  10)'''
    total_sel = '''SELECT name, type_1, type_2, total FROM pokemon ORDER BY total (DESC (LIMIT = 10)'''
    att_sel = '''SELECT name, type_1, type_2, Attack FROM pokemon ORDER BY Attack (DESC (LIMIT = 10)'''
    def_sel = '''SELECT name, type_1, type_2, Defense FROM pokemon ORDER BY Defense (DESC (LIMIT = 10)'''
    speed_sel = '''SELECT name, type_1, type_2, Speed FROM pokemon ORDER BY Speed (DESC LIMIT =  10'''
    hp_sel = '''SELECT name, type_1, type_2, HP FROM pokemon ORDER BY HP DESC LIMIT = 10'''
    
    type_list = ["Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting", "Fire", "Flying", "Ghost", "Grass",
             "Ground", "Ice", "Normal", "Poison", "Psychic", "Rock", "Steel", "Water"]
    gen_list = ['1','2','3','4','5','6']

    stat_list = ["total", "HP", "Attack", "Defense", "Speed"]

    def __init__(self, conn, response, data, statement):
        self.response = response
        self.constraint = None
        self.data = data
        self.conn = conn
        self.statement = statement
    def regex(self):
        for self.request in self.data:
            if re.search(self.request, self.response, re.IGNORECASE):
                self.constraint = True
                return self.request
        if self.constraint is True:
            return self.constraint
    def regex_Bravo(self):
        if re.search('legendar(ies)?', self.response, re.IGNORECASE):
            self.constraint = True
            return self.constraint

#Takes the search class, and its variables, to find and produce the data using sqllite3 functions
class Find_Data(Search):


    def __init__(self, database, conn, request, statement):
        self.request = request
        self.statement = statement
        self.conn = conn
        self.database = database

    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn

        
    def sql_Alpha(self):
        Search.regex(self)
        cur = self.conn.cursor()
        if self.constraint is True:
            print("Data recorded")
            cur.execute(self.statement, (self.request,))
            self.record = cur.fetchall()
            return self.record
    def sql_Bravo(self):
        Search.regex(self)
        cur = self.conn.cursor()
        if self.constraint is True:
            print("Data recorded")
            cur.execute(self.statement, (self.request, self.request))
            self.record = cur.fetchall()
            return self.record
    def sql_Gamma(self):
        Search.regex_Bravo(self)
        cur = self.conn.cursor()
        if self.constraint is True:
            print("Data recorded")
            cur.execute(self.statement)
            self.record = cur.fetchall()
            return self.record

def user_input():
    global response

    print("Helpful Information:\n")
    print("Type options:", Search.type_list, "\n")
    print("Generation options:", Search.gen_list, "\n")
    print("User instructions:\n")
    print("1: Enter a known Pokemon name\n")
    print("2: Enter a known Pokemon type\n")
    print("3: Enter a generation number to get all Pokemon from a certain generation\n")
    print("4: Enter '(type) pokemon from generation 1-6' to get a certain type from a certain generation.\n")
    print("5: Enter 'legendaries' to get all legendary pokemon or 'legendaries' from a certain generation\n")
    print("Or specific type legendaries")
    
    response = input()
    return True
    return response

            
def main():
    while user_input() == True:
        conn = Find_Data.create_connection('pokemon.db')
        Generation = Search(conn, response, Search.gen_list, Search.GEN_SELECT)
        Types = Search(conn, response, Search.type_list, Search.TYPE_SELECT)
        Legendary = Search(conn, response, None, Search.LEG_SELECT)
        Names = Search(conn, response, names_list, Search.NAME_SELECT)
        Find_Data.sql_Alpha(Generation)
        Find_Data.sql_Bravo(Types)
        Find_Data.sql_Gamma(Legendary)
        Find_Data.sql_Alpha(Names)

        #Generation and Types
        if Generation.constraint is True and Types.constraint is True:
            print("Generation | Type")
            cur = conn.cursor()
            cur.execute(Search.GENTYPE_SELECT, (Types.request, Types.request, Generation.request,))
            record = cur.fetchall()
            for row in record:
                print(row)
        #Generation and Legendaries
        elif Legendary.constraint is True and Generation.constraint is True:
            print("Generation | Legendary")
            cur = conn.cursor()
            cur.execute(Search.GENLEG_SELECT, (Generation.request,))
            record = cur.fetchall()
            for row in record:
                print(row)
        elif Legendary.constraint is True and Types.constraint is True:
            print("Types | Legendary")
            cur = conn.cursor()
            cur.execute(Search.TYPE_LEG_SELECT, (Types.request, Types.request,))
            record = cur.fetchall()
            for row in record:
                print(row)

        elif Generation.constraint is True:
            for row in Generation.record:
                print(row)
        elif Types.constraint is True:
            for row in Types.record:
                print(row)
        elif Names.constraint is True:
            for row in Names.record:
                stat_dict = {'type 1': row[0], 'type 2': row[1], 'total': row[2],'HP':row[3], 'attack':row[4], 'defense':row[5], 'special attack':row[6], 'special defense':row[7],
                         'speed':row[8], 'generation':row[9]}
            for i in stat_dict.items():
                print(i)
        elif Legendary.constraint is True:
            for row in Legendary.record:
                print(row)
if __name__ == '__main__':
    main()
