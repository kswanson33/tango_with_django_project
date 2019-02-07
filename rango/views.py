from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

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
        # Try to get a category name slug with the given name
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

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # Save new category to database
            cat = form.save(commit=True)
            print(cat)
            # New category will show up on the index page
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        #form.clean() # BROKEN
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category':category}
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid:
            # Save user data to database
            user = user_form.save()
            # Hash password and update user object
            user.set_password(user.password)
            user.save()
            # commit=False delays saving until we set user attribute
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Save & set registered to true
            profile.save()
            registered = True
        else:
            # Invalid form(s)
            print(user_form.errors, profile_form.errors)
    else:
        # Not HTTP POST
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', { 'user_form': user_form,
                'profile_form': profile_form, 'registered': registered } )

def user_login(request):
    if request.method == 'POST':
        # using POST.get() raises an exception if the value doesn't exist
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        # Do we have a user?
        if user:
            # Is the account active?
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # Inactive account
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        # Not a POST
        return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
