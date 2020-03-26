import json
from Recipe import Recipe
from jsmin import jsmin                                     # pip install jsmin

def instantiate_recipe(record, prim_ingr_table):
    name = record["name"]
    ingredients = tuple((record["primary_ingredients"], record["secondary_ingredients"]))
    table_data = []
    for pi in ingredients[0].keys():
        table_data.append(prim_ingr_table[pi])
    r = Recipe(name, ingredients)
    return(r, table_data)

# Newly added recipes stored in a JSON file at PATH must have the leftover scores added
# File at PATH will be overwritten with updated values
def update_lo_scores(path):
    with open("tables.jsonc") as tables:
        with open(path) as recipe_file:
            recipe_records = json.loads(jsmin(recipe_file.read()))
            prim_ingr_table = json.loads(jsmin(tables.read()))["primary_ingredients"]
    for recipe in recipe_records:
        if (recipe["leftover_score"] is None):
            r, table_data = instantiate_recipe(recipe, prim_ingr_table)
            r.update_leftover_score(table_data)
            recipe["leftover_score"] = r.leftover_score
            print("Leftover score", r.leftover_score)
    open(path, "w").write(json.dumps(recipe_records))

# When new recipes are added, the entire database's buddies must be updated
# (A new best bud could be found in the new recipes)        
# But maybe to reduce complexity we are only interested in overlapping recipes that share > 0 primary ingredients
def update_new_buddies(path):
    ingredients = set()                                           # Union of all primary ingredients required by new recipes
    with open("tables.jsonc") as tables:
        with open(path) as recipe_file:
            new_recipes = json.loads(jsmin(recipe_file.read()))
            prim_ingr_table = json.loads(jsmin(tables.read()))["primary_ingredients"]
    for recipe in new_recipes:
        for ingr in recipe["primary_ingredients"].keys():
            ingredients.add(ingr)
    old_recipes = read_from_db(ingredients)                         # Only compare recipes that share primary ingredients with new recipes
    #recipes = old_recipes + new_recipes                         # Shallow copies, no memory issue, all new + fetched recipes will be updated
    recipes = new_recipes                                           # REMOVE EVENTUALLY
    for recipe in recipes:
        r, table_data = instantiate_recipe(recipe, prim_ingr_table)
        n_minus_1 = [r for r in recipes if r != recipe]
        r.update_buddies(n_minus_1, prim_ingr_table)
        print("Buddies")
        print(r.buddies)
        recipe["buddies"] = r.buddies
    open("output.jsonc", "w").write(json.dumps(recipes))                  # Overwrite file with updated recipes from entire DB + new recipes

def read_from_db(ingredients):
    # fetch all recipes from db that contain at least one of the specified ingredients
    # return a list of dicts
    return(["stub function"])


if __name__=="__main__":
    update_lo_scores("master_recipes.jsonc")
    update_new_buddies("master_recipes.jsonc")
