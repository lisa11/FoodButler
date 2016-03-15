# Meal class to represent each meal
# This file is entirely original
import re

MAJOR_INGREDIENTS = ['steak', 'mustard', 'coriander', 'sprout', 'honey', 'tomato', 'bell', 'chickpea', 'couscous', 'pita', 'companelle', 'leeks', 'beet', 'walnut', 'shrimp', 'sierra', 'meat', 'orange', 'spinach', 'carrot', 'phyllo dough', 'lobster', 'celery', 'noodle', 'frond', 'fettucine', 'cherry', 'lamb', 'chocolate', 'hummus', 'cilantro', 'brownie', 'cookie', 'kiwi', 'cayenne', 'chicken wings', 'nana', 'cumin', 'salad', 'rice', 'eggplant', 'onion', 'avocado', 'khoa', 'podded pea', 'garam masala', 'cabbage', 'ras-el-hanout', 'mint', 'mushroom', 'sausage', 'pancake', 'baguette', 'naan', 'polenta', 'pumpkin', 'lettuce', 'broccoli', 'tagliatelle', 'loaves', 'parsley', 'curry', 'pork', 'cacao', 'linguine', 'cardamom', 'beef', 'loaf', 'apple', 'dough', 'meatball', 'berr', 'pudding', 'lentil', 'fruit', 'peach', 'asparagus', 'arugula', 'marshmallow', 'egg', 'molasses', 'seed', 'popcorn', 'pine nut', 'shetbet', 'cornmeal', 'albacore', 'coconut', 'bulgur', 'sandwich', 'red chilli', 'hamburger', 'oreo', 'thyme', 'tomatoes', 'pistachio', 'spaghetti', 'salmon', 'cucumber', 'corn', 'chicken', 'ditalini', 'pineapple', 'tortilla', 'potato', 'herb', 'strawberr', 'bread', 'pizza', 'fish', 'sauerkraut', 'brioche', 'buns', 'pie', 'sirloin', 'hazelnut', 'cake', 'pecorino', 'mango', 'granola', 'mushroom', 'graviera', 'fettucine', 'wedge', 'macaroni', 'ham', 'almonds', 'soy', 'flax', 'wheat', 'mushrooms', 'korma', 'peanut', 'peas', 'strawberries', 'zucchini', 'cheddar', 'potatoes', 'prosciutto', 'pomegranate', 'nuts', 'tortillas', 'bacon', 'lemon', 'wedges', 'yoghurt', 'almond', 'jasmine', 'apples', 'onions', 'sockeye', 'nut', 'cutlet', 'pistachios', 'rutabaga', 'ribs', 'bananas', 'yogurt', 'vegetables', 'loin', 'noodles', 'scallions', 'breasts', 'mozzarella', 'milk', 'fillet', 'matcha', 'pasta', 'tenderloins', 'oranges', 'sesame', 'shoulder', 'cereal', 'cider', 'turnips', 'tenderloin', 'oyster', 'rib', 'carrots', 'kale', 'cauliflower', 'leg', 'yolks', 'cheese', 'seeds', 'vegetable', 'feta', 'taco', 'oats', 'fillets', 'sausages', 'walnuts', 'sheep', 'thighs', 'blueberries', 'turkey', 'coffee', 'steaks', 'breast', 'beans']


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
