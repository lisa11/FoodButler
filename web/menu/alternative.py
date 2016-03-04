# functions to call when users specify the alternative dishes and the original
# dishes they want to discard from front end
import random


def update_menu(result, discard_list, selected_list):
	'''
	result: the final_output from generate_menu.py
	discard_list: a list of meal index (from 1 to 21) user would like to discard
	selected_list: a list of meal index (from 1 to 21) user would like to add
	               to the main menu from the alternative lists
	NOTE: discard_list and selected_list must be of the same length
	'''

    assert len(discard_list) == len(selected_list)
    breakfast_final_list, lunch_list, dinner_list, calories_list, alternative_breakfast_list, alternative_lunch_list, alternative_dinner_list = result
    main_list = breakfast_final_list + lunch_list + dinner_list + alternative_breakfast_list + alternative_lunch_list + alternative_dinner_list
    random.shuffle(selected_list) # to make it more exciting :D
    for i in range(len(selected_list)):
        dish_to_discard = main_list[discard_list[i]]
        dish_selected = alternative_list[selected_list[i]]
        main_list[discard_list[i]] = dish_selected
        main_list[selected_list[i]] = dish_to_discard

    breakfast_final_list = main_list[0:7]
    lunch_list = main_list[7:14]
    dinner_list = main_list[14:21]
    alternative_breakfast_list = main_list[21:28]
    alternative_lunch_list = main_list[28:35]
    alternative_dinner_list = main_list[35:42]
    new_calories_list = []
    for i in range(7):
    	new_calories_list.append(breakfast_final_list[i]["calories"] + lunch_list[i]["calories"] + dinner_list[i]["calories"])

    return breakfast_final_list, lunch_list, dinner_list, new_calories_list, alternative_breakfast_list, alternative_lunch_list, alternative_dinner_list