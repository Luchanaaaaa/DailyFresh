import re
#导入正则表达式模块
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.conf import settings

from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from apps.user.models import User

from django.http import HttpResponse

from celery_tasks.tasks import sendRegisterActiveEmail
from django.contrib.auth import authenticate, login

#导入用户模型类
# Create your views here.
#/user/register

class RegisterView(View):
    def get(self, request):
        '''显示注册页面'''

        return  render(request,'register.html')
    def post(self, request):

        '''进行注册处理'''
        #  1. 访问地址的时候如果发过来数据应该接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')  # checkBox: on

        # 2. 进行数据的校验
        "2.1 all方法进行数据校验，进行迭代，对里面的方法进行判断，如果都为真才会进行返回"
        # 2.1 数据不完整
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': 'Please input all the information'})

        # 2.2. 正则匹配校验邮箱
        # /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

        """
        re.match(pattern, string, flags=0) 是 Python 中正则表达式库 re 中的一个函数，用于在一个字符串中匹配正则表达式模式。
        其中，pattern 参数是一个字符串，代表正则表达式模式。
        string 参数是要匹配的字符串。flags 参数是一个整数，可以是零或多个标志的组合。
        这个函数会在字符串的开头匹配正则表达式模式，并返回一个匹配对象（如果匹配成功）或 None（如果匹配失败）。
        """
        pattern = r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$'

        if not re.match(pattern, email):
            return render(request, 'register.html', {'errmsg': 'Wrong Form '})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': 'Please check and Agree the User Policy'})

        # 检查用户名是否重复

        # 3. 如果数据没有问题，进行业务处理
        # 使用Django内置的认证系统

        # user = User()
        # user.username = username
        # user.password = password
        # ...
        # user.save()

        #------ This part is to check if the user is already existing----#
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            return render(request, 'register.html', {'errmsg': 'Username already exists'})

        # 储存用户信息
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # -------Send active (active link) email http://127.0.0.1:8000/user/active/3
        # The link must include the ID of user, but considering safe: encryption
        # Encrypt the user information: TOKEN
        # Set the expired time: current time + valid time  Example: 5 minutes
        expire = datetime.utcnow() + timedelta(minutes=60)
        # exp && information want to be encrypted
        infEncode = {"exp": expire, 'confirm': user.id }
        # Creat token
        token = jwt.encode(infEncode, settings.SECRET_KEY, algorithm="HS256")
        # return bytes

        # EMAIL
        sendRegisterActiveEmail.delay(email, username, token)


        return redirect(reverse('goods:index'))

class ActiveView(View):
    ''' Active '''
    def get(self, request, token):
        '''acitve user'''
        # decode
       # decodeJwt = jwt.decode(token, settings.SECRET_KEY, algorithm="HS256")

        try:
            info = jwt.decode(token, settings.SECRET_KEY, algorithm="HS256")
            # Get the uer id
            user_id = info['confirm']

            # Get user information and update active state
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            # Redeirction to Log in page
            return redirect(reverse('user:login'))
        except ExpiredSignatureError as e:
            return HttpResponse("The activation link has expired, please resend the email")
        except JWTError as e:
            return HttpResponse("Token verification failed")

# /user/login
class LoginView(View):
    def get(self, request):

        # Look at if remember username
        if ('username' in request.COOKIES) and ('pwd' in request.COOKIES):
            username = request.COOKIES.get('username')
            pwd = request.COOKIES.get('pwd')
            checked = 'checked'
        else:
            username = ''
            pwd = ''
            checked = ''

        # 使用模版
        return render(request, 'login.html',{'username':username, 'pwd':pwd, 'checked':checked})

    def post(self, request):
        ''
        # 1. Receive the data
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        if not all([username, password]):
            return render(request, 'login.html', {'errmsg' : 'Data missed'})

        user = authenticate(username = username, password = password)

        if user is not None:
            # the password verified for the user
            if user.is_active:
                # Record the login status of the user
                login(request, user)
                # Get the URL to redirect
                next_url = request.GET.get('next', reverse('goods:index'))
                # jump to the home page
                response = redirect(next_url)  # HttpResponseRedirect
                # MEMO USERNAME
                remember = request.POST.get('remember')

                if remember == 'on':
                    response.set_cookie('username', username, max_age= 7* 24*3600)
                    response.set_cookie('pwd', password, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')

                return response
            else:
                return render(request, 'login.html', {'errmsg': 'Pleas active your account at first '})
        else:
            return render(request,'login.html', {'errmsg' : 'Wrong Username or Password '})
        # Check data
#
class UserInfoView(View):
    '''用户中心-信息页'''
    def get(self, request):
        return render(request, 'user_center_info.html', {'page':'user'})
        print('我来了')

# /user/order
class UserOrderView(View):
    '''UserCenter- Oder Page'''
    def get(self, request):
        return render(request, 'user_center_order.html', {'page':'order'})

# /user/address
class AddressView(View):
    '''UserCenter-Address'''
    def get(self, request):
        return render(request, 'user_center_site.html',{'page':'address'})