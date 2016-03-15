# FoodButler
CMSC122 Project
Let's Go!

Before you try our application, please run:
1) sudo pip install yummly
to pick up the python2 yummly library.
2) sudo pip3 install apiclient
to get some short cuts
3) sudo pip3 install oauth2client
to enable OAuth
4) sudo pip install --upgrade pip google-api-python-client
to pick up google API library


Before runing generate_menu.py, please pull the updated recipe_db.json which is our database. Everytime the function generate_menu.py is run, please push the updated recipe_db.json.

Maximum time in the search form only refers to the preparation time. It might take a significant longer time with cooking time added in the calculation, which is the result displayed in the menu tables.

Some calories amount are unreasonable from the information the api returns. We have no way to deal with that.