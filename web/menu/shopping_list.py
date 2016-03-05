# Must be used together with input from generate_menu.py or front end


def build_sub_shopping_dict(day, result, rv_dict, meal_num):
    for k in range(len(result[meal_num][i]["ingredients"])):
        ingredient = result[meal_num][i]["ingredients"][k]
        if ingredient not in rv_dict[i]:
            rv_dict[i][ingredient] = 1
        else:
            rv_dict[i][ingredient] += 1


def generate_shopping_list(days):
    '''
	generate the shopping list after finalizing menu
	result: final_output from backend after finalizing for alternative changes
    output: a list with each element a list of 2 elements -- the 
    ingredient needed and a list of days on which this ingredient is needed
    '''

    rv_dict = {}
    rv_list = []
    for day in range(7):
        for meal in range(3):
            build_sub_shopping_dict(day, result, rv_dict, meal)
    for day in range(7):
        sub_shopping_list = []
        for ingredient in rv_dict[day]:
            sub_shopping_list.append((ingredient, rv_dict[day][ingredient]))
        rv_list.append(sub_shopping_list)
    return rv_list







    '''

        if i not in rv_dict:
            rv_dict[i] = {}
        for j in range(len(result[0][i]["ingredients"])):
            if result[0][i]["ingredients"][j] not in rv_dict:
    	        rv_dict[result[0][i]["ingredients"][j]] = [i + 1]
            else:
                rv_dict[result[0][i]["ingredients"][j]].append(i + 1)
        for j in range(len(result[1][i]["ingredients"])):
            if result[1][i]["ingredients"][j] not in rv_dict:
                rv_dict[result[1][i]["ingredients"][j]] = [i + 1]
            else:
                rv_dict[result[1][i]["ingredients"][j]].append(i + 1)
        for j in range(len(result[2][i]["ingredients"])):
            if result[2][i]["ingredients"][j] not in rv_dict:
                rv_dict[result[2][i]["ingredients"][j]] = [i + 1]
            else:
                rv_dict[result[2][i]["ingredients"][j]].append(i + 1)
    
    rv_list = []
    for k in range(7)
    for x in rv_dict:
    	rv_list.append([x, rv_dict[x]])

    with open("shopping_list_sample.txt", "w") as f:
        print(rv_list, file = f)

    return rv_list
    '''