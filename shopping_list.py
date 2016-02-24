# Must be used together with input from generate_menu.py or front end

def generate_shopping_list(result):
	'''
	generate the shopping list after finalizing menu
	result: final_output from backend after finalizing for alternative changes
    output: a list with each element a list of 2 elements -- the 
    ingredient needed and a list of days on which this ingredient is needed
    '''

    breakfast_final_list, lunch_list, dinner_list, calories_list, alternative_breakfast_list, alternative_lunch_list, alternative_dinner_list = result
    rv_dict = {}

    for i in range(7):
        if breakfast_final_list[i]["ingredients"] not in rv_dict:
    	    rv_dict[breakfast_final_list[i]["ingredients"]] = [i + 1]
    	else:
    		rv_dict[breakfast_final_list[i]["ingredients"]].append(i + 1)
    	if lunch_list[i]["ingredients"] not in rv_dict:
    	    rv_dict[lunch_list[i]["ingredients"]] = [i + 1]
    	else:
    		rv_dict[lunch_list[i]["ingredients"]].append(i + 1)
    	if dinner_list[i]["ingredients"] not in rv_dict:
    	    rv_dict[dinner_list[i]["ingredients"]] = [i + 1]
    	else:
    		rv_dict[dinner_list[i]["ingredients"]].append(i + 1)
    
    rv_list = []
    for x in rv_dict:
    	rv_list.append([x, rv_dict[x]])

    return rv_list