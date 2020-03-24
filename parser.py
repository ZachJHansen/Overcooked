import json
from Recipe import Recipe
from jsmin import jsmin                                     # pip install jsmin

if __name__=="__main__":
    with open("tables.jsonc") as tables:
        with open("recipeV1.jsonc") as recipe_file:
            recipe_records = json.loads(jsmin(recipe_file.read()))
            prim_ingr_table = json.loads(jsmin(tables.read()))["Primary_ingredients"]
            for recipe in recipe_records:
                name = recipe["name"]
                ingredients = tuple((recipe["primary_ingredients"], recipe["secondary_ingredients"]))
                quantities = tuple((recipe["primary_quanitites"], recipe["secondary_quantities"]))
                table_data = []
                for pi in ingredients[0]:
                    table_data.append(prim_ingr_table[pi])
                r = Recipe(name, ingredients, quantities)
                r.update_leftover_score(table_data)
                print("Leftover score", r.leftover_score)