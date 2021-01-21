import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
import random

django.setup()
from rango.models import Category, Page


def populate():
    python_pages = [
        {'title': 'Official Python Tutorial', 'url': 'https://docs.python.org/3/tutorial/'},
        {'title': 'How to Think like a Computer Scientist', 'url': 'http://www.greenteapress.com/thinkpython/'},
        {'title': 'Learn Python in 10 Minutes', 'url': 'http://www.korokithakis.net/tutorials/python/'},
    ]

    django_pages = [
        {'title': 'Official Django Tutorial', 'url': 'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'},
        {'title': 'Django Rocks', 'url': 'http://www.djangorocks.com/'},
        {'title': 'How to Tango with Django', 'url': 'http://www.tangowithdjango.com/'}
    ]

    other_pages = [
        {'title': 'Bottle', 'url': 'http://bottlepy.org/docs/dev/'},
        {'title': 'Flask', 'url': 'http://flask.pocoo.org'}
    ]

    cats = {'Python': {'pages': python_pages},
            'Django': {'pages': django_pages},
            'Other Frameworks': {'pages': other_pages}}

    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')


def add_page(cat, title, url):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = random.randint(0, 100)
    p.save()
    return p


def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    if name == 'Python':
        c.views = 128
        c.likes = 64
    elif name == 'Django':
        c.views = 64
        c.likes = 32
    elif name == 'Other Frameworks':
        c.views = 32
        c.likes = 16
    c.save()
    return c


# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
