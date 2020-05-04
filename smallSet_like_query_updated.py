#works with sqliteRecipeList.db
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

#Grabs the main_ingredient parameter off the url
@app.route('/reciperetrieve', methods=['GET'])
def api_filter():
    query_parameters = request.args
    
    main_ingredient = query_parameters.get('main_ingredient')
    
    to_filter = []

    if main_ingredient:
      to_filter.append("%" + main_ingredient + "%")	

	#connection to database sqliteRecipeList.db 
    conn = sqlite3.connect('sqliteRecipeList.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
	#Searches database for string that matches main_ingredient from the url
    print(to_filter)
    results = cur.execute("SELECT title, ingredients, instructions FROM smallSet WHERE title LIKE ?", to_filter).fetchall()

    return jsonify(results)

  
app.run()
