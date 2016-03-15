from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.
def abc(request):
    c = {
        "name": "Lisa"
        "foods": ["sushi", "pizza"]
    }
    
    return render(request, 'diary/start.html', c)

    