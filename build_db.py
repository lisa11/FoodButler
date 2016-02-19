from yummly import Client
import csv
# default option values
TIMEOUT = 5.0
RETRIES = 0
YOUR_API_ID = "057fa7e9"
YOUR_API_KEY = "eb5bef37e3d25571eafd42e98ace7ee7"


client = Client(api_id=YOUR_API_ID, api_key=YOUR_API_KEY, timeout=TIMEOUT, retries=RETRIES)
#search = Client.search("green eggs and ham")
params = ["beef", "pork", "chicken", "turkey", "fish"]
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





