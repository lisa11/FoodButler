import json

search_values = []
for x in l:
    search_values.append(x["searchValue"])

with open("search_values.txt", "w") as f:
    print(search_values, file = f)

with open("search_values.json", "w") as f:
    f.write(json.dumps(search_values))