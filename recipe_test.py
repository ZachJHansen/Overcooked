#works with Recipe.db
import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

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

    conn = sqlite3.connect('Recipes.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

    #print(query)
    #print(to_filter)
	
    #return(query_parameters)
    

app.run()