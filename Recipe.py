from bitarray import bitarray   
import sys

# Globals
COOKWARE_LENGTH = 100

class Recipe:
    def __init__(self, name, ingredients, quantities, **kwargs):                # Not all recipes will have information such as complexity and calorie count
        self.name = name                                            # Hence, None initialization or empty arrays
        self.ingredients = ingredients                              # Minimum of recipe name, quantities, and ingredients must be provided
        self.quantities = [float(q) for q in quantities.split(",")]
        self.allergens = kwargs.get('allergens', [])
        self.restrictions = kwargs.get('restrictions', [])
        self.complexity = kwargs.get('complexity', None)
        self.time = kwargs.get('time', None)
        self.calories = kwargs.get('calories', None)
        self.link = kwargs.get('link', None)
        self.leftover_score = kwargs.get('leftover_score', 0)
        self.buddies = kwargs.get('buddies', {})
        self.cookware = kwargs.get('cookware', bitarray(COOKWARE_LENGTH))

    def update_tags(self, **kwargs):                                # Update any of the standard members above, or add new members with kwargs dict
        for key, value in kwargs.items():
            setattr(self, key, value)

    # Restrict ourselves to primary ingredients for now
    # MDU = minimum discrete unit purchasable at store (D)
    # S = minimum natural number st S * MDU > Quanitity Required (QR)
    def update_leftover_score(self, table_data):
        leftovers = []
        for ingr_table in table_data:
            QR_idx = self.ingredients.index(ingr_table["Ingredient"])
            QR = self.quantities[QR_idx]
            leftovers.append(ingredient_score(ingr_table, QR))
        self.leftover_score = sum(leftovers)

    # Parameters: All recipes except recipe in question, lookup table for primary ingredients
    # Generate the leftover score of every recipe when combined with the recipe in question
    # Updates an array of the K recipes that pair best with given recipe (lowest leftover score), tuples (id, leftover score)
    def update_buddies(self, n_minus_1, table, K):
        buddies = [(0, float("inf")) for i in range(K)]
        for candidate in n_minus_1:
            table_data = []
            combined_ingredients = set([*(self.ingredients)] + [*(candidate.ingredients)])       # unpack keys into list literals and combine
            for pi in combined_ingredients:
                table_data.append(table_lookup(table, pi))
            leftovers = []
            for ingr_table in table_data:
                _id = ingr_table['Ingredient']
                if _id in self.ingredients:
                    QR_1 = self.quantities[self.ingredients.index(_id)]
                else:
                    QR_1 = 0
                if _id in candidate.ingredients:
                    QR_2 = candidate.quantities[candidate.ingredients.index(_id)]
                else:
                    QR_2 = 0
                leftovers.append(ingredient_score(ingr_table, QR_1+QR_2))
            score = sum(leftovers)
            curr_max_index = 0
            curr_max_score = buddies[0][1]
            for i, bud in enumerate(buddies):
                bID, bScore = bud[0], bud[1]
                if bScore > curr_max_score:
                    curr_max_score = bScore
                    curr_max_index = i
            if curr_max_score > score:
                del buddies[curr_max_index]
                buddies.append(tuple((candidate.name, score)))
        for b in buddies:
            self.buddies[b[0]] = b[1]


class MealPlan:
    def __init__(self, recipes_array, prim_ingr_table):
        self.meal_count = len(recipes_array)
        self.ingr_set = set()
        self.recipes = []
        self.tabular = []
        self.grocery_list = {}
        for recipe in recipes_array:
            r, table_data = instantiate_recipe(recipe, prim_ingr_table)
            self.recipes.append(r)
            self.tabular += table_data
            for pi in r.ingredients:
                if not pi in self.ingr_set:
                    self.ingr_set.add(pi)
            for si in r.secondary_ingredients:
                if not si in self.ingr_set:
                    self.ingr_set.add(si)
        for ingr in self.ingr_set:
            self.grocery_list[ingr] = 0
        for recipe in self.recipes:
            for i in self.ingr_set:
                if i in recipe.ingredients:
                    self.grocery_list[i] += recipe.ingredients[i]
                if i in recipe.secondary_ingredients:
                    self.grocery_list[i] += recipe.secondary_ingredients[i]

    def print_grocery(self, output_file=sys.stdout):
        print("Grocery List")
        for i in self.grocery_list:
            for t in self.tabular:
                if t["id"] == i:
                    print(t["name"] + ": " + str(self.grocery_list[i]) + t["units"], file=output_file)
                    break
    
    def print_recipes(self, output_file=sys.stdout):
        print("Recipes:", file=output_file)
        for r in self.recipes:
            print(r.name, file=output_file)

def ingredient_score(ingr_table, QR):
    S = 1
    MDU = ingr_table['MDU']
    while (S * MDU < QR):     
        S += 1
    leftover = (S * MDU - QR) * ingr_table['Weight']
    return(leftover)

def instantiate_recipe(record, ingr_table):
    name = record["title"]
    ingredients = []
    for i in record["ingredientsSimplified"].split(","):
        ingredients.append(i.strip())
    table_data = []
    for i in ingredients:
        table_data.append(table_lookup(ingr_table, i))
    r = Recipe(name, ingredients, record["ingredientsUnits"])
    return(r, table_data)

def table_lookup(ingr_table, ingredient):
    for i in ingr_table:
        if (ingredient == i["Ingredient"]):
            return i
    sys.exit("Requested ingredient " + ingredient + " does not exist in ingredient table!")

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

        # we could have a user-improvement feature where they enter the smallest unit they saw at the store for a certain product
