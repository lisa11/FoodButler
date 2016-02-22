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


ALLERGIES = ['Dairy', 'Egg', 'Gluten', 'Peanut', 'Soy', 'Sulfite', 'Treenut', 'Wheat']
DIET = ['Lacto vegetarian', 'Ovo vegetarian', 'Pescetarian', 'Vegan', 'Vegetarian']
SERVINGS = [1, 2, 3, 4]

class SearchForm(forms.Form):
    avoid=forms.CharField(
        label="Ingredients to avoid", 
        #help_text="ingredients you want to avoid",
        #required=False
        )
    already_have=forms.CharField(
        label='Ingredients already have', 
        #help_text="ingredients you already have",
        required=False)
    allergy=forms.MultipleChoiceField(
        #fields=(forms.IntegerField(),
        #          forms.IntegerField()),
        label='Allergy',
        choices=[(x, x) for x in ALLERGIES],
        widget=forms.CheckboxSelectMultiple, 
        required=False)
    diet = forms.MultipleChoiceField(
        label='Diet',
        choices= [(x, x) for x in DIET],
        widget=forms.CheckboxSelectMultiple, 
        required=False)
    cooking_time=ValueField(
        required=False)
    calories=ValueField(
        required=False)
    servings=forms.ChoiceField(
        label='Servings', 
        choices=[(x, x) for x in SERVINGS], 
        required=False)


# Source: http://stackoverflow.com/questions/3765887/add-request-get-variable-using-django-shortcuts-redirect
def custom_redirect(url_name, *args, **kwargs):
    from django.core.urlresolvers import reverse 
    import urllib
    url = reverse(url_name, args=args)
    print(kwargs)
    params = urllib.parse.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)

def query(request):
    if request.GET.get('search'):
        form = SearchForm(request.GET)

        if form.is_valid():

            return custom_redirect('results', **form.cleaned_data)
    else:  
        form = SearchForm()
        #else:
        #    form = SearchForm()
    return render(request, "query/start.html", {"form":form})

def results(request):
    form = SearchForm(request.GET)
    c = {}
    if form.is_valid():
        avoid = form.cleaned_data['avoid']
        c['avoid'] = avoid
    return render(request, "query/results.html", c)