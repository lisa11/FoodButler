# Must be used together with input from generate_menu.py or front end

def generate_shopping_list(result):
    '''
	generate the shopping list after finalizing menu
	result: final_output from backend after finalizing for alternative changes
    output: a list with each element a list of 2 elements -- the 
    ingredient needed and a list of days on which this ingredient is needed
    '''

    rv_dict = {}

    for i in range(7):
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
    for x in rv_dict:
    	rv_list.append([x, rv_dict[x]])

    with open("shopping_list_sample.txt", "w") as f:
        print(rv_list, file = f)

    return rv_list