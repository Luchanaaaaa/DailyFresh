# DailyFresh
*Online Store Websit*

## Some Tips for the Migrating versions of Django
### 1. `html` Files
#### `Register.html`   
The staticfiles library was removed in Django 2.0 and was replaced with the static library.   
To fix this error, you should replace `{% load staticfiles %}` with `{% load static %}` in your templates and you should also remove or update any django.contrib.staticfiles from your installed apps, since this library is not needed anymore.
