#works with Recipe.db
import flask
from flask import request, jsonify
import sqlite3
from parser import generate_meal_plan
import json
import sys

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Returns a cursor or None in case of failure
def establish_connection(db):
    try:
        conn = sqlite3.connect(db)
    except Exception as e:
        print("Error while establishing database connection:", e)
        return(None)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    return(cur)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def insertion_wrapper(cursor, table, columns, values):
    sql = "INSERT INTO " + table + "("
    for c in columns:
        col = c + ", "
        sql += col
    sql = sql[:-2] + ") VALUES ("
    for i in range(len(values)):
        sql += "?, "
    sql = sql[:-2] + ");"
    cursor.execute(sql, values)
    return(cur.lastrowid)

# List of possible recipe constraints
@app.route('/', methods=['GET'])
def api_filter():
    query_parameters = request.args
    
    main_ingredient = query_parameters.get('main_ingredient')
    calories = query_parameters.get('calories')
    complexity = query_parameters.get('complexity')
    
    #print('parameters = ')
    #print(query_parameters)
    #print(mainingredient)
    #print(calories)
    #print(complexity)
    
	#creates a query
    query = "SELECT * FROM recipes WHERE"
    to_filter = []

    if main_ingredient:
      query += ' main_ingredient=? AND' 
      to_filter.append(main_ingredient)	
    if calories:
      query += ' calories<=? AND'
      to_filter.append(calories)
    if complexity:
      query += ' complexity=? AND'
      to_filter.append(complexity)
	  
    query = query[:-4] + ';'

    #conn = sqlite3.connect('Recipes.db')
    #conn.row_factory = dict_factory
    #cur = conn.cursor()
    cur = establish_connection('Recipes.db')
#    results = cur.execute(query, to_filter).fetchall()

    try:
        results = cur.execute(query, to_filter).fetchall()
        #print("Length: ", len(results), file=sys.stderr)
        #for row in results:
        #  print(row, file=sys.stderr)
        mp = generate_meal_plan(results, 5)
        mp.print_recipes(sys.stderr)
        mp.print_grocery(sys.stderr)
        return(mp.recipes)
    except Exception as e:
        print("Error while retrieving results from DB", file=sys.stderr)
        return None

    # Generate meal plan from results
    #data = jsonify(results)
    #print("Data", file=sys.stderr)
    #for key in data:
    #  print(data[key], file=sys.stderr)
    #mp = generate_meal_plan(jsonify(results), 5)
    #mp.print_recipes()
    #mp.print_grocery()
    #return(jsonify(results))
    #data = results.get_json()
    #type(data))
    #print(data)
    #return(jsonify(results))
    #print(query)
    #print(to_filter)
	
    #return(query_parameters)
    
@app.route('/add_recipe', methods=['POST'])
def add_recipe(recipe_json):
    # Connect to DB
    cur = establish_connection('Recipes.db')

    # Insert recipe data into recipes table
    columns = []
    values = []
    for key in recipe_json:
        if (key != "primary_ingredients"):
            columns.append(key)
            values.append(recipe_json[key])
    rowid = insertion_wrapper(cur, 'recipes', columns, values)

    # Insert ingredient data into ingredients table
    columns = []
    values = []



    # Insert ingredients into 
    
    primary_ingredients = recipe_json["primary_ingredients"]
    #for ingr in primary_ingredients:




app.run()


# https://stackoverflow.com/questions/11542930/inserting-an-array-into-sqlite3-python
'''
CREATE TABLE IF NOT EXISTS ingredients ( 
  recipe_id INTEGER NOT NULL,
  code VARCHAR(8) NOT NULL, 
  quantity REAL NOT NULL, 
  units varchar(8), 
  PRIMARY KEY(recipe_id, code),
  FOREIGN KEY(recipe_id) 
    REFERENCES recipes(recipe_id)
    ON DELETE CASCADE);
ALTER TABLE ingredients
  ADD FOREIGN KEY(code)
    REFERENCES ingr_lookup(code)
    ON DELETE CASCADE;
  '''