# DailyFresh
*Online Store Websit*

## To Run the server:
Using `python manage.py runserver` at Terminal
## Some Tips for the Migrating versions of Django
### 1. `HTML` Files
#### `Register.html`   
The staticfiles library was removed in Django 2.0 and was replaced with the static library.   
To fix this error, you should replace `{% load staticfiles %}` with `{% load static %}` in your templates and you should also remove or update any django.contrib.staticfiles from your installed apps, since this library is not needed anymore.

### 2. `view` Files
#### `user/views.py`
`from django.core.urlresolvers import reverse`  should be replaced by `from django.urls import reverse`
