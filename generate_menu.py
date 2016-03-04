import json
import random
from subprocess import call
import re


# The ingredients we care that should not be repeated within three days
MAJOR_INGREDIENTS = ["beef", "lamb", "chicken", "lobster", "shrimp", "pork",
                     "steak", "tomato", "onion", "potato", "broccoli",
                     "cabbage", "lettuce", "leeks", "chicken wings",
                     "eggplant"]
TRIAL_NUM_BEFORE_GOING_TO_ALT = 3
TRIL_NUM_BEFORE_REPEATING_INGREDIENT = 10
FINAL_TOLERANCE = 20 # the number of days generated failed lower calories limit before discarding the lower limit
BREAKFAST_CALORIES_WEIGHT = 0.4
LUNCH_CALORIES_WEIGHT = 0.5
DINNER_CALORIES_WEIGHT = 0.5



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


def clean_recipes(available_recipes):
    '''
    convert the messy lists from generate_available_recipes to lists of
    Meal objects
    '''

    breakfast_alt_list_old, breakfast_list_old, main_dish_alt_list_old, main_dish_list_old = available_recipes
    major_ingredients = []

    breakfast_alt_list = []
    if breakfast_alt_list_old != []:
        for i in range(len(breakfast_alt_list_old)):
            item = breakfast_alt_list_old[i][0]
            for x in item["nutritionEstimates"]:
                if x["attribute"] == "ENERC_KCAL":
                    calories = x["value"]
                    break
            if item["ingredientLines"][0][0:11] == "Ingredients": # some repeated messy ingredientLines needs to be cleaned this way
                ingredient_lines = [item["ingredientLines"][0][12:]]
            else:
                ingredient_lines = list(set(item["ingredientLines"]))
            meal = Meal(item["name"], 0, calories, item["totalTime"], breakfast_alt_list_old[i][1], ingredient_lines, item["images"][0]["hostedLargeUrl"], item["source"]["sourceRecipeUrl"])
            major_ingredients += breakfast_alt_list_old[i][1]
            breakfast_alt_list.append(meal)
    
    breakfast_list = []
    for i in range(len(breakfast_list_old)):
        item = breakfast_list_old[i][0]
        for x in item["nutritionEstimates"]:
            if x["attribute"] == "FAT_KCAL":
                calories = x["value"]
                break
        if item["ingredientLines"][0][0:11] == "Ingredients":
            ingredient_lines = [item["ingredientLines"][0][12:]]
        else:
            ingredient_lines = list(set(item["ingredientLines"]))
        meal = Meal(item["name"], 0, calories, item["totalTime"], breakfast_list_old[i][1], ingredient_lines, item["images"][0]["hostedLargeUrl"], item["source"]["sourceRecipeUrl"])
        major_ingredients += breakfast_list_old[i][1]
        breakfast_list.append(meal)
    
    main_dish_alt_list = []
    if main_dish_alt_list_old != []:
        for i in range(len(main_dish_alt_list_old)):
            item = main_dish_alt_list_old[i][0]
            for x in item["nutritionEstimates"]:
                if x["attribute"] == "FAT_KCAL":
                    calories = x["value"]
                    break
            if item["ingredientLines"][0][0:11] == "Ingredients":
                ingredient_lines = [item["ingredientLines"][0][12:]]
            else:
                ingredient_lines = list(set(item["ingredientLines"]))
            meal = Meal(item["name"], 0, calories, item["totalTime"], main_dish_alt_list_old[i][1], ingredient_lines, item["images"][0]["hostedLargeUrl"], item["source"]["sourceRecipeUrl"])
            major_ingredients += main_dish_alt_list_old[i][1]
            main_dish_alt_list.append(meal)
    
    main_dish_list = []
    for i in range(len(main_dish_list_old)):
        item = main_dish_list_old[i][0]
        for x in item["nutritionEstimates"]:
            if x["attribute"] == "FAT_KCAL":
                calories = x["value"]
                break
        if item["ingredientLines"][0][0:11] == "Ingredients":
            ingredient_lines = [item["ingredientLines"][0][12:]]
        else:
            ingredient_lines = list(set(item["ingredientLines"]))
        meal = Meal(item["name"], 0, calories, item["totalTime"], main_dish_alt_list_old[i][1], ingredient_lines, item["images"][0]["hostedLargeUrl"], item["source"]["sourceRecipeUrl"])
        major_ingredients += main_dish_list_old[i][1]
        main_dish_list.append(meal)
    
    major_ingredients = list(set(major_ingredients))
    with open("major_ingredients_in_trial.txt", "w") as f:
        print(major_ingredients, file = f)

    return breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list


def generate_Day(breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list, args_from_ui, Day1 = None, Day2 = None):
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
    while total < FINAL_TOLERANCE and day.calories < day.lower_calories or day.calories > day.upper_calories:

        total += 1
        day = Day(args_from_ui["price"], args_from_ui["calories_per_day"], args_from_ui["servings"])
        major_ingredients = []
        if Day1:
            major_ingredients += Day1.major_ingredients
        if Day2:
            major_ingredients += Day2.major_ingredients
        major_ingredients = list(set(major_ingredients))
        from_alt = [None, None, None]
        
        # Choose breakfast
        t1 = 0
        while day.breakfast == None and t1 < TRIAL_NUM_BEFORE_GOING_TO_ALT:
            t1 += 1
            num1 = random.randint(0, len(breakfast_list) - 1)
            if breakfast_list[num1].calories < BREAKFAST_CALORIES_WEIGHT * day.upper_calories and [x for x in major_ingredients if x in breakfast_list[num1].major_ingredients] == []:
                day.insert_meal(breakfast_list[num1], "breakfast")
                major_ingredients += breakfast_list[num1].major_ingredients
                from_alt[0] = 0
        if day.breakfast == None and breakfast_alt_list != []:
            while day.breakfast == None and t1 < TRIL_NUM_BEFORE_REPEATING_INGREDIENT:
                num1 = random.randint(0, len(breakfast_alt_list) - 1)
                if breakfast_alt_list[num1].calories < BREAKFAST_CALORIES_WEIGHT * day.upper_calories and [x for x in major_ingredients if x in breakfast_list[num1].major_ingredients] == []:
                    day.insert_meal(breakfast_alt_list[num1], "breakfast")
                    major_ingredients += breakfast_list[num1].major_ingredients
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
            while day.lunch == None and t2 < TRIL_NUM_BEFORE_REPEATING_INGREDIENT:
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
            while day.dinner == None and t3 < TRIL_NUM_BEFORE_REPEATING_INGREDIENT:
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

    return day


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
        elif i == 1:
            day = generate_Day(breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list, args_from_ui, Day1 = day_list[-1])
        else:
            day = generate_Day(breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list, args_from_ui, Day1 = day_list[-1], Day2 = day_list[-2])
        day_list.append(day)
        breakfast_final_list.append({"num": i + 1, "name": day.breakfast.name, "calories": day.breakfast.calories, "cooking_time": day.breakfast.cooking_time, "ingredients": day.breakfast.full_ingredients, "pic_url": day.breakfast.pic_url, "instruction_url": day.breakfast.instruction_url})
        lunch_list.append({"num": i + 8, "name": day.lunch.name, "calories": day.lunch.calories, "cooking_time": day.lunch.cooking_time, "ingredients": day.lunch.full_ingredients, "pic_url": day.lunch.pic_url, "instruction_url": day.lunch.instruction_url})
        dinner_list.append({"num": i + 15, "name": day.dinner.name, "calories": day.dinner.calories, "cooking_time": day.dinner.cooking_time, "ingredients": day.dinner.full_ingredients, "pic_url": day.dinner.pic_url, "instruction_url": day.dinner.instruction_url})
        calories_list.append(day.calories)

    for i in range(7):
        day = generate_Day(breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list, args_from_ui)
        alternative_breakfast_list.append({"num": i + 22, "name": day.breakfast.name, "calories": day.breakfast.calories, "cooking_time": day.breakfast.cooking_time, "ingredients": day.breakfast.full_ingredients, "pic_url": day.breakfast.pic_url, "instruction_url": day.breakfast.instruction_url})
        alternative_lunch_list.append({"num": i + 29, "name": day.lunch.name, "calories": day.lunch.calories, "cooking_time": day.lunch.cooking_time, "ingredients": day.lunch.full_ingredients, "pic_url": day.lunch.pic_url, "instruction_url": day.lunch.instruction_url})
        alternative_dinner_list.append({"num": i + 36, "name": day.dinner.name, "calories": day.dinner.calories, "cooking_time": day.dinner.cooking_time, "ingredients": day.dinner.full_ingredients, "pic_url": day.dinner.pic_url, "instruction_url": day.dinner.instruction_url})

    with open("final_output.txt", "w") as f:
        print(breakfast_final_list, ",", lunch_list, ",", dinner_list, ",", calories_list, ",", alternative_breakfast_list, ",", alternative_lunch_list, ",", alternative_dinner_list, file = f)

    with open("major_ingredients.txt", "w") as f:
        for x in day_list:
            print(x.major_ingredients, file = f)

    return breakfast_final_list, lunch_list, dinner_list, calories_list, alternative_breakfast_list, alternative_lunch_list, alternative_dinner_list