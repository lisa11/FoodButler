import random
import sqlite3


# The ingredients we care that should not be repeated within three days
MAJOR_INGREDIENTS = ["beef", "lamb", "chicken", "lobster", "shrimp", "pork",
                     "steak", "tomato", "onion", "potato", "broccoli",
                     "cabbage", "lettuce"]


class Meal(object):

    def __init__(self, price, calories, time, ingredients):

        self.price = 0
        self.calories = 0
        self.time = 0
        self.ingredients = []


class Day(object):

    def __init__(self, price, calories, time, num_of_servings):
        '''
        price: max price for the day
        calories: lower and upper limits of calories for the day (a list)
        time: max time for breakfast and lunch/dinner (a list)
        num_of_servings: number of people serving for the day
        '''

        self.breakfast = Meal(0.2 * price, 0.3 * calories, )
        self.lunch = []
        self.dinner = []
        self.price = price
        self.major_ingredients = []
        self.calories = 0
        self.time = time
        self.lower_calories = calories[0]
        self.upper_calories = calories[1]
        self.num_of_servings = num_of_servings


def generate_available_recipes(args_from_ui):
    '''
    input: input from front end, a dictionary.
    sample args_from_ui = {"calories": [50, 500], 
                    "ingredients_have": ["onion", "tomato", "lamb"],
                    "ingredients_avoid": {"ingredients": ["pork", "potato"], "dietary_res": "vegetarian"},
                    "price": 200,
                    "time": [20, 60],
                    "num_of_servings": 1
                    }
    Breakfast accounts for roughly 20 percent price and 30 percent calories
    Lunch accounts for roughly 40 percent price and 40 percent calories
    Dinner accounts for roughly 40 percent price and 30 percent calories
    '''

    breakfast_list = 

    return breakfast_list, lunch_list, dinner_list


def generate_Day(args_from_ui, Day1 = None, Day2 = None):
    '''
    Day1: the day object for the previous day
    Day2: the day object for the day before yesterday
    '''

    breakfast_list, lunch_list, dinner_list = generate_available_recipes(args_from_ui)
    day = Day(args_from_ui["price"], args_from_ui["calories"], args_from_ui["time"], args_from_ui["num_of_servings"])
    ingredients_avoid = []
    if Day1:
        ingredients_avoid += Day1.major_ingredients
    if Day2:
        ingredients_avoid += Day1.major_ingredients
    # how to adjust to the major ingredients to avoid...
    # need to come up a way
    # Urgent...
    day.breakfast = breakfast_list[random.randint(0, len(breakfast_list) - 1)]
    day.lunch = lunch_list[random.randint(0, len(lunch_list) - 1)]
    day.dinner = dinner_list[random.randint(0, len(dinner_list) - 1)]


def generate_final_output(args_from_ui):
    
    menu = []
    calories_list = []
    day_list = []

    for i in range(7):
        if i == 0:
            day = generate_Day(args_from_ui)
        elif i == 1:
            day = generate_Day(args_from_ui, Day1 = day_list[-1])
        else:
            day = generate_Day(args_from_ui, Day1 = day_list[-1], Day2 = day_list[-2])
        day_list.append(day)
        menu += [day.breakfast, day.lunch, day.dinner]
        calories_list += day.calories

    return menu, calories_list