from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
import logging


ALLERGIES = ['Dairy', 'Egg', 'Gluten', 'Peanut', 'Soy', 'Sulfite', 'Treenut', 'Wheat']
DIET = ['Lacto vegetarian', 'Ovo vegetarian', 'Pescetarian', 'Vegan', 'Vegetarian']
SERVINGS = [1, 2, 3, 4]

class SearchForm(forms.Form):
    ingredients_avoid=forms.CharField(
        label="Ingredients to Avoid", 
        #help_text="(Ingredients to avoid)",
        required=False)
    ingredients_already_have=forms.CharField(
        label='Ingredients to Include', 
        #help_text="(Ingredients to include in meal)",
        required=False)
    number_of_meal=forms.IntegerField(
        label='Number of Meals',
        help_text='(Number of meals to that contains Ingredients to Include)', 
        min_value=1,
        max_value=21,
        required=False)
    allergy=forms.MultipleChoiceField(
        label='Allergy',
        choices=[(x, x) for x in ALLERGIES],
        widget=forms.CheckboxSelectMultiple, 
        required=False)
    diet = forms.MultipleChoiceField(
        label='Diet',
        choices= [(x, x) for x in DIET],
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
    #servings=forms.ChoiceField(
    #    label="Serving Size", 
    #    choices=[(x, x) for x in range(1, 5)],
    #    #required=False)
    #    )
    calories_lower=forms.IntegerField(
        label="Minimum Calories Per Day", 
        min_value=0,
        max_value=5000,
        required=False)
    calories_upper=forms.IntegerField(
        label="Maximum Calories Per Day",
        min_value=0,
        max_value=5000, 
        required=False)

def query(request):
    if request.GET.get('search'):
        form = SearchForm(request.GET)

        if form.is_valid():
            args={}
            if form.cleaned_data['ingredients_already_have']:
                args['allowedIngredient[]'] = form.cleaned_data['ingredients_already_have'].split()
            
            if form.cleaned_data['ingredients_avoid']:
                args['excludedIngredient[]'] = form.cleaned_data['ingredients_avoid'].split()
            
            if form.cleaned_data['number_of_meal']:
                args['meal_number'] = form.cleaned_data['number_of_meal']

            if form.cleaned_data['allergy']:
                args['allowedAllergy[]'] = form.cleaned_data['allergy']
            
            if form.cleaned_data['diet']:
                args['allowedDiet[]'] = form.cleaned_data['diet']
            
            if form.cleaned_data['time_breakfast'] and form.cleaned_data['time_meal']:
                args['maxTotalTimeInSeconds'] = [form.cleaned_data['time_breakfast'], form.cleaned_data['time_meal']]
            
            #if form.cleaned_data['servings']:
            #    args['servings'] = form.cleaned_data['servings']
            
            if form.cleaned_data['calories_lower'] and form.cleaned_data['calories_upper']:
                args['calories_per_day'] = [form.cleaned_data['calories_lower'], form.cleaned_data['calories_upper']]
            
            #logging.error("what is this" % (form))
            #return custom_redirect('results', **form.cleaned_data)
            return render(request, "query/results.html", {"c":args})
    else:  
        form = SearchForm()
        #else:
        #    form = SearchForm()
    return render(request, "query/start.html", {"form":form})
