# DailyFresh
*Online Store Website using Django*

## TO START
1. Run the server:    
Using `python manage.py runserver` at Terminal to start the server for website.    
Using `nohup redis-server` at Terminal to start the server of *Celery*
>Celery is an asynchronous task queue/job queue based on distributed message passing. It is written in Python and allows you to run tasks in the background while your application is still serving other requests. You can use Celery to handle long-running tasks, such as sending emails, generating reports, or processing images.

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
       1. Token 
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
       3. `task.py`:  Using `Celery` and `Redis` as broker to send **Asynchronous Requests**.    
        
       *Remind: do not forget to install Celery and Redis at first*.   
       `pip install celery`    
       As you can see at ` 'redis://localhost:6379/0' `, I used local host.    
       It should be noted that if you need to use Celery in a production environment, it is recommended to use a separate Redis instance as a message broker instead of running Redis locally.
       ```python
       from  celery import  Celery
       from django.conf import settings
       from django.core.mail import send_mail
       import time
       app = Celery('celery_tasks.tasks', broker='redis://localhost:6379/0')
       @app.task
       def sendRegisterActiveEmail(toEmail, username, token):
           # Send active email, include the active link: http://127.0.0.1:8000/user/active/id
           # the active link should include the User ID
           subject = "Welcome to Yvonne's PlayGround project: DailyFresh"
           message = ''
           sender = settings.EMAIL_FROM
           receiver = [toEmail]
           htmlMessage = '<h1>%s, Welcome to yvonne&apos;s websit: DailyFresh</h1> <br/> ' \
                          'Please active your account by click this link : <a href ="http://127.0.0.1:8000/user/active/%s"> http://127.0.0.1:8000/user/active/%s </a>' % (
                         username, token, token)
           # TODO??? To send the verify mail
           send_mail(subject, message, sender, receiver, html_message= htmlMessage)
           time.sleep(5)
       ```


