import random
from subprocess import call


# The ingredients we care that should not be repeated within three days
MAJOR_INGREDIENTS = ["beef", "lamb", "chicken", "lobster", "shrimp", "pork",
                     "steak", "tomato", "onion", "potato", "broccoli",
                     "cabbage", "lettuce", "leeks"]
TRIAL_NUM_BEFORE_GOING_TO_ALT = 3
TRIL_NUM_BEFORE_REPEATING_INGREDIENT = 10


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
            if ingredient in MAJOR_INGREDIENTS:
                self.major_ingredients.append(ingredient)
        self.pic_url = pic_url
        self.instruction_url = instruction_url
        self.full_ingredients = full_ingredients


class Day(object):

    def __init__(self, price, calories, num_of_servings):
        '''
        price: max price for the day
        calories: lower and upper limits of calories for the day (a list)
        time: max time for breakfast and lunch/dinner (a list)
        num_of_servings: number of people serving for the day
        '''

        self.breakfast = None
        self.lunch = None
        self.dinner = None
        self.price = price
        self.major_ingredients = []
        self.calories = 0
        self.breakfast_time = time[0]
        self.main_meal_time = time[1]
        self.lower_calories = calories[0]
        self.upper_calories = calories[1]
        self.num_of_servings = num_of_servings


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
                    "num_of_servings": 1
                    }
    Breakfast accounts for roughly 20 percent price and 30 percent calories
    Lunch accounts for roughly 40 percent price and 40 percent calories
    Dinner accounts for roughly 40 percent price and 30 percent calories

    return four lists. Each a list of tuples in which the first
    element is the Recipe object and the second element a list of ingredients
    '''
    
    with open("temp_dict.txt", "w") as f:
        print(args_from_ui, file = f)

    breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list = call("python2 build_db.py temp_dict.txt", shell=True)
    return breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list


def clean_recipes(available_recipes):
    '''
    convert the messy lists from generate_available_recipes to lists of
    Meal objects
    '''

    ### work not done
    breakfast_alt_list_old, breakfast_list_old, main_dish_alt_list_old, main_dish_list_old = available_recipes
    breakfast_alt_list = []
    for item in breakfast_alt_list_old:
        meal = Meal(item["name"], 0, list(filter(y["attribute"] == "FAT_KCAL" for y in x))y["value"] in item["nutritionEstimates"] if y["attribute"] == "FAT_KCAL")
        breakfast_alt_list.append(x)
    breakfast_list = []
    main_dish_alt_list = []
    main_dish_list = []
    return breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list


def generate_Day(clean_recipes, args_from_ui, Day1 = None, Day2 = None):
    '''
    Day1: the day object for the previous day
    Day2: the day object for the day before yesterday
    '''

    breakfast_alt_list, breakfast_list, main_dish_alt_list, main_dish_list = clean_recipes
    day = Day(args_from_ui["price"], args_from_ui["calories per day"], args_from_ui["servings"])
    major_ingredients = []
    if Day1:
        major_ingredients += Day1.major_ingredients
    if Day2:
        major_ingredients += Day2.major_ingredients
    # how to adjust to the major ingredients to avoid...
    # need to come up a way
    # Urgent...
    if breakfast_preferred_list:
        num = random.randint(0, len(breakfast_list) - 1)

    day.insert_meal(breakfast_list[random.randint(0, len(breakfast_list) - 1)], "breakfast")
    day.insert_meal(lunch_list[random.randint(0, len(lunch_list) - 1)], "lunch")
    day.insert_meal(dinner_list[random.randint(0, len(dinner_list) - 1)], "dinner")

    return day


def generate_final_output(args_from_ui):
    '''
    return breakfast_list, lunch_list, dinner_list, alternative_breakfast_list,
    alternative_main_meal_list, each with 7 items.
    Each item being a dictionary including "name", "calories", "cooking time",
    ingredients as a list of strings, pic_url as a string, instruction_url
    as a string
    ''' 
    
    available_recipes = generate_available_recipes(args_from_ui)
    clean_recipes = clean_recipes(available_recipes)

    day_list = []
    calories_list = []
    breakfast_list = []
    lunch_list = []
    dinner_list = []

    for i in range(7):
        if i == 0:
            day = generate_Day(clean_recipes, args_from_ui)
        elif i == 1:
            day = generate_Day(clean_recipes, args_from_ui, Day1 = day_list[-1])
        else:
            day = generate_Day(clean_recipes, args_from_ui, Day1 = day_list[-1], Day2 = day_list[-2])
        day_list.append(day)
        breakfast_list.append({"name": day.breakfast.name, "calories": day.breakfast.calories, "cooking time": day.breakfast.cooking_time, "ingredients": day.breakfast.full_ingredients, "pic url" day.breakfast.pic_url, "instruction url": day.breakfast.instruction_url})
        lunch_list.append({"name": day.lunch.name, "calories": day.lunch.calories, "cooking time": day.lunch.cooking_time, "ingredients": day.lunch.full_ingredients, "pic url" day.lunch.pic_url, "instruction url": day.lunch.instruction_url})
        dinner_list.append({"name": day.dinner.name, "calories": day.dinner.calories, "cooking time": day.dinner.cooking_time, "ingredients": day.dinner.full_ingredients, "pic url" day.dinner.pic_url, "instruction url": day.dinner.instruction_url})
        calories_list.append(day.calories)

    for i in range(7):
        day = generate_Day(clean_recipes, args_from_ui)
        alternative_breakfast_list.append({"name": day.breakfast.name, "calories": day.breakfast.calories, "cooking time": day.breakfast.cooking_time, "ingredients": day.breakfast.full_ingredients, "pic url" day.breakfast.pic_url, "instruction url": day.breakfast.instruction_url})
        alternative_lunch_list.append({"name": day.lunch.name, "calories": day.lunch.calories, "cooking time": day.lunch.cooking_time, "ingredients": day.lunch.full_ingredients, "pic url" day.lunch.pic_url, "instruction url": day.lunch.instruction_url})
        alternative_dinner_list.append({"name": day.dinner.name, "calories": day.dinner.calories, "cooking time": day.dinner.cooking_time, "ingredients": day.dinner.full_ingredients, "pic url" day.dinner.pic_url, "instruction url": day.dinner.instruction_url})

    return breakfast_list, lunch_list, dinner_list, calories_list, alternative_breakfast_list, alternative_lunch_list, alternative_dinner_list