import json
import Recipe
from jsmin import jsmin                                     # pip install jsmin

if __name__=="__main__":
    with open("tables.jsonc") as tables:
        with open("recipeV1.jsonc") as recipe_file:
            recipe_records = json.loads(jsmin(recipe_file.read()))
            for recipe in recipe_records:
                name = recipe["name"]
                ingredients = tuple((recipe["primary_ingredients"], recipe["secondary_ingredients"]))
                quantities = tuple((recipe["primary_quanitites"], recipe["secondary_quantities"]))
                r = Recipe(name, ingredients, quantities)
                r.update_leftover_score(ingredients, weights, units)