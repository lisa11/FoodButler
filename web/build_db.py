from yummly import Client
import json
import sys

# default option values
TIMEOUT = 5.0
RETRIES = 0
YOUR_API_ID = "057fa7e9"
YOUR_API_KEY = "eb5bef37e3d25571eafd42e98ace7ee7"


client = Client(api_id=YOUR_API_ID, api_key=YOUR_API_KEY, timeout=TIMEOUT, retries=RETRIES)
#search = client.search("green eggs and ham")

def find_recipes(client, param, recipe_db, course, max_time):
    '''
    Finds recipes that match the parameters provided; update the database. 

    Inputs:
        client: a client object
        param: a dict of parameters
        recipe_db: a dict mapping recipe ids to recipes
        course: a list containing a string indicating the meal, "Break and Brunch" or "Main Dishes"
        max_time: an integer

    Returns:
        a list of recipes ids (strings) that meets the parameters; updates the recipe_db dict\
        in the process
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
            recipe_list.append((recipe_db[recipe_id], ingredients)) # can simply update the dict
        else:
            recipe = client.recipe(recipe_id)
            recipe_list.append((recipe, ingredients))
            recipe_db[recipe_id] = recipe

    return recipe_list

def go(param):
    '''
    Generates 4 lists that meets the parameters

    Inputs:
        param: a dict of parameters. e.g:
                                       {"allowedIngredient[]": ["onion", "tomato", "lamb"],
                                        "excludedIngredient[]": ["pork", "potato"],
                                        "allowedAllergy[]": ["egg"],
                                        "allowedDiet[]": ["vegetarian"],
                                        "time": [20, 60]}

    Returns:
        writes a json file containing a dict of 4 lists: breakfast_alt_list, breakfast_list, \
        main_dish_alt_list, main_dish_list
    '''
    with open("recipe_db.json") as f:
        recipe_db = json.load(f)
    
    rv = {}
    if "time" in param:
        breakfast_max_time, main_dish_max_time = param["time"]
        del param["time"]
        breakfast_max_time = breakfast_max_time * 60
        main_dish_max_time = main_dish_max_time * 60
    else:
        breakfast_max_time = None
        main_dish_max_time = None

    rv["breakfast_list"] = find_recipes(client, param, recipe_db, \
        ["course^course-Breakfast and Brunch"], breakfast_max_time)  
    rv["main_dish_list"] = find_recipes(client, param, recipe_db, \
        ["course^course-Main Dishes"], main_dish_max_time)


    if param.has_key("allowedIngredient[]"):
        if param.has_key("excludedIngredient[]"):
            param["excludedIngredient[]"].extend(param["allowedIngredient[]"])
        else:
            param["excludedIngredient[]"] = param["allowedIngredient[]"]
        del param["allowedIngredient[]"]
        rv["breakfast_alt_list"] = find_recipes(client, param, recipe_db, 
            ["course^course-Breakfast and Brunch"], breakfast_max_time)  
        rv["main_dish_alt_list"] = find_recipes(client, param, recipe_db, 
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
    if "price" in param:
        del param["price"]
    if "servings" in param:
        del param["servings"]
    if "calories_per_day" in param:
        del param["calories_per_day"]
    go(param)











'''
with open("recipe_csv.csv", "w") as f:   # may change the file name to "meat_dish_csv.csv"
    for param in params:
        results = client.search(param)
        for result in results.matches:
            recipe_id = result["id"]
            recipe = client.recipe(recipe_id)
            recipe_name = recipe["name"]
            recipe_num_serve = recipe["yield"]  # need to figure out the difference between this and the attribute "number of serving"
            recipe_total_time = recipe["totalTime"]  # notice there is also an attribute called total time in seconds
            recipe_url = recipe["sourceRecipeUrl"]
            recipe_ingredient = recipe["ingredientLines"]  # this is a list 
            recipe_nutrition = recipe["nutritionEstimates"] # do we need this? note this is a list of dicts.
            recipe_image = recipe["image"][0]
            recipe_rating = str(recipe["rating"])
            recipe_row = ",".join([recipe_id, recipe_name, recipe_url, recipe_image, recipe_num_serve, recipe_total_time,
                            recipe_rating, recipe_nutrition, recipe_ingredient])
            print(recipe_row, file = f)
'''




