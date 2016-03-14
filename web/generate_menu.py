# The code in the file is the algorithm to generate the output menu of recipes.
# It is mainly written by ourselves.

import json
import random
from subprocess import call
import re
from Meal import Meal
from Day import Day
from MyExceptions import MyError


# The ingredients we care that should not be repeated within three days
MAJOR_INGREDIENTS = ['steak', 'mustard', 'coriander', 'sprout', 'honey', 'tomato', 'bell', 'chickpea', 'couscous', 'pita', 'companelle', 'leeks', 'beet', 'walnut', 'shrimp', 'sierra', 'meat', 'orange', 'spinach', 'carrot', 'phyllo dough', 'lobster', 'celery', 'noodle', 'frond', 'fettucine', 'cherry', 'lamb', 'chocolate', 'hummus', 'cilantro', 'brownie', 'cookie', 'kiwi', 'cayenne', 'chicken wings', 'nana', 'cumin', 'salad', 'rice', 'eggplant', 'onion', 'avocado', 'khoa', 'podded pea', 'garam masala', 'cabbage', 'ras-el-hanout', 'mint', 'mushroom', 'sausage', 'pancake', 'baguette', 'naan', 'polenta', 'pumpkin', 'lettuce', 'broccoli', 'tagliatelle', 'loaves', 'parsley', 'curry', 'pork', 'cacao', 'linguine', 'cardamom', 'beef', 'loaf', 'apple', 'dough', 'meatball', 'berr', 'pudding', 'lentil', 'fruit', 'peach', 'asparagus', 'arugula', 'marshmallow', 'egg', 'molasses', 'seed', 'popcorn', 'pine nut', 'shetbet', 'cornmeal', 'albacore', 'coconut', 'bulgur', 'sandwich', 'red chilli', 'hamburger', 'oreo', 'thyme', 'tomatoes', 'pistachio', 'spaghetti', 'salmon', 'cucumber', 'corn', 'chicken', 'ditalini', 'pineapple', 'tortilla', 'potato', 'herb', 'strawberr', 'bread', 'pizza', 'fish', 'sauerkraut', 'brioche', 'buns', 'pie', 'sirloin', 'hazelnut', 'cake', 'pecorino', 'mango', 'granola', 'mushroom', 'graviera', 'fettucine', 'wedge', 'macaroni', 'ham', 'almonds', 'soy', 'flax', 'wheat', 'mushrooms', 'korma', 'peanut', 'peas', 'strawberries', 'zucchini', 'cheddar', 'potatoes', 'prosciutto', 'pomegranate', 'nuts', 'tortillas', 'bacon', 'lemon', 'wedges', 'yoghurt', 'almond', 'jasmine', 'apples', 'onions', 'sockeye', 'nut', 'cutlet', 'pistachios', 'rutabaga', 'ribs', 'bananas', 'yogurt', 'vegetables', 'loin', 'noodles', 'scallions', 'breasts', 'mozzarella', 'milk', 'fillet', 'matcha', 'pasta', 'tenderloins', 'oranges', 'sesame', 'shoulder', 'cereal', 'cider', 'turnips', 'tenderloin', 'oyster', 'rib', 'carrots', 'kale', 'cauliflower', 'leg', 'yolks', 'cheese', 'seeds', 'vegetable', 'feta', 'taco', 'oats', 'fillets', 'sausages', 'walnuts', 'sheep', 'thighs', 'blueberries', 'turkey', 'coffee', 'steaks', 'breast', 'beans']
MAX_TRIAL_BEFORE_GOING_TO_ALT = 2
MAX_TRIAL_BEFORE_REPEATING_INGREDIENT = 3
MAX_TRIAL_AFTER_REPEATING_INGREDIENT = 5
MAX_TRIAL_BEFORE_IGNORE_CALORIES = 10 # is it only lower or both?
#the number of days generated failed lower calories limit before discarding the lower limit
BREAKFAST_CALORIES_WEIGHT = 0.4 # 40% of the total calories of the day 
LUNCH_CALORIES_WEIGHT = 0.6
DINNER_CALORIES_WEIGHT = 0.6
# Default calories amount when there is no return of calories amount
DEFAULT_CAL_BREAKFAST = 100
DEFAULT_CAL_MAIN_DISH = 500


def generate_available_recipes(args_from_ui):
    '''
    input: input from front end, a dictionary.
    sample args_from_ui = {"calories_per_day": [50, 500], 
                    "allowedIngredient[]": ["onion", "tomato", "lamb"],
                    "excludedIngredient[]": ["pork", "potato"],
                    "allowedAllergy[]": ["397^Egg-Free"],
                    "allowedDiet[]": ["386^Vegan"],
                    "time": [20, 60],
                    }

    return a dictionary of four lists. Each a list of tuples in which the first
    element is the Recipe object and the second element a list of ingredients
    '''
    
    with open("temp_dict.json", "w") as f:
        f.write(json.dumps(args_from_ui))
    
    call("python2 build_db.py temp_dict.json", shell=True)
    
    with open("recipe_lists.json") as f:
        recipe_lists = json.load(f)
    
    call("rm temp_dict.json", shell=True)
    call("rm recipe_lists.json", shell=True)

    return recipe_lists


def clean_one_recipe_list(recipe_list, major_ingredients, default_cal):
    '''
    Clean one recipe list to generate a list of meal objects and build a list of major ingredients

    Inputs:
        recipe_list: a list of available recipes to clean
        major_ingredients: a val for testing and improving purpose,
            to keep track of what ingredients are included in the 
            trial and we manually add some of the ingredients we
            regard as major to MAJOR_INGREDIENTS 
        default_cal: an integer. DEFAULT_CAL_BREAKFAST for breakfast and DEFAULT_CAL_MAIN_DISH for main dish
    '''
    cleaned_list = []
    for i in range(len(recipe_list)):
        item = recipe_list[i][0] # the list consists of tuples eg. (one recipe dict, a list of ingredients used)
        calories = default_cal 
        for x in item["nutritionEstimates"]:
            if x["attribute"] == "ENERC_KCAL":
                calories = x["value"]
                break
        if item["ingredientLines"][0][0:11] == "Ingredients": 
            ingredient_lines = [item["ingredientLines"][0][12:]] # to get rid of the word "Ingredients" at the start
        else:
            ingredient_lines = list(set(item["ingredientLines"])) # to remove repeated lines
        meal = Meal(item["name"], calories, item["totalTime"], recipe_list[i][1], ingredient_lines,\
                item["images"][0]["hostedLargeUrl"], item["source"]["sourceRecipeUrl"])
        major_ingredients += recipe_list[i][1]
        cleaned_list.append(meal)
    return cleaned_list
    

def clean_recipes(recipe_lists):
    '''
    convert the messy lists from generate_available_recipes to lists of
    Meal objects
    recipe_lists: a dict mapping to four lists 
    '''
    breakfast_alt_list_old = recipe_lists["breakfast_alt_list"]
    breakfast_list_old = recipe_lists["breakfast_list"]
    main_dish_alt_list_old = recipe_lists["main_dish_alt_list"]
    main_dish_list_old = recipe_lists["main_dish_list"]

    major_ingredients = []
    
    if breakfast_alt_list_old != []:
    # use list(set()) to remove repeated recipe in the list returned by API  
        breakfast_alt_list = list(set(clean_one_recipe_list(breakfast_alt_list_old, major_ingredients, DEFAULT_CAL_BREAKFAST)))
    else:
        breakfast_alt_list = []
    
    breakfast_list = list(set(clean_one_recipe_list(breakfast_list_old, major_ingredients, DEFAULT_CAL_BREAKFAST)))
    
    if main_dish_alt_list_old != []:
        main_dish_alt_list = list(set(clean_one_recipe_list(main_dish_alt_list_old, major_ingredients, DEFAULT_CAL_MAIN_DISH)))
    else:
        main_dish_alt_list = []
    
    main_dish_list = list(set(clean_one_recipe_list(main_dish_list_old, major_ingredients, DEFAULT_CAL_MAIN_DISH)))
    
    major_ingredients = list(set(major_ingredients))
    with open("major_ingredients_in_trial.txt", "w") as f:
        print(major_ingredients, file = f)

    print("len of lists:", "breakfast_alt_list", len(breakfast_alt_list), "breakfast_list", len(breakfast_list), \
        "main_dish_alt_list", len(main_dish_alt_list), "main_dish_list", len(main_dish_list))

    return breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list


def pick_recipe(max_trail, recipe_list, max_calories, used_ingredients, used_recipe):
    '''
    Pick a recipe based on the list and parameters given

    max_trail: eg. TRIAL_NUM_BEFORE_GOING_TO_ALT, TRIAL_NUM_BEFORE_REPEATING_INGREDIENT
    recipe_list: eg. breakfast_list
    max_calories: max calories for this meal 
    used_ingredients: a set of ingredients to avoid
    used_recipe: a recipe used for lunch of the same day; to be avoided; might be None

    '''
    chosen_recipe = None
    trial_count = 0
    while (trial_count < max_trail) and (chosen_recipe == None or chosen_recipe == used_recipe):
        print("Individual meal trial", trial_count)
        print(len(recipe_list))
        trial_count += 1
        index = random.randint(0, len(recipe_list) - 1)
        recipe = recipe_list[index]
        if recipe.calories < max_calories and list(used_ingredients & set(recipe.major_ingredients)) == []: 
            used_ingredients.update(set(recipe.major_ingredients))
            chosen_recipe = recipe
    return chosen_recipe 


def set_meal(day, meal_type, main_list, alt_list, used_ingredients, used_recipe=None):
    '''
    Update a Day object with selected recipe for a meal  
    
    day: a Day object
    meal_type: "breakfast", "lunch" or "dinner"
    used_ingredients: a set of used ingredients to avoid
    main_list: a list of recipes with ingredients user has
    alt_list: a list of recipes excluding ingredients that user has
    '''
    if meal_type == "breakfast":
        max_calories = BREAKFAST_CALORIES_WEIGHT * day.upper_calories
    elif meal_type == "lunch":
        max_calories = LUNCH_CALORIES_WEIGHT * day.upper_calories
    else:
        max_calories = DINNER_CALORIES_WEIGHT * day.upper_calories
    
    chosen_recipe = None
    if main_list != []:
        chosen_recipe = pick_recipe(MAX_TRIAL_BEFORE_GOING_TO_ALT, main_list, max_calories, used_ingredients, used_recipe)
        print("choosing from main_list")
        from_alt = False

    if chosen_recipe == None and alt_list != []:
        chosen_recipe = pick_recipe(MAX_TRIAL_BEFORE_REPEATING_INGREDIENT, alt_list, max_calories, used_ingredients, used_recipe)
        print("choosing from alt_list")
        from_alt = True
    
    if chosen_recipe == None:
        # start repeating ingredients, the pick recipe function
        # would only be run once in this scenario
        if main_list != []:
            chosen_recipe = pick_recipe(MAX_TRIAL_AFTER_REPEATING_INGREDIENT, main_list, max_calories, set(), used_recipe) 
            from_alt = False
        else:
            if alt_list != []:
                chosen_recipe = pick_recipe(MAX_TRIAL_AFTER_REPEATING_INGREDIENT, alt_list, max_calories, set(), used_recipe)
                from_alt = True 
            #else:
             #   print("both main_list and alt_list are empty")
              #  raise MyError()
        
    if chosen_recipe == None:
        raise MyError()

    day.insert_meal(chosen_recipe, meal_type)

    return day, used_ingredients, from_alt

    
def update_recipe_lists(day, available_recipes, from_alt):
    '''
    Once a day's menu is confirmed, delete used recipes from the available recipe lists
    
    day: a Day object
    available_recipes: a tuple consisting 4 recipe lists
    from_alt: a list indicating whether each meal is choosen from alt_list, eg. [True, False, True]
    '''
    breakfast_list, breakfast_alt_list, main_dish_list, main_dish_alt_list = available_recipes

    if from_alt[0]:
        breakfast_alt_list.remove(day.breakfast)
    else:
        breakfast_list.remove(day.breakfast)

    if from_alt[1]:
        main_dish_alt_list.remove(day.lunch)
    else:
        main_dish_list.remove(day.lunch)

    if day.lunch != day.dinner:
        if from_alt[2]:
            main_dish_alt_list.remove(day.dinner)
        else:
            main_dish_list.remove(day.dinner)
    return breakfast_list, breakfast_alt_list, main_dish_list, main_dish_alt_list


def generate_Day(breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list, 
                 args_from_ui, Day1 = None, Day2 = None):
    '''
    Day1: the day object for the previous day
    Day2: the day object for the day before yesterday
    The lists must be in clean version!!!
    '''

    # Set a default calories range if none is given
    if "calories_per_day" not in args_from_ui:
        args_from_ui["calories_per_day"] = [1, 5000]

    day = Day(args_from_ui["calories_per_day"]) # This is the initialization for the first time
    total = 0

    # while calories requirement not met 
    while total < MAX_TRIAL_BEFORE_IGNORE_CALORIES and not day.is_qualified():
        print("Total trial run in a day:", total)
        total += 1
        day = Day(args_from_ui["calories_per_day"])
        used_ingredients = set()
        if Day1:
            used_ingredients.update(set(Day1.major_ingredients))
        if Day2:
            used_ingredients.update(set(Day2.major_ingredients))
        # not sure if used_ingredients list will be shared in backend; keep it here for now
        day, used_ingredients, breakfast_from_alt = set_meal(day, "breakfast", breakfast_list, \
                                                            breakfast_alt_list, used_ingredients)
        day, used_ingredients, lunch_from_alt = set_meal(day, "lunch", main_dish_list, \
                                                        main_dish_alt_list, used_ingredients)
        day, used_ingredients, dinner_from_alt = set_meal(day, "dinner", main_dish_list,\
                                                        main_dish_alt_list, used_ingredients, day.lunch)
    
    # at this point meals are already set regardless of whether meeting calories limits
    breakfast_list, breakfast_alt_list, main_dish_list, main_dish_alt_list = \
        update_recipe_lists(day, (breakfast_list, breakfast_alt_list, main_dish_list, main_dish_alt_list), \
        [breakfast_from_alt, lunch_from_alt, dinner_from_alt])
    return day 



def update_output_lists(day, output_lists, day_num, is_alt_list):
    '''
    Update breakfast, lunch, and dinner output lists with a day's menu

    day: a Day object
    output_lists: a tuple consisting of 3 output lists
    day_num: an integer; day of the week
    is_alt_list: a boolean indicating whether the lists are for alternative lists
    '''
    if is_alt_list:
        additional_index = 21
    else:
        additional_index = 0

    breakfast_output_list, lunch_output_list, dinner_output_list = output_lists
    breakfast_output_list.append({"num": day_num + 1 + additional_index, "name": day.breakfast.name, 
        "calories": day.breakfast.calories, "cooking_time": day.breakfast.cooking_time, 
        "ingredients": day.breakfast.full_ingredients, "pic_url": day.breakfast.pic_url, 
        "instruction_url": day.breakfast.instruction_url})
    lunch_output_list.append({"num": day_num + 8 + additional_index, "name": day.lunch.name, 
        "calories": day.lunch.calories, "cooking_time": day.lunch.cooking_time, 
        "ingredients": day.lunch.full_ingredients, "pic_url": day.lunch.pic_url, 
        "instruction_url": day.lunch.instruction_url})
    dinner_output_list.append({"num": day_num + 15 + additional_index, "name": day.dinner.name, 
        "calories": day.dinner.calories, "cooking_time": day.dinner.cooking_time, 
        "ingredients": day.dinner.full_ingredients, "pic_url": day.dinner.pic_url, 
        "instruction_url": day.dinner.instruction_url})
    
    return (breakfast_output_list, lunch_output_list, dinner_output_list)


def generate_final_output(args_from_ui):
    '''
    return breakfast_list, lunch_list, dinner_list, alternative_breakfast_list,
    alternative_lunch_list, alternative_dinner_list, each with 7 items.
    Each item being a dictionary including "name", "calories", "cooking_time",
    ingredients as a list of strings, pic_url as a string, instruction_url
    as a string
    ''' 
    
    if "calories_per_day" in args_from_ui:
        if len(args_from_ui["calories_per_day"]) != 2 or args_from_ui["calories_per_day"][1] >= args_from_ui["calories_per_day"][0]:
            raise MyError(message="invalid calories range (must enter both upper and lower limits for calories per day, with upper limit greater than lower limit)")

    available_recipes = generate_available_recipes(args_from_ui)
    print("successfully got available recipes")
    
    breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list = clean_recipes(available_recipes)
    print("successfully cleaned the recipes")

    day_list = []
    calories_list = []
    breakfast_final_list = []
    lunch_list = []
    dinner_list = []
    alternative_breakfast_list = []
    alternative_lunch_list = []
    alternative_dinner_list = []

    for i in range(7):
        # Check for available lists
        if breakfast_alt_list == [] and breakfast_list == []:
            raise MyError()
        elif main_dish_alt_list == [] and main_dish_list == []:
            raise MyError()
        # Start generating the day
        if i == 0:
            day = generate_Day(breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list, args_from_ui)
            print("Generated day 0")
        elif i == 1:
            day = generate_Day(breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list, args_from_ui, 
                Day1 = day_list[-1])
            print("Generated day 1")
        else:
            day = generate_Day(breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list, args_from_ui, 
                Day1 = day_list[-1], Day2 = day_list[-2])
            print("Generated day", i)
        day_list.append(day)
        breakfast_final_list, lunch_list, dinner_list = update_output_lists(day, 
            (breakfast_final_list, lunch_list, dinner_list), i, False)
        calories_list.append(day.calories)

    for i in range(7):
        # Also need this check for alternative menu
        if breakfast_alt_list == [] and breakfast_list == []:
            raise MyError()
        elif main_dish_alt_list == [] and main_dish_list == []:
            raise MyError()
        day = generate_Day(breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list, args_from_ui)
        print("Generated alternative day", i)
        alternative_breakfast_list, alternative_lunch_list, alternative_dinner_list = update_output_lists(day, 
            (alternative_breakfast_list, alternative_lunch_list, alternative_dinner_list), i, True)

    with open("final_output.txt", "w") as f:
        print(breakfast_final_list, ",", lunch_list, ",", dinner_list, ",", calories_list, ",", 
            alternative_breakfast_list, ",", alternative_lunch_list, ",", alternative_dinner_list, file = f)

    with open("major_ingredients.txt", "w") as f:
        for x in day_list:
            print(x.major_ingredients, file = f)

    with open("final_output.json", "w") as f:
        rv = {}
        rv["breakfast_final_list"] = breakfast_final_list
        rv["lunch_list"] = lunch_list
        rv["dinner_list"] = dinner_list
        rv["calories_list"] = calories_list
        rv["alternative_breakfast_list"] = alternative_breakfast_list
        rv["alternative_lunch_list"] = alternative_lunch_list
        rv["alternative_dinner_list"] = alternative_dinner_list
        f.write(json.dumps(rv))

    return breakfast_final_list, lunch_list, dinner_list, calories_list, alternative_breakfast_list, alternative_lunch_list, alternative_dinner_list






    