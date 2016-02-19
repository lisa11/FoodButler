from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django import forms

class SearchForm(forms.Form):
    avoid = forms.CharField(
        label="Ingredients to Avoid", 
        #help_text="ingredients you want to avoid",
        #required=False
        )
    must_have = forms.CharField(
        label="Ingredients to Include", 
        #help_text="ingredients you already have",
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