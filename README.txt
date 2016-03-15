# FoodButler
CMSC122 Project
Let's Go!

Before you try our application, please run:
1) $ sudo pip install yummly
   to pick up the python2 yummly library.
2) $ sudo pip3 install apiclient
   to get help make Google's api functioning
3) $ sudo pip3 install oauth2client
   to enable OAuth
4) $ sudo pip install --upgrade pip google-api-python-client
   to pick up google API library


Before runing generate_menu.py, please pull the updated recipe_db.json which is our database. Everytime the function generate_menu.py is run, please push the updated recipe_db.json as a courtesy to future users, as there might be new recipes not seen before updated in recipe_db.

Maximum time in the search form only refers to the preparation time. It might take a significant longer time in reality.

Some calories amount are unreasonable from the information the api returns. We have no way to deal with that.

The fewer the requirements entered in django, the faster our program runs and the greater the chance is to successfully generate the menu. If insufficient recipes are found for a given preference, an error message will appear at the bottom of the page explaining the reason.

Please make sure only enter reasonable inputs to django:
1) Only enter meal index for "Alternative Meal(s) A/B"
2) Please give reasonable range for calories, where the upper limit must be greater than the lower limit. In general, we recommend a range of greater than 500 Kcal to maximize your chance of obtaining menu within this range. Please note that if we can't fulfill the calories requirement within a specified number of trials, we will omit this requirement.
3) There shouldn't be contradicting arguments, such as entering "chicken" as an ingredient to include and selecting "Vegan" as a dietary restriction, or entering "egg" as an ingredient to include and "Egg" as an allergy.