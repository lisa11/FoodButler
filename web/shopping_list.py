# Must be used together with input from generate_menu.py or front end

import json



def build_sub_shopping_dict(day, result, rv_dict, meal_num):
    for k in range(len(result[meal_num][day]["ingredients"])):
        ingredient = result[meal_num][day]["ingredients"][k]
        if ingredient not in rv_dict[day + 1]:
            rv_dict[day + 1][ingredient] = 1
        else:
            rv_dict[day + 1][ingredient] += 1


def generate_shopping_list(days):
    '''
	generate the shopping list after finalizing menu
	result: final_output from backend after finalizing for alternative changes
    output: a list with each element a list of 2 elements -- the 
    ingredient needed and a list of days on which this ingredient is needed
    '''

    with open("final_output.json") as f:
        result = json.load(f)
        breakfast_list = result["breakfast_final_list"]
        lunch_list = result["lunch_list"]
        dinner_list = result["dinner_list"]
        calories_list = result["calories_list"]
        alternative_breakfast_list = result["alternative_breakfast_list"]
        alternative_lunch_list = result["alternative_lunch_list"]
        alternative_dinner_list = result["alternative_dinner_list"]
    result = (breakfast_list, lunch_list, dinner_list, calories_list, alternative_breakfast_list, alternative_lunch_list, alternative_dinner_list)

    week_list = []
    rv_dict = {}
    for day in range(7):
        rv_dict[day + 1] = {}
        for meal in range(3):
            build_sub_shopping_dict(day, result, rv_dict, meal)
    
    for i in range(1,8):
        if i not in days:
            del rv_dict[i]
    
    if len(rv_dict) <= 4:
        return rv_dict, {}
    else:
        day_count = 0
        rv_dict1 = {}
        for day in range(1,8):
            if day in rv_dict:
                day_count += 1
                rv_dict1[day] = rv_dict[day]
                del rv_dict[day]
                if day_count == 4:
                    return (rv_dict1, rv_dict)







