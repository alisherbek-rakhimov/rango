from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse

from .forms import PageForm, CategoryForm, UserForm, UserProfileForm
from .models import Page, Category, UserProfile


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages = Page.objects.order_by('views')[:5]
    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': category_list,
        'pages': pages,
    }

    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    visitor_cookie_handler(request)

    return render(request, 'rango/about.html', context={
        'visits': request.session.get('visits', 1)
    })


def show_category(request, category_name_slug):
    context_dict = dict()
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    # You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('rango:index')
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    return render(request, 'rango/add_page.html', {'form': form, 'category': category})


@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rango:index')
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def restricted(request):
    # return HttpResponse("Since you're logged in, you can see this text!")
    return render(request, 'rango/restricted.html')


# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


# Updated the function definition
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).seconds > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits

# @login_required
# def user_logout(request):
#     logout(request)
#     return redirect('rango:index')
#
# def register(request):
#     registered = False
#
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         profile_form = UserProfileForm(request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#
#             profile.save()
#
#             registered = True
#         else:
#             print(user_form.errors, profile_form.errors)
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     return render(request, 'rango/register.html',
#                   {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
#
#
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return redirect('rango:index')
#             else:
#                 return HttpResponse('Your Rango account is disabled.')
#         else:
#             print(f"Invalid login details: {username}, {password}")
#             return HttpResponse("Invalid login details supplied.")
#
#     else:
#         return render(request, 'rango/login.html')
