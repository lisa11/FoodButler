# This file contains functions to get recipes from yummly API and update our database
# Modified from https://pypi.python.org/pypi/yummly/0.3.3

from yummly import Client
import json
import sys

# default option values
TIMEOUT = 5.0
RETRIES = 0
YOUR_API_ID = "057fa7e9"
YOUR_API_KEY = "eb5bef37e3d25571eafd42e98ace7ee7"


client = Client(api_id=YOUR_API_ID, api_key=YOUR_API_KEY, timeout=TIMEOUT, retries=RETRIES)


def find_recipes(client, param, recipe_db, course, max_time):
    '''
    Finds recipes that match the parameters provided; updates the database. 

    Inputs:
        client: a client object
        param: a dict of parameters
        recipe_db: a dict mapping recipe ids to recipes
        course: a list containing a string indicating the meal type, "Break and Brunch" 
                or "Main Dishes"
        max_time: an integer

    Returns:
        a list of tuples each containing a recipe object and ingredients 
        used in this recipe; updates the recipe_db dict in the process
    '''
    recipe_list = []
    param["requirePictures"] = True
    param["allowedCourse[]"] = course
    if max_time != None:
        param["maxTotalTimeInSeconds"] = max_time

    recipes = client.search("", **param)
    for match in recipes.matches:
        ingredients = match["ingredients"]
        recipe_id = match["id"]
        if recipe_id in recipe_db:
            recipe_list.append((recipe_db[recipe_id], ingredients)) 
        else:
            recipe = client.recipe(recipe_id)
            recipe_list.append((recipe, ingredients))
            recipe_db[recipe_id] = recipe

    return recipe_list

def go(param):
    '''
    Generates 4 lists that meets the parameters: breakfast_alt_list, breakfast_list,
        main_dish_alt_list, main_dish_list

    Inputs:
        param: a dict of parameters. 
        e.g:{"allowedIngredient[]": ["onion", "tomato", "lamb"],
            "excludedIngredient[]": ["pork", "potato"],
            "allowedAllergy[]": ["397^Egg-Free"],
            "allowedDiet[]": ["386^Vegan"],
            "time": [20, 60]}

    Returns:
        writes a json file containing a dict of the 4 lists 
    '''
    with open("recipe_db.json") as f:
        recipe_db = json.load(f)
    
    rv = {}
    if "maxTotalTimeInSeconds" in param:
        breakfast_max_time, main_dish_max_time = param["maxTotalTimeInSeconds"]
        del param["maxTotalTimeInSeconds"]
    else:
        breakfast_max_time = None
        main_dish_max_time = None

    rv["breakfast_list"] = find_recipes(client, param, recipe_db, \
        ["course^course-Breakfast and Brunch"], breakfast_max_time)  
    rv["main_dish_list"] = find_recipes(client, param, recipe_db, \
        ["course^course-Main Dishes"], main_dish_max_time)
    
    # generates alternative lists that does not contain the ingredient user
    # already has to avoid having the same ingredient for every meal in 7 days
    if param.has_key("allowedIngredient[]"):
        if param.has_key("excludedIngredient[]"):
            param["excludedIngredient[]"].extend(param["allowedIngredient[]"])
        else:
            param["excludedIngredient[]"] = param["allowedIngredient[]"]
        del param["allowedIngredient[]"]
        rv["breakfast_alt_list"] = find_recipes(client, param, recipe_db, \
            ["course^course-Breakfast and Brunch"], breakfast_max_time)  
        rv["main_dish_alt_list"] = find_recipes(client, param, recipe_db, \
            ["course^course-Main Dishes"], main_dish_max_time)
    else: 
        rv["breakfast_alt_list"] = []
        rv["main_dish_alt_list"] = []

    with open("recipe_db.json", "w") as f:  
        f.write(json.dumps(recipe_db))

    with open("recipe_lists.json", "w") as f:
        f.write(json.dumps(rv))



if __name__=="__main__":
    num_args = len(sys.argv)

    if num_args != 2:
        print("usage: python2 " + sys.argv[0] + "<dictionary json file name>")
        sys.exit(0)

    with open(sys.argv[1]) as f:
        param = json.load(f)
    if "calories_per_day" in param:
        del param["calories_per_day"]
    go(param)
