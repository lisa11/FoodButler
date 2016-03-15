# Day class to represent each day with three meals and some properties
# This file is entirely original

class Day(object):

    def __init__(self, calories):
        '''
        Create a class object containing the recipes and their basic 
        information for a day.
        Input:
            calories: lower and upper limits of calories for the day (a list)
        '''
        self._breakfast = None
        self._lunch = None
        self._dinner = None
        self._major_ingredients = []
        self._calories = 0
        self._lower_calories = calories[0]
        self._upper_calories = calories[1]


    @property
    def breakfast(self):
        return self._breakfast

    @property
    def lunch(self):        
        return self._lunch

    @property
    def dinner(self):
        return self._dinner

    @property
    def major_ingredients(self):
        return self._major_ingredients

    @property
    def calories(self):
        return self._calories

    @property
    def upper_calories(self):
        return self._upper_calories

    @property
    def lower_calories(self):
        return self._lower_calories


    def is_qualified(self):
        '''
        See if the day is qualified under calories limit and with all meals chosen
        '''

        if (self.breakfast != None) and (self.lunch != None) and (self.dinner != None)\
            and self.calories >= self._lower_calories \
            and self.calories <= self._upper_calories:
            return True
        else:
            return False


    def insert_meal(self, meal, position):
        '''
        Insert a Meal to a specified position of a Day
        meal: a Meal object
        position: "breakfast", "lunch", or "dinner"
        '''

        if position == "breakfast":
            self._breakfast = meal
        if position == "lunch":
            self._lunch = meal
        if position == "dinner":
            self._dinner = meal
        self._calories += meal.calories
        self._major_ingredients += meal.major_ingredients
        self._major_ingredients = list(set(self._major_ingredients))
        