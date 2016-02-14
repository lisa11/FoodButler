from yummly import Client

# default option values
TIMEOUT = 5.0
RETRIES = 0
YOUR_API_ID = "057fa7e9"
YOUR_API_KEY = "eb5bef37e3d25571eafd42e98ace7ee7"


client = Client(api_id=YOUR_API_ID, api_key=YOUR_API_KEY, timeout=TIMEOUT, retries=RETRIES)
#search = Client.search("green eggs and ham")
params = ["beef", "pork", "chicken", "turkey", "fish"]
for param in params:
    results = Client.search(param)
    for result in results.matches:
        recipe_id = result["id"]
        recipe = Client.recipe(recipe_id)
        recipe_url = recipe["sourceRecipeUrl"]





