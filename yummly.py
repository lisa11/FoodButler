from yummly import Client

# default option values
TIMEOUT = 5.0
RETRIES = 0
YOUR_API_ID = "057fa7e9"
YOUR_API_KEY = "eb5bef37e3d25571eafd42e98ace7ee7"


client = Client(api_id=YOUR_API_ID, api_key=YOUR_API_KEY, timeout=TIMEOUT, retries=RETRIES)

search = client.search('green eggs and ham')
match = search.matches[0]

recipe = client.recipe(match.id)

results = yummly.search('bacon')

print('Total Matches:', results.totalMatchCount)
for match in results.matches:
    print('Recipe ID:', match.id)
    print('Recipe:', match.recipeName)
    print('Rating:', match.rating)
    print('Total Time (mins):', match.totalTimeInSeconds / 60.0)
    print('----------------------------------------------------')

params = {
    'q': 'pork chops',
    'start': 0,
    'maxResult': 40,
    'requirePicutres': True,
    'allowedIngredient[]': ['salt', 'pepper'],
    'excludedIngredient[]': ['cumin', 'paprika'],
    'maxTotalTimeInSeconds': 3600,
    'facetField[]': ['ingredient', 'diet'],
    'flavor.meaty.min': 0.5,
    'flavor.meaty.max': 1,
    'flavor.sweet.min': 0,
    'flavor.sweet.max': 0.5,
    'nutrition.FAT.min': 0,
    'nutrition.FAT.max': 15
}

results = yummly.search(**params)

# return the first 10 results
results = yummly.search('chicken marsala', maxResults=10)

# return 2nd page of results
results = yummly.search('pulled pork', maxResults=10, start=10)

METADATA_KEYS = [
    'ingredient',
    'holiday',
    'diet',
    'allergy',
    'technique',
    'cuisine',
    'course',
    'source',
    'brand',
    'restriction'
]

ingredients = client.metadata('ingredient')
diets = client.metadata('diet')
sources = client.metadata('source')

recipe = yummly.recipe(recipe_id)

print('Recipe ID:', recipe.id)
print('Recipe:', recipe.name)
print('Rating:', recipe.rating)
print('Total Time:', recipe.totalTime)
print('Yields:', recipe.yields)
print('Ingredients:')
for ingred in recipe.ingredientLines:
    print(ingred)
