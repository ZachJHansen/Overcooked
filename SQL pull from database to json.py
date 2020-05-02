import sqlite3;
import json
def readSqliteTable():
    try:
        sqliteConnection = sqlite3.connect('C:/Users/Grant/Desktop/sqliteRecipeList.db')#hardcoded filepath to database storage
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_select_query = """SELECT * from smallSet"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")
        secondaryIngredients = ['water','salt','black pepper']
        json = '['
        for row in records:
            title = row[0]
            print(title)
            readableingredients = row[1]
            #print(readableingredients)
            instructions = row[2]
            #print(instructions)
            ingredientsSimplifed = row[3]
            ingredientsSimplifed = ingredientsSimplifed.split(',')
            #print(ingredientsSimplifed)
            ingredientsUnits = row[4]
            ingredientsUnits = ingredientsUnits.split(',')
            #print(ingredientsUnits)
            
            if len(ingredientsSimplifed) == len(ingredientsUnits):
                json = json + '{"name" : "' + title + '", "ingredients" : {'
                length = len(ingredientsSimplifed)
                for i in range(length):
                    json = json + '"' + ingredientsSimplifed[i].lstrip() + '":"' + ingredientsUnits[i].lstrip() + '",' 
                json = json[:-1] #delete trailing comma for last entry
                json = json + '},"leftover_score": 0,"buddy_recipes":{}},'
            
            else:
                print('unequal ingredients and units')
        json = json[:-2]#delete terminal },
        json = json + '}]'
        print(json)
        jsonobject = eval(json)
        print(jsonobject)
        #sql_update_query = "UPDATE LowIngredientsRecipes set buddyScore ='" + buddyScore + "' WHERE title = '" + title + "'"
            #cursor.execute(sql_update_query);
            #cursor.execute('COMMIT')
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

readSqliteTable()