from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from alternative import update_menu
from generate_menu import generate_final_output
from shopping_list import generate_shopping_list
from sync_initiate import sync

#hard-coded inputs for Yummly API
ALLERGIES = [("396^Dairy-Free", "Dairy"),
    ("397^Egg-Free", "Egg"),
    ("393^Gluten-Free", "Gluten"),
    ("394^Peanut-Free","Peanut"),
    ("398^Seafood-Free", "Seafood"),
    ("399^Sesame-Free", "Sesame"),
    ("400^Soy-Free", "Soy"),
    ("401^Sulfite-Free", "Sulfite"),
    ("395^Tree Nut-Free", "Tree Nut"),
    ("392^Wheat-Free", "Wheat")]
DIET = [("388^Lacto vegetarian","Lacto vegetarian"),
    ("387^Lacto-ovo vegetarian","Lacto-ovo vegetarian"),
    ("389^Ovo vegetarian","Ovo vegetarian"),
    ("403^Paleo","Paleo"),
    ("390^Pescetarian","Pescetarian"),
    ("386^Vegan","Vegan")]
CUISINE = [("cuisine^cuisine-american","American"),
    ("cuisine^cuisine-barbecue-bbq","Barbecue"), 
    ("cuisine^cuisine-cajun","Cajun & Creole"),
    ("cuisine^cuisine-chinese","Chinese"),
    ("cuisine^cuisine-cuban","Cuban"),
    ("cuisine^cuisine-english","English"),
    ("cuisine^cuisine-french","French"),
    ("cuisine^cuisine-german,","German"),
    ("cuisine^cuisine-greek","Greek"),
    ("cuisine^cuisine-hawaiian","Hawaiian"),
    ("cuisine^cuisine-hungarian","Hungarian"),
    ("cuisine^cuisine-indian","Indian"),
    ("cuisine^cuisine-irish","Irish"),
    ("cuisine^cuisine-italian","Italian"), 
    ("cuisine^cuisine-japanese","Japanese"),
    ("cuisine^cuisine-mediterranean","Mediterranean"),
    ("cuisine^cuisine-mexican","Mexican"), 
    ("cuisine^cuisine-moroccan","Moroccan"),
    ("cuisine^cuisine-portuguese","Portuguese"),
    ("cuisine^cuisine-southwestern","Southwestern"),
    ("cuisine^cuisine-southern","Southern & Soul Food"),
    ("cuisine^cuisine-spanish","Spanish"),
    ("cuisine^cuisine-swedish", "Swedish"),
    ("cuisine^cuisine-thai","Thai")]
DAYS = [(1, "Day1"),
    (2, "Day2"), 
    (3, "Day3"),
    (4, "Day4"),
    (5, "Day5"),
    (6, "Day6"),
    (7, "Day7")]

#modified from pa3/ui/search/views.py
class SearchForm(forms.Form):
    ingredients_avoid=forms.CharField(
        label="Ingredients to Avoid", 
        #help_text="(Ingredients to avoid)",
        required=False)
    ingredients_already_have=forms.CharField(
        label='Ingredients to Include', 
        #help_text="(Ingredients to include in meal)",
        required=False)
    allergy=forms.MultipleChoiceField(
        label='Allergy',
        choices=ALLERGIES,
        widget=forms.CheckboxSelectMultiple, 
        required=False)
    diet = forms.MultipleChoiceField(
        label='Diet',
        choices=DIET,
        widget=forms.CheckboxSelectMultiple, 
        required=False)
    cuisine = forms.MultipleChoiceField(
        label='Cuisine',
        choices=CUISINE,
        widget=forms.CheckboxSelectMultiple, 
        required=False)
    time_breakfast = forms.IntegerField(
        label="Maximum Breakfast Cooking Time",
        #help_text="(Maximun breakfast cooking time)",
        min_value=0,
        max_value=300,
        required=False)
    time_meal = forms.IntegerField(
        label="Maximum Lunch/Dinner Cooking Time",
        #help_text="(Maximun lunch or dinner cooking time)",
        min_value=0,
        max_value=300, 
        required=False)
    calories_lower=forms.IntegerField(
        label="Minimum Calories Per Day", 
        min_value=1,
        max_value=5000,
        required=False)
    calories_upper=forms.IntegerField(
        label="Maximum Calories Per Day",
        min_value=1,
        max_value=5000, 
        required=False)
    alt_rm=forms.CharField(
        label='Alternative Meal(s) A',
        required=False)
    alt_add=forms.CharField(
        label='Alternative Meal(s) B',
        required=False)
    shopping_list=forms.MultipleChoiceField(
        choices=DAYS,
        widget=forms.CheckboxSelectMultiple, 
        required=False)
    synch=forms.DateField(
        label='Menu Start Date', 
        #input_formats='%Y-%m-%d',
        help_text="mm/dd/yyyy",
        required=False)
    breakfast_start=forms.TimeField(
        label='Start time for Breakfast', 
        #input_formats='%Y-%m-%d',
        help_text="HH:MM (24 hours)",
        required=False)
    lunch_start=forms.TimeField(
        label='Start time for Lunch', 
        help_text="HH:MM (24 hours)",
        required=False)
    dinner_start=forms.TimeField(
        label='Start time for Dinner', 
        help_text="HH:MM (24 hours)",
        required=False)

#modified from pa3/ui/search/views.py
def search(request):
    menu=None
    rm=None
    if request.GET.get('search'):
        form = SearchForm(request.GET)

        if form.is_valid():
            if form.cleaned_data['alt_rm'] and form.cleaned_data['alt_add']:
                rm = list(map(int, form.cleaned_data['alt_rm'].split()))
                add = list(map(int, form.cleaned_data['alt_add'].split()))
                if len(rm) == len(add):
                    breakfast_final_list, lunch_list, dinner_list, new_calories_list, alternative_breakfast_list, alternative_lunch_list, alternative_dinner_list = update_menu(rm, add)
                    menu = breakfast_final_list,lunch_list,dinner_list
                    calories = new_calories_list
                    alternative = alternative_breakfast_list, alternative_lunch_list,alternative_dinner_list
                    return render(request, "menu/search.html", {"form":form, 'm':menu, 'ca':calories, 'a':alternative})
                else:
                    return render(request, "menu/search.html", {"form":form})
            elif form.cleaned_data['shopping_list']:
                shopping_list = list(map(int, form.cleaned_data['shopping_list']))
                lsts = generate_shopping_list(shopping_list)
                return render(request, "menu/shopping_list.html", {"shopping_list":lsts}) 
            elif form.cleaned_data['synch']:
                args = {}
                if form.cleaned_data['breakfast_start']:
                    bs = form.cleaned_data['breakfast_start']
                    args['breakfast_start_time'] = [bs.hour, bs.minute, bs.second]
                if form.cleaned_data['lunch_start']:
                    ls = form.cleaned_data['lunch_start']
                    args['lunch_start_time'] = [ls.hour, ls.minute, ls.second]
                if form.cleaned_data['dinner_start']:
                    ds = form.cleaned_data['dinner_start']
                    args['dinner_start_time'] = [ds.hour, ds.minute, ds.second]
                date = form.cleaned_data['synch']
                args['start_date'] = [date.year, date.month, date.day]
                sync(args)
                return render(request, "menu/search.html", {"form":form})
            else:
                args={}
                if form.cleaned_data['ingredients_already_have']:
                    args['allowedIngredient[]'] = form.cleaned_data['ingredients_already_have'].split()
                
                if form.cleaned_data['ingredients_avoid']:
                    args['excludedIngredient[]'] = form.cleaned_data['ingredients_avoid'].split()

                if form.cleaned_data['allergy']:
                    args['allowedAllergy[]'] = form.cleaned_data['allergy']
                
                if form.cleaned_data['diet']:
                    args['allowedDiet[]'] = form.cleaned_data['diet']
                
                if form.cleaned_data['time_breakfast'] and form.cleaned_data['time_meal']:
                    args['maxTotalTimeInSeconds'] = [form.cleaned_data['time_breakfast'], form.cleaned_data['time_meal']]
                
                if form.cleaned_data['calories_lower'] and form.cleaned_data['calories_upper']:
                    args['calories_per_day'] = [form.cleaned_data['calories_lower'], form.cleaned_data['calories_upper']]
                
                if form.cleaned_data['cuisine']:
                    args['allowedCuisine[]'] = form.cleaned_data['cuisine']

                #logging.error("what is this" % (form))
                #return custom_redirect('results', **form.cleaned_data)
                
                breakfast_list, lunch_list, dinner_list, calories_list, alternative_breakfast_list, alternative_lunch_list, alternative_dinner_list = generate_final_output(args)
                m = breakfast_list,lunch_list,dinner_list
                ca = calories_list
                a = alternative_breakfast_list, alternative_lunch_list,alternative_dinner_list
                return render(request, "menu/search.html", {"form":form, 'm':m, 'ca':ca, 'a':a, "args":args})
                
    else:  
        form = SearchForm()

    return render(request, "menu/search.html", {"form":form})