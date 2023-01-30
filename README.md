# DailyFresh
*Online Store Websit*

## To Run the server:
Using `python manage.py runserver` at Terminal

## Some detail about Function Implementation
### 1. [Send active email after registion](#anchor)
[jwt](https://jwt.io/introduction).  
Instead using [ItsDangerous](https://itsdangerous.palletsprojects.com/en/2.1.x/) to encrpt the User ID, I choose to use `python-jose`



## Some Tips for the Migrating versions of Django
### 1. `HTML` Files
#### `Register.html`   
The staticfiles library was removed in Django 2.0 and was replaced with the static library.   
To fix this error, you should replace `{% load staticfiles %}` with `{% load static %}` in your templates and you should also remove or update any django.contrib.staticfiles from your installed apps, since this library is not needed anymore.


### 2. `view` Files
#### 2.1 `user/views.py`
`from django.core.urlresolvers import reverse`  should be replaced by `from django.urls import reverse`



## Appendix
 <a name="anchor"></a> 
1.  Send active email after registion
An example to use `python-jose`:   

```python
pip install python-jose
# install the libray at terminal at first

from datetime import datetime, timedelta
from jose import jwt
# SecretKey
SECRET_KEY = "kkkkk"

# Set the expire time: current time + valid time  Example: 5 minutes
expire = datetime.utcnow() + timedelta(minutes=5)
# exp |  sub & uid: Information
to_encode = {"exp": expire, "sub": str(123), "uid": "12345"}
# creat token 
encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
print(encoded_jwt) 
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1OTU1MDg5MzQsInN1YiI6IjEyMyIsInVpZCI6IjEyMzQ1In0.lttAYe808lVQgGhL9NXei2bbC1LIGs-SS0l6qfU_QxU
```
The way I used:   
```python
# Send active (active link) email http://127.0.0.1:8000/user/active/3
  # The link must include the ID of user, but considering about safe: encryption
  # encrpt the user information

  #  Set the expired time: current time + valid time  Example: 5 minutes
  expire = datetime.utcnow() + timedelta(minutes=60)
  # exp && information want to be encrypted
  infEncode = {"exp": expire, 'confirm': user.id }
  # Creat token
  encodedJwt = jwt.encode(infEncode, settings.SECRET_KEY, algorithm="HS256")
```
2. To send email with HTML format
```python
        subject = "Welcome to Yvonne's PlayGround project: DailyFresh"
        message = ''
        htmlMessage = '<h1>%s, Welcome to yvonne&apos;s websit: DailyFresh</h1> <br/> " \
                  "Please active your account by click this link : <a href ="http://127.0.0.1:8000/user/active/%s"> http://127.0.0.1:8000/user/active/%s </a>' %(username, token, token)
        sender = settings.EMAIL_FROM
        receiver = [email]
        send_mail(subject, message, sender, receiver, html_message= htmlMessage)

```



