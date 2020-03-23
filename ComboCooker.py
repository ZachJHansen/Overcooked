from bitarray import bitarray

# Globals
COOKWARE_LENGTH = 100

class Recipe:
    def __init__(self, name, ingredients, **kwargs):                # Not all recipes will have information such as complexity and calorie count
        self.name = name                                            # Hence, None initialization or empty arrays
        self.primary_ingredients = ingredients[0]
        self.secondary_ingredients = ingredients[1]
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

    #def update_tags(self, allergens, restrictions, complexity, time, calories):
    #    for 

    def update_tags(self, **kwargs):                                # 
        for key, value in kwargs.items():
            setattr(self, key, value)

    #def update_leftover_score(self):

    #def update_buddies(self):

if __name__=="__main__":
    ingredients = tuple((["rice", "beans"], ["red pepper"]))
    additional_info = {
        "restrictions": ["vegan", "gluten free"],
        "time": 45,
        "complexity": "hard"
    }
    r1 = Recipe("Spaghetti-os", ingredients)
    print(r1.name)
    r1.update_tags(**additional_info)
    print(r1.link)
    print(r1.restrictions)