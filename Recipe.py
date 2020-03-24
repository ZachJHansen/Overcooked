from bitarray import bitarray   
import json
from jsmin import jsmin                                     # pip install bitarray

# Globals
COOKWARE_LENGTH = 100

class Recipe:
    def __init__(self, name, ingredients, quantities, **kwargs):    # Not all recipes will have information such as complexity and calorie count
        self.name = name                                            # Hence, None initialization or empty arrays
        self.primary_ingredients = ingredients[0]                   # Minimum of recipe name, quantities, and ingredients (tuple of arrays) must be provided
        self.secondary_ingredients = ingredients[1]
        self.primary_quantities = quantities[0]
        self.secondary_quantities = quantities[1]
        self.allergens = kwargs.get('allergens', [])
        self.restrictions = kwargs.get('restrictions', [])
        self.complexity = kwargs.get('complexity', None)
        self.time = kwargs.get('time', None)
        self.calories = kwargs.get('calories', None)
        self.link = kwargs.get('link', None)
        self.leftover_score = kwargs.get('leftover_score', 0)
        self.buddies = kwargs.get('buddies', [])
        self.buddy_scores = kwargs.get('buddy_scores', [])
        self.cookware = kwargs.get('cookware', bitarray(COOKWARE_LENGTH))

    def update_tags(self, **kwargs):                                # Update any of the standard members above, or add new members with kwargs dict
        for key, value in kwargs.items():
            setattr(self, key, value)

    # Restrict ourselves to primary ingredients for now
    # MDU = minimum discrete unit purchasable at store (D)
    # S = minimum natural number st S * MDU > Quanitity Required
    def update_leftover_score(self, table_data):
        leftovers = []
        for ingr_table in table_data:
            S = 1
            MDU = ingr_table['MDU']
            ingr_index = self.primary_ingredients.index(ingr_table['id'])
            required = self.primary_quantities[ingr_index]
            while (S * MDU < required):     
                S += 1
            leftover = (S * MDU - required) * ingr_table['weight']
            leftovers.append(leftover)
        self.leftover_score = sum(leftovers)

    def update_buddies(self):
        print("Stub function")
        
if __name__=="__main__":
    if False:
        ingredients = tuple((["rice", "beans"], ["red pepper"]))
        additional_info = {
            "restrictions": ["vegan", "gluten free"],
            "time": 45,
            "complexity": "hard",
            "new_arg": "This wasn't in the original constructor"
        }
        r1 = Recipe("Spaghetti-os", ingredients)
        print(r1.name)
        r1.update_tags(**additional_info)
        print(r1.link)
        print(r1.restrictions)
        print("New Member:", r1.new_arg)
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