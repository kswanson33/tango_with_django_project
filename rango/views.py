from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page

def index(request):
    #return HttpResponse('Rango says hey there partner! <br/> <a href=\'/rango/about/\'>About</a>')
    ##content_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    ##return render(request, 'rango/index.html', context=content_dict)
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}
    return render(request, 'rango/index.html', context_dict)

def about(request):
    #return HttpResponse('Rango says here is the about page. <br/> <a href=\'/rango/\'>Index</a>')
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        # Try to get a category name slug wiht the given name
        category = Category.objects.get(slug=category_name_slug)
        # Retrieve all pages in category
        pages = Page.objects.filter(category=category)
        # Add our results to template context
        context_dict['pages'] = pages
        # Also add category object to context dict
        context_dict['category'] = category
    except Category.DoesNotExist:
        # If we didn't find the specified category, context_dict contains Nones
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context_dict)
