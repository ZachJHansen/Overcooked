import json
from Recipe import *
from jsmin import jsmin                                     # pip install jsmin
import requests           
import multiprocessing as mp 
import random               

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
def update_new_buddies(path, K):
    ingredients = set()                                           # Union of all primary ingredients required by new recipes
    with open("tables.jsonc") as tables:
        with open(path) as recipe_file:
            new_recipes = json.loads(jsmin(recipe_file.read()))
            prim_ingr_table = json.loads(jsmin(tables.read()))["primary_ingredients"]
    for recipe in new_recipes:
        for ingr in recipe["primary_ingredients"].keys():
            ingredients.add(ingr)
    #old_recipes = read_from_db("", ingredients)                         # Only compare recipes that share primary ingredients with new recipes
    #recipes = old_recipes + new_recipes                         # Shallow copies, no memory issue, all new + fetched recipes will be updated
    recipes = new_recipes
    for recipe in recipes:
        r, table_data = instantiate_recipe(recipe, prim_ingr_table)
        n_minus_1 = [r for r in recipes if r != recipe]
        r.update_buddies(n_minus_1, prim_ingr_table, K)
        print("Buddies -", recipe["rID"])
        print(r.buddies)
        recipe["buddy_recipes"] = r.buddies
    open("output.jsonc", "w").write(json.dumps(recipes))                  # Overwrite file with updated recipes from entire DB + new recipes

def read_from_db(URL, PARAMS):
    # fetch all recipes from db that contain at least one of the specified ingredients
    r = requests.get(url = URL, params = PARAMS) 
    sc = r.status_code
    if (sc == 200):                              # OK
        docs = r.json()
        return(docs)
    elif (sc >= 300 and sc < 400):
        print("Redirection code %s.".format(sc))
    elif (sc >= 400 and sc < 500):
        print("Client Error %s".format(sc))
    elif (sc >= 500):
        print("Server Error %s.".format(sc))
    else:
        print("Unknown error %s".format(sc))
    return None

# Find the N smallest members of the array
# Returns an array of ints representing the reciped IDs of the best candidates:
# Best candidates are recipes who possess a buddy recipe that has one of the N smallest leftover scores
# Symmetric arrays: candidate ids, buddies, and scores
def find_min_buddies(start, end, array, candidate_ids, candidate_buddies, candidate_scores, lock, N):
    # Find the N recipes with the lowest buddy score
    maxes = [(0,0,float("inf")) for i in range(N)]
    curr_max = float("inf")
    max_index = 0
    for doc in array[start:end]:
        buddies = doc["buddy_recipes"]
        for b in buddies:
            score = buddies[b]
            if score < curr_max:
                del maxes[max_index]
                maxes.append(tuple((doc["rID"], int(b), score)))
                curr_max = score
                max_index = N-1
                for indx in range(len(maxes)-1):
                    s = maxes[indx][2]
                    if s > curr_max:
                        curr_max = s
                        max_index = indx
    # Acquire the mutex lock to update the shared array
    lock.acquire()
    candidates = []
    for i in range(N):
        candidates.append(tuple((candidate_ids[i], candidate_buddies[i], candidate_scores[i])))
    maxes += candidates
    tupleware = minimize_tuple_array(maxes, 3, N)
    for i in range(N):
        t = tupleware[i]
        candidate_ids[i] = t[0]
        candidate_buddies[i] = t[1]
        candidate_scores[i] = t[2]
    lock.release()

# Expects an array of JSON from the DB representing candidates for the meal plan
# Return an array of N recipe ids
def select_meal_plan_recipes(results, N):
    # Maintain a list of N recipes with the lowest buddy score
    candidate_ids = mp.RawArray('i', range(N))
    candidate_buddies = mp.RawArray('i', range(N))
    candidate_scores = mp.RawArray('i', range(999999, 999999+N))
    procs = mp.cpu_count()
    chunk_size = len(results)//procs
    start = 0
    end = chunk_size
    lock = mp.Lock()
    running = []
    # Process the recipes in parallel using all CPUs
    for i in range(procs):
        p = mp.Process(target=find_min_buddies, args=(start, end, results, candidate_ids, candidate_buddies, candidate_scores, lock, N))
        running.append(p)
        p.start()
        start = end
        end += chunk_size
    p = mp.Process(target=find_min_buddies, args=(start, len(results), results, candidate_ids, candidate_buddies, candidate_scores, lock, N))
    #p = mp.Process(target=find_min_buddies, args=(0, len(results), results, candidate_ids, candidate_buddies, candidate_scores, lock, N))
    running.append(p)
    p.start()
    # Join terminated procs to parent
    for r in running:
        r.join()
    # Multiprocessing ctype arrays dont like min or index methods or deletion. and i like those
    nice_ids = [candidate_ids[i] for i in range(N)]
    nice_buddies = [candidate_buddies[i] for i in range(N)]
    nice_scores = [candidate_scores[i] for i in range(N)]            
    # Remove reciprocals - (id1, id2), (id2, id1)
    for i, rID in enumerate(nice_ids):
        bID, score = nice_buddies[i], nice_scores[i]
       # print("Recipe:", rID, "| Buddy Recipe:", bID, "| Score:", score)
        while i < len(nice_ids)-1: 
            i += 1
            if (nice_ids[i] == bID and nice_buddies[i] == rID):
                del nice_ids[i]
                del nice_buddies[i]
                del nice_scores[i]
    # Select minimum
    total_lo_score = 0
    final = []       
    for i in range(N//2):
        m_index = nice_scores.index(min(nice_scores))
        final.append(nice_ids[m_index])
        final.append(nice_buddies[m_index])
        total_lo_score += nice_scores[m_index]
        del nice_ids[m_index]
        del nice_buddies[m_index]
        del nice_scores[m_index]
    if (N%2 == 1):                                                          # Match N//2 recipes, add a minimal remainder
        capstones = find_min_leftover(results, procs, chunk_size, N)
        for i, c in enumerate(capstones):
            if c[0] in final:
                del capstones[i]
        minimal_recipe = minimize_tuple_array(capstones, 2, 1)[0]
        final.append(minimal_recipe[0])
        total_lo_score += minimal_recipe[1]
    print("Total Leftover Score:", total_lo_score)    
    return(final)                                                           # Return array of rIDs 

# Find the N//2 + 1 recipes with the lowest personal leftover scores (we only need 1, but at most N//2 might overlap with paired recipes)
# Although it would probably be faster to identify the lowest leftover score for each array segment while processing the best buddies
def find_min_leftover(results, num_procs, chunk_size, N):
    q = mp.Queue()
    running = []
    start = 0
    end = chunk_size
    for i in range(num_procs):
        p = mp.Process(target=min_leftover, args=(start, end, results, q))
        running.append(p)
        p.start()
        start = end
        end += chunk_size
    p = mp.Process(target=min_leftover, args=(start, end, results, q))
    running.append(p)
    p.start()
    for r in running:
        r.join()
    array = []
    while not q.empty():
        array.append(q.get(block=True, timeout=1))
    return(minimize_tuple_array(array, 2, (N//2)+1))

def min_leftover(start, end, array, q):
    curr_min_score = float('inf')
    curr_min_id = None
    for doc in array[start:end]:
        score = doc["leftover_score"]
        if score < curr_min_score:
            curr_min_score = score
            curr_min_id = doc["rID"]
    t = tuple((curr_min_id, curr_min_score))
    q.put(t)

# Return the N tuples of size X with the minimum (X-1)th values (tuple[X-1])
def minimize_tuple_array(array, X, N):
    if (X == 2):
        results = [(0, float("inf")) for i in range(N)]
    elif (X == 3):
        results = [(0, 0, float("inf")) for i in range(N)]
    X -= 1
    curr_max = results[0][X]
    max_index = 0
    for a in array:
        score = a[X]
        if (score < curr_max):
            del results[max_index]
            results.append(a)
            curr_max = score
            max_index = N-1
            for indx in range(N-1):
                s = results[indx][X]
                if s > curr_max:
                    curr_max = s
                    max_index = indx
    return(results)


# Make a meal plan with N recipes
def generate_meal_plan(results, N):
    try:
        if (len(results) < N):
            print("Recipe finder returned fewer results than requested number of recipes in meal plan")
            raise ValueError 
        with open("tables.jsonc") as tables:
            prim_ingr_table = json.loads(jsmin(tables.read()))["primary_ingredients"]
            rids = select_meal_plan_recipes(results, N)
            print(rids)
            recipes = [r for r in results if r["rID"] in rids]
            mp = MealPlan(recipes, prim_ingr_table)
        return(mp)
    except:
        return None


# Generate a random meal plan, calculate total leftover score
# Needs testing
def random_meal_plan(results, prim_ingr_table, N):
    recipes = random.sample(results, N)
    ingredients = []
    for r in recipes:
        ingredients += r["primary_ingredients"]
    combined_ingredients = set(ingredients)
    table_data = []
    for pi in combined_ingredients:
        table_data.append(prim_ingr_table[pi])
        leftovers = []
    for ingr_table in table_data:
        _id = ingr_table['id']
        QR = 0
        for r in recipes:
            if _id in r["primary_ingredients"]:
                QR += r["primary_ingredients"][_id]
        leftovers.append(ingredient_score(ingr_table, QR))
    score = sum(leftovers)
    print("Random Meal Plan Recipes:")
    print([r["rID"] for r in recipes])
    print("Total score for random meal plan:", score)


if __name__=="__main__":
    update_lo_scores("output.jsonc")
    update_new_buddies("output.jsonc", 3)
    #old = read_from_db("http://127.0.0.1:5000/", {'main_ingredient':'chicken'})
    #print(old)
    #insertion_wrapper(1, "ingredients", ["code", "quantity"], ["ch", 10])
#c.execute("INSERT INTO nametable " + snames + ";")
    with open("tables.jsonc") as tables:
        with open("output.jsonc") as recipe_file:
            new_recipes = json.loads(jsmin(recipe_file.read()))
            prim_ingr_table = json.loads(jsmin(tables.read()))["primary_ingredients"]
            mp = generate_meal_plan(new_recipes, 3)
            #random_meal_plan(new_recipes, prim_ingr_table, 3)
            mp.print_recipes()
            mp.print_grocery()
