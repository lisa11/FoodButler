import random
import sqlite3


class Day:

    def __init__(self, price, calories, num_of_servings):
        '''
        price: maximum price per day (from max price per week divided by 6)
        calaries: a list with lower and upper limit for calories per day
        num_of_servings: number of people serving for the day
        '''

        self.breakfast = []
        self.lunch = []
        self.dinner = []
        self.price = price
        self.lower_calories = calories[0]
        self.upper_calories = calories[1]
        self.num_of_servings = num_of_servings


def generate_available_recipes(input):
    '''
    input: input from front end, a dictionary.
    sample_input = {“calories”: [50, 500], 
                    “ingredients_have”: [“onion”, “tomato”, “lamb”],
                    “ingredients_avoid”: {"ingredients"“dietary_res”: “vegetarian”},
                    “price”: 200,
                    “time”: [20, 60],
                    }
    '''

    breakfast_list = 

    return breakfast_list, lunch_list, dinner_list


def generate_Day():



def generate_menu():

    menu = []
    for i in range(7):
        menu.append(generate_Day())

    return menu