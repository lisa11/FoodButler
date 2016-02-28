from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
import logging

class Widgets(forms.MultiWidget):
    def __init__(self, attrs=None, dt=None, mode=0):
        _widgets = (forms.widgets.NumberInput, forms.widgets.NumberInput)
        super(Widgets, self).__init__(_widgets, attrs)
    def decompress(self, values):
        logging.error("WHAT IS VALUES%s" % (values,))
        print('decompress value: ', values)
        return values

class ValueField(forms.fields.MultiValueField):
    widget = Widgets()
    def __init__(self, *args, **kwargs):
        fields = [forms.fields.IntegerField(),
                  forms.fields.IntegerField()]
        super(ValueField, self).__init__(fields,
                                        *args, **kwargs)
    def compress(self, values):
        logging.error("WHAT IS VALUES2 %s" % (values,))
        return values


class IntegerRange(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (forms.IntegerField(),
                  forms.IntegerField())
        super(IntegerRange, self).__init__(fields=fields,
                                           *args, **kwargs)

    def compress(self, values):
        if values and (values[0] is None or values[1] is None):
            raise forms.ValidationError('Must specify both lower and upper '
                                        'bound, or leave both blank.')

        return values

    def decompress(self, values):
        return values

RANGE_WIDGET = forms.widgets.MultiWidget(widgets=(forms.widgets.NumberInput,
                                                  forms.widgets.NumberInput))

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

    ###cooking_time=IntegerRange(widget=RANGE_WIDGET)#ValueField(
        #required=False)
    ###calories=IntegerRange(widget=RANGE_WIDGET)

    #ValueField()
    ###servings=forms.ChoiceField(
    ###    label='Servings', 
    ###    choices=[(x, x) for x in SERVINGS])


# Source: http://stackoverflow.com/questions/3765887/add-request-get-variable-using-django-shortcuts-redirect
def custom_redirect(url_name, *args, **kwargs):
    from django.core.urlresolvers import reverse 
    import urllib
    url = reverse(url_name, args=args)
    print(kwargs)
    params = urllib.parse.urlencode(kwargs)

    import pdb; pdb.set_trace()
    return HttpResponseRedirect(url + "?%s" % params)

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

def results(request):
    form = SearchForm(request.GET)
    c = {}
    if form.is_valid():
        #calories = form.cleaned_data['calories']
        #c['calories'] = calories
        avoid = form.cleaned_data['avoid']
        c['avoid'] = avoid
        print("here")
    print("c", c)
    return render(request, "query/results.html", c)
