from yummly import Client
import json
# default option values
TIMEOUT = 5.0
RETRIES = 0
YOUR_API_ID = "057fa7e9"
YOUR_API_KEY = "eb5bef37e3d25571eafd42e98ace7ee7"


client = Client(api_id=YOUR_API_ID, api_key=YOUR_API_KEY, timeout=TIMEOUT, retries=RETRIES)
#search = Client.search("green eggs and ham")

def find_recipes(client, param, recipe_db, course, max_time):
    recipe_list = []
    param["requirePictures"] = True
    param["allowedCourse[]"] = [course]
    param["maxTotalTimeInSeconds"] = max_time
    recipes = client.search(param)
    for match in recipes.matches:
        ingredients = match["ingredients"]
        recipe_id = match["id"]
        if recipe_id in recipe_db:
            recipe_list.append((recipe_db[recipe_id], ingredients))
        else:
            recipe = client.recipe(recipe_id)
            recipe_list.append((recipe, ingredients))
            recipe_db[recipe_id] = recipe

def go(param):
    with open("recipe_db.json") as f:
        recipe_db = json.load(f)

    breakfast_maxtime, maindish_maxtime = param["maxTotalTimeInSeconds"]

    breakfast_list = find_recipes(client, param, recipe_db, "Breakfast and Brunch", breakfast_maxtime)  
    main_dish_list = find_recipes(client, param, recipe_db, "Main Dishes", maindish_maxtime)

    if "allowedIngredient[]" in param:
        if "excludedIngredient[]" in param:
            param["excludedIngredient[]"].extend(param["allowedIngredient"])
        else:
            param["excludedIngredient"] = param["allowedIngredient"]
        del param["allowedIngredient"]
        breakfast_alt_list = find_recipes(client, param, recipe_db, "Breakfast and Brunch", breakfast_maxtime)  
        main_dish_alt_list = find_recipes(client, param, recipe_db, "Main Dishes", maindish_maxtime)
    else: 
        breakfast_alt_list = []
        main_dish_alt_list = []

    with open("recipe_db.json", "w") as f:  
        f.write(json.dumps(recipe_db))

    return(breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list)



if __name__ == "__main__":
    go(sys.argv)




































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





