from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    content_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    return render(request, 'rango/index.html', context=content_dict)

def about(request):
    return render(request, 'rango/about.html')
