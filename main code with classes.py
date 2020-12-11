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
    gen_sel = '''SELECT name, type_1, type_2 FROM pokemon WHERE Generation = ?'''
    type_sel = '''Select name, type_1, type_2 FROM pokemon WHERE (type_1 = ?) OR (type_2 = ?)'''
    gentype_sel = '''SELECT name, type_1, type_2 FROM pokemon WHERE ((type_1 = ?) or (type_2 = ?)) AND (Generation = ?)'''
    leg_sel = '''SELECT name, type_1, type_2 FROM pokemon WHERE Legendary = "TRUE"'''
    genleg_sel = '''SELECT name, type_1, type_2 FROM pokemon WHERE (Generation = ?) AND (Legendary = "TRUE")'''
    typeleg_sel = '''SELECT name, type_1, type_2 FROM pokemon WHERE ((type_1 = ?) or (type_2 = ?)) AND (Legendary = 'TRUE')'''
    name_sel = '''SELECT type_1, type_2, total, HP, Attack, Defense, Sp_Atk, Sp_Def, Speed, Generation FROM pokemon WHERE (name = ?) '''

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
    
    response = input()
    return True
    return response

            
def main():
    while user_input() == True:
        conn = Find_Data.create_connection('pokemon.db')
        Generation = Search(conn, response, Search.gen_list, Search.gen_sel)
        Types = Search(conn, response, Search.type_list, Search.type_sel)
        Legendary = Search(conn, response, None, Search.leg_sel)
        Names = Search(conn, response, names_list, Search.name_sel)
        Find_Data.sql_Alpha(Generation)
        Find_Data.sql_Bravo(Types)
        Find_Data.sql_Gamma(Legendary)
        Find_Data.sql_Alpha(Names)
        if Generation.constraint is True and Types.constraint is True:
            print("Generation and Type")
            cur = conn.cursor()
            cur.execute(Search.gentype_sel, (Types.request, Types.request, Generation.request,))
            record = cur.fetchall()
            for row in record:
                print(row)
        Find_Data.sql_Gamma(Legendary)
if __name__ == '__main__':
    main()
