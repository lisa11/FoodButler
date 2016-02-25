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
    avoid=forms.CharField(
        label="Ingredients to avoid", 
        #help_text="ingredients you want to avoid",
        #required=False)
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
            #logging.error("what is this" % (form))
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
        #calories = form.cleaned_data['calories']
        #c['calories'] = calories
        avoid = form.cleaned_data['avoid']
        c['avoid'] = avoid
        print("here")
    print("c", c)
    return render(request, "query/results.html", c)
