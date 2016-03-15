# Meal class to represent each meal
# This file is entirely original

class Meal(object):

    def __init__(self, name, calories, time, ingredients, full_ingredients, pic_url, instruction_url):
        '''
        Generate a class object containing basic information of a meal.
        Inputs:
            name: string, name of the dish
            calories: the amount of calories this meal contains
            time: a string, the cooking time required for this meal
            ingredients: a brief list of ingredient without amount obtained from search recipe query,
                used for summarizing the major ingredients this meal uses
            full_ingredients: a list of full ingredient lines with amount associated with each ingredient,
                to be displayed in the final output to django
            pic_url: string, the url of the dish's picture
            instruction_url: string, the url to recipe webpage
        '''
        self.name = name
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

    def __str__(self):
        '''
        This methond helps with printing and testing.
        '''
        rv = {"name": self.name, "calories": self.calories, \
            "cooking_time": self.cooking_time, \
            "full_ingredients": self.full_ingredients, \
            "major_ingredients": self.major_ingredients, \
            "pic_url": self.pic_url, \
            "instruction_url": self.instruction_url}
        return str(rv)
