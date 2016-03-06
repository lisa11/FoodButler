import json
import random
from subprocess import call
import re


# The ingredients we care that should not be repeated within three days
MAJOR_INGREDIENTS = ['steak', 'mustard', 'coriander', 'sprout', 'honey', 'tomato', 'bell', 'chickpea', 'couscous', 'pita', 'companelle', 'leeks', 'beet', 'walnut', 'shrimp', 'sierra', 'meat', 'orange', 'spinach', 'carrot', 'phyllo dough', 'lobster', 'celery', 'noodle', 'frond', 'fettucine', 'cherry', 'lamb', 'chocolate', 'hummus', 'cilantro', 'brownie', 'cookie', 'kiwi', 'cayenne', 'chicken wings', 'nana', 'cumin', 'salad', 'rice', 'eggplant', 'onion', 'avocado', 'khoa', 'podded pea', 'garam masala', 'cabbage', 'ras-el-hanout', 'mint', 'mushroom', 'sausage', 'pancake', 'baguette', 'naan', 'polenta', 'pumpkin', 'lettuce', 'broccoli', 'tagliatelle', 'loaves', 'parsley', 'curry', 'pork', 'cacao', 'linguine', 'cardamom', 'beef', 'loaf', 'apple', 'dough', 'meatball', 'berr', 'pudding', 'lentil', 'fruit', 'peach', 'asparagus', 'arugula', 'marshmallow', 'egg', 'molasses', 'seed', 'popcorn', 'pine nut', 'shetbet', 'cornmeal', 'albacore', 'coconut', 'bulgur', 'sandwich', 'red chilli', 'hamburger', 'oreo', 'thyme', 'tomatoes', 'pistachio', 'spaghetti', 'salmon', 'cucumber', 'corn', 'chicken', 'ditalini', 'pineapple', 'tortilla', 'potato', 'herb', 'strawberr', 'bread', 'pizza', 'fish', 'sauerkraut', 'brioche', 'buns', 'pie', 'sirloin', 'hazelnut', 'cake', 'pecorino', 'mango', 'granola', 'mushroom', 'graviera', 'fettucine', 'wedge']
MAX_TRIAL_BEFORE_GOING_TO_ALT = 2
MAX_TRIAL_BEFORE_REPEATING_INGREDIENT = 3
MAX_TRIAL_BEFORE_IGNORE_CALORIES = 10 # is it only lower or both?
#the number of days generated failed lower calories limit before discarding the lower limit
BREAKFAST_CALORIES_WEIGHT = 0.3 # 40% of the total calories of the day 
LUNCH_CALORIES_WEIGHT = 0.4
DINNER_CALORIES_WEIGHT = 0.3


class Meal(object):

    def __init__(self, name, price, calories, time, ingredients, full_ingredients, pic_url, instruction_url):

        self.name = name
        self.price = price
        self.calories = calories
        self.cooking_time = time
        self.ingredients = []
        self.major_ingredients = []
        for ingredient in ingredients:
            self.ingredients.append(ingredient)
            for word in re.findall("[A-Za-z0-9]+", ingredient):
                if word in MAJOR_INGREDIENTS:
                    self.major_ingredients.append(word)
        self.pic_url = pic_url
        self.instruction_url = instruction_url
        self.full_ingredients = full_ingredients


class Day(object):

    def __init__(self, price, calories, servings):
        '''
        price: max price for the day
        calories: lower and upper limits of calories for the day (a list)
        time: max time for breakfast and lunch/dinner (a list)
        servings: number of people serving for the day
        '''

        self.breakfast = None
        self.lunch = None
        self.dinner = None
        self.price = price
        self.major_ingredients = []
        self.calories = 0
        # self.breakfast_time = time[0]
        # self.main_meal_time = time[1]
        self.lower_calories = calories[0]
        self.upper_calories = calories[1]
        self.servings = servings


    def insert_meal(self, meal, position):
        '''
        meal: a Meal object (or a dictionary actually...)
        position: "breakfast", "lunch", or "dinner"
        '''

        if position == "breakfast":
            self.breakfast = meal
        if position == "lunch":
            self.lunch = meal
        if position == "dinner":
            self.dinner = meal
        self.price += meal.price
        self.calories += meal.calories
        self.major_ingredients += meal.major_ingredients
        self.major_ingredients = list(set(self.major_ingredients))


def generate_available_recipes(args_from_ui):
    '''
    input: input from front end, a dictionary.
    sample args_from_ui = {"calories": [50, 500], 
                    "ingredients_already_have": ["onion", "tomato", "lamb"],
                    "ingredients_avoid": ["pork", "potato"],
                    "allergy": "egg",
                    "diet": "vegetarian",
                    "price": 200,
                    "time": [20, 60],
                    "servings": 1
                    }

    return four lists. Each a list of tuples in which the first
    element is the Recipe object and the second element a list of ingredients
    '''
    
    with open("temp_dict.json", "w") as f:
        f.write(json.dumps(args_from_ui))
    
    call("python2 build_db.py temp_dict.json", shell=True)
    
    with open("recipe_lists.json") as f:
        recipe_lists = json.load(f)

    return recipe_lists["breakfast_alt_list"], recipe_lists["breakfast_list"],\
    recipe_lists["main_dish_alt_list"], recipe_lists["main_dish_list"]


def clean_one_recipe_list(recipe_list, major_ingredients):
    '''
    Clean one recipe list to generate a list of meal objects and build a list of major ingredients
    '''
    cleaned_list = []
    for i in range(len(recipe_list)):
        item = recipe_list[i][0] # the list consists of tuples eg. (one recipe dict, a list of ingredients used)
        for x in item["nutritionEstimates"]:
            calories = 100
            if x["attribute"] == "ENERC_KCAL":
                calories = x["value"]
                break
            if item["ingredientLines"][0][0:11] == "Ingredients": 
                ingredient_lines = [item["ingredientLines"][0][12:]] # to get rid of the word "Ingredients" at the start
            else:
                ingredient_lines = list(set(item["ingredientLines"])) # to remove repeated lines
            meal = Meal(item["name"], 0, calories, item["totalTime"], recipe_list[i][1], ingredient_lines,
                   item["images"][0]["hostedLargeUrl"], item["source"]["sourceRecipeUrl"])
            major_ingredients += recipe_list[i][1]
            cleaned_list.append(meal)
    return cleaned_list
    


def clean_recipes(available_recipes):
    '''
    convert the messy lists from generate_available_recipes to lists of
    Meal objects
    '''

    breakfast_alt_list_old, breakfast_list_old, main_dish_alt_list_old, main_dish_list_old = available_recipes
    major_ingredients = []
    
    if breakfast_alt_list_old != []: # assuming major_ingredients list will be changed in backend, no need to return 
        breakfast_alt_list = clean_one_recipe_list(breakfast_alt_list_old, major_ingredients)
    else:
        breakfast_alt_list = []
    
    breakfast_list = clean_one_recipe_list(breakfast_list_old, major_ingredients)
    
    if main_dish_alt_list_old != []:
        main_dish_alt_list = clean_one_recipe_list(main_dish_alt_list_old, major_ingredients)
    else:
        main_dish_alt_list = []
    
    main_dish_list = clean_one_recipe_list(main_dish_list_old, major_ingredients)
    
    major_ingredients = list(set(major_ingredients))
    with open("major_ingredients_in_trial.txt", "w") as f:
        print(major_ingredients, file = f)

    return breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list


def pick_recipe(max_trail, recipe_list, max_calories, used_ingredients, used_recipe):
    '''
    Pick a recipe based on the list and parameters given

    max_trail: eg. TRIAL_NUM_BEFORE_GOING_TO_ALT, TRIAL_NUM_BEFORE_REPEATING_INGREDIENT
    recipe_list: eg. breakfast_time
    max_calories: max calories for this meal 
    used_ingredients: a set of ingredients to avoid
    used_recipe: a recipe used for lunch of the same day; to be avoided; might be None

    '''
    chosen_recipe = None
    trial_count = 0
    while trial_count < max_trail and (chosen_recipe == None or chosen_recipe == used_recipe):
        print("Individual meal trial", trial_count)
        trial_count += 1
        index = random.randint(0, len(recipe_list) - 1)
        recipe = recipe_list[index]
        if recipe.calories < max_calories and list(used_ingredients & set(recipe.major_ingredients)) == []: 
            used_ingredients.update(set(recipe.major_ingredients))
            chosen_recipe = recipe
    return chosen_recipe #, used_ingredients


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

    chosen_recipe = pick_recipe(MAX_TRIAL_BEFORE_GOING_TO_ALT, main_list, max_calories, used_ingredients, used_recipe)
    from_alt = False

    if chosen_recipe == None and alt_list != []:
        chosen_recipe = pick_recipe(MAX_TRIAL_BEFORE_REPEATING_INGREDIENT, alt_list, max_calories, used_ingredients, used_recipe)
        from_alt = True
    
    if chosen_recipe == None: # start repeating ingredients
        # 1 is magical number 
        chosen_recipe = pick_recipe(1, main_list, max_calories, set(), used_recipe) 
        from_alt = False
    
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

    if from_alt[2]:
        main_dish_alt_list.remove(day.dinner)
    else:
        main_dish_list.remove(day.dinner)
    #return breakfast_list, breakfast_alt_list, main_dish_list, main_dish_alt_list



def generate_Day(breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list, 
                 args_from_ui, Day1 = None, Day2 = None):
    '''
    Day1: the day object for the previous day
    Day2: the day object for the day before yesterday
    The lists must be in clean version!!!
    '''

    if "price" not in args_from_ui:
        args_from_ui["price"] = 0
    if "calories_per_day" not in args_from_ui:
        args_from_ui["calories_per_day"] = [0, 5000]
    if "servings" not in args_from_ui:
        args_from_ui["servings"] = 1

    day = Day(args_from_ui["price"], args_from_ui["calories_per_day"], args_from_ui["servings"])
    total = 0

    # while calories requirement not met 
    while total < MAX_TRIAL_BEFORE_IGNORE_CALORIES and (day.calories < day.lower_calories or day.calories > day.upper_calories):
        print("Total trial run in a day", total)
        total += 1
        day = Day(args_from_ui["price"], args_from_ui["calories_per_day"], args_from_ui["servings"])
        used_ingredients = set()
        if Day1:
            used_ingredients.update(set(Day1.major_ingredients))
        if Day2:
            used_ingredients.update(set(Day2.major_ingredients))
        # not sure if used_ingredients list will be shared in backend; keep it here for now
        day, used_ingredients, breakfast_from_alt = set_meal(day, "breakfast", breakfast_list, 
                                                            breakfast_alt_list, used_ingredients)
        day, used_ingredients, lunch_from_alt = set_meal(day, "lunch", main_dish_list, 
                                                        main_dish_alt_list, used_ingredients)
        day, used_ingredients, dinner_from_alt = set_meal(day, "dinner", main_dish_list,
                                                        main_dish_alt_list, used_ingredients, day.lunch)
    
    update_recipe_lists(day, (breakfast_list, breakfast_alt_list, main_dish_list, main_dish_alt_list),
        [breakfast_from_alt, lunch_from_alt, dinner_from_alt])
    return day 

                
        # Choose breakfast
'''        t1 = 0
        while day.breakfast == None and t1 < TRIAL_NUM_BEFORE_GOING_TO_ALT:
            t1 += 1
            num1 = random.randint(0, len(breakfast_list) - 1)
            if breakfast_list[num1].calories < BREAKFAST_CALORIES_WEIGHT * day.upper_calories \
            and [x for x in major_ingredients if x in breakfast_list[num1].major_ingredients] == []:
                day.insert_meal(breakfast_list[num1], "breakfast")
                major_ingredients += breakfast_list[num1].major_ingredients
                from_alt[0] = 0
        if day.breakfast == None and breakfast_alt_list != []:
            while day.breakfast == None and t1 < TRIAL_NUM_BEFORE_REPEATING_INGREDIENT:
                num1 = random.randint(0, len(breakfast_alt_list) - 1)
                if breakfast_alt_list[num1].calories < BREAKFAST_CALORIES_WEIGHT * day.upper_calories \
                and [x for x in major_ingredients if x in breakfast_alt_list[num1].major_ingredients] == []:
                    day.insert_meal(breakfast_alt_list[num1], "breakfast")
                    major_ingredients += breakfast_alt_list[num1].major_ingredients
                    from_alt[0] = 1
        if day.breakfast == None:
            num1 = random.randint(0, len(breakfast_list) - 1)
            day.insert_meal(breakfast_list[num1], "breakfast")
            major_ingredients = list(set(major_ingredients) & set(breakfast_list[num1].major_ingredients))
            from_alt[0] = 0

        # Choose Lunch
        t2 = 0
        while day.lunch == None and t2 < TRIAL_NUM_BEFORE_GOING_TO_ALT:
            t2 += 1
            num2 = random.randint(0, len(main_dish_list) - 1)
            if main_dish_list[num2].calories < LUNCH_CALORIES_WEIGHT * day.upper_calories and [x for x in major_ingredients if x in main_dish_list[num2].major_ingredients] == []:
                day.insert_meal(main_dish_list[num2], "lunch")
                major_ingredients += main_dish_list[num2].major_ingredients
                from_alt[1] = 0
        if day.lunch == None and main_dish_alt_list != []:
            while day.lunch == None and t2 < TRIAL_NUM_BEFORE_REPEATING_INGREDIENT:
                num2 = random.randint(0, len(main_dish_alt_list) - 1)
                if main_dish_alt_list[num2].calories < LUNCH_CALORIES_WEIGHT * day.upper_calories and [x for x in major_ingredients if x in main_dish_alt_list[num2].major_ingredients] == []:
                    day.insert_meal(main_dish_alt_list[num2], "lunch")
                    major_ingredients += main_dish_list[num2].major_ingredients
                    from_alt[1] = 1
        if day.lunch == None:
            num2 = random.randint(0, len(main_dish_list) - 1)
            day.insert_meal(main_dish_list[num1], "lunch")
            major_ingredients = list(set(major_ingredients) & set(main_dish_list[num2].major_ingredients))
            from_alt[1] = 0

        # Choose Dinner
        t3 = 0
        while day.dinner == None and t3 < TRIAL_NUM_BEFORE_GOING_TO_ALT:
            t3 += 1
            num3 = random.randint(0, len(main_dish_list) - 1)
            if num3 != num2 and main_dish_list[num2].calories < DINNER_CALORIES_WEIGHT * day.upper_calories and [x for x in major_ingredients if x in main_dish_list[num2].major_ingredients] == []:
                day.insert_meal(main_dish_list[num3], "dinner")
                major_ingredients += main_dish_list[num3].major_ingredients
                from_alt[2] = 0
        if day.dinner == None and main_dish_alt_list != []:
            while day.dinner == None and t3 < TRIAL_NUM_BEFORE_REPEATING_INGREDIENT:
                num3 = random.randint(0, len(main_dish_alt_list) - 1)
                if num3 != num2 and main_dish_alt_list[num3].calories < DINNER_CALORIES_WEIGHT * day.upper_calories and [x for x in major_ingredients if x in main_dish_alt_list[num2].major_ingredients] == []:
                    day.insert_meal(main_dish_alt_list[num3], "dinner")
                    major_ingredients += main_dish_list[num3].major_ingredients
                    from_alt[2] = 1
        if day.lunch == None:
            num3 = random.randint(0, len(main_dish_list) - 1)
            day.insert_meal(main_dish_list[num1], "dinner")
            major_ingredients = list(set(major_ingredients) & set(main_dish_list[num3].major_ingredients))
            from_alt[2] = 0
    
    # Delete the selected dishes
    if from_alt[0] == 0:
        del breakfast_list[num1]
    else:
        del breakfast_alt_list[num1]

    if from_alt[1] == 0 and from_alt[2] == 0:
        if num2 < num3:
            del main_dish_list[num3]
            del main_dish_list[num2]
        else:
            del main_dish_list[num2]
            del main_dish_list[num3]
    elif from_alt[1] == 1 and from_alt[2] == 1:
        if num2 < num3:
            del main_dish_alt_list[num3]
            del main_dish_alt_list[num2]
        else:
            del main_dish_alt_list[num2]
            del main_dish_alt_list[num3]
    elif from_alt[1] == 1 and from_alt[2] == 0:
        del main_dish_alt_list[num2]
        del main_dish_list[num3]
    elif from_alt[1] == 0 and from_alt[2] == 1:
        del main_dish_list[num2]
        del main_dish_alt_list[num3]

    return day''' # need to return list?

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
    
    available_recipes = generate_available_recipes(args_from_ui)
    print("successfully got available recipes")
    with open("available_recipes.txt", "w") as f:
        print(available_recipes, file = f)
    breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list = clean_recipes(available_recipes)
    print("successfully cleaned the recipes")
    with open("cleaned_recipes.txt", "w") as f:
        print(breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list, file = f)

    day_list = []
    calories_list = []
    breakfast_final_list = []
    lunch_list = []
    dinner_list = []
    alternative_breakfast_list = []
    alternative_lunch_list = []
    alternative_dinner_list = []

    for i in range(7):
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
        day = generate_Day(breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list, args_from_ui)
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