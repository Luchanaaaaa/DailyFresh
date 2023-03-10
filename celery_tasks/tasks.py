from  celery import  Celery
from django.conf import settings
from django.core.mail import send_mail
import time

app = Celery('celery_tasks.tasks', broker='redis://localhost:6379/0')


# TODO： Use Log files to track the worker (The worker might deploy the Django at first. ) PS: add password at first!

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
    send_mail(subject, message, sender, receiver, html_message= htmlMessage)
    # 返回应答, 跳转到首页
