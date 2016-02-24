from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, world.")

def testing(request):
    return render(request, 'menu/start.html')

def output(request):
    d = {"name": "string1", 
        "calories": 50, 
        "cookingtime": 60, 
        "ingredients": ['hello', 'world'], 
        "picurl": 'string2', 
        "instructionurl": 'string3'}
    breakfast_list=[d for i in range(7)]
    lunch_list=[d for i in range(7)]
    dinner_list=[d for i in range(7)]
    calories_list=[200, 300, 500, 600, 700, 500, 450] # calories for every day
    alternative_breakfast_list=[d for i in range(7)]
    alternative_lunch_list=[d for i in range(7)]
    alternative_dinner_list=[d for i in range(7)]
    c = {'breakfast':breakfast_list, 
        'lunch':lunch_list, 
        'dinner':dinner_list, 
        'calories':calories_list,
        'abreakfast':alternative_breakfast_list, 
        'alunch':alternative_lunch_list,
        'adinner':alternative_dinner_list, 
        'list_range': 7}
    m = breakfast_list,lunch_list,dinner_list
    ca = calories_list
    a = alternative_breakfast_list, alternative_lunch_list,alternative_dinner_list

    return render(request, "menu/output.html", {"c":c, 'm':m, 'ca':ca, 'a':a})



                                                #{
                                                #'breakfast':breakfast_list, 
                                                #'lunch':lunch_list, 
                                                #'dinner':dinner_list, 
                                                #'calories':calories_list,
                                                #'abreakfast':alternative_breakfast_list, 
                                                #'alunch':alternative_lunch_list,
                                                #'adinner':alternative_dinner_list, 
                                                #'list_range': 7})
