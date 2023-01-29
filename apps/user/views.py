import re
#导入正则表达式模块
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect
from django.urls import reverse

from  apps.user.models import User
#导入用户模型类


# Create your views here.
#/user/register
def register(request):
    "show the register page"
    # Render: 渲染
    if request.method == 'GET':
        #显示页面
        return  render(request, 'register.html')
    else:
        register_handle(request)
        #进行注册处理


    return render(request, 'register.html')

def register_handle(request):
    "进行注册的处理"
    #  1. 访问地址的时候如果发过来数据应该接受数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow') # checkBox: on

    #2. 进行数据的校验
    "2.1 all方法进行数据校验，进行迭代，对里面的方法进行判断，如果都为真才会进行返回"
    # 2.1 数据不完整
    if not all([username, password, email]):
        return render(request, 'register.html', {'errmsg': 'Please input all the information'})


    # 2.2. 正则匹配校验邮箱
    #/^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
    
    """
    re.match(pattern, string, flags=0) 是 Python 中正则表达式库 re 中的一个函数，用于在一个字符串中匹配正则表达式模式。
    其中，pattern 参数是一个字符串，代表正则表达式模式。
    string 参数是要匹配的字符串。flags 参数是一个整数，可以是零或多个标志的组合。
    这个函数会在字符串的开头匹配正则表达式模式，并返回一个匹配对象（如果匹配成功）或 None（如果匹配失败）。
    """
    pattern = r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$'

    if not re.match(pattern, email):
        return render(request, 'register.html', {'errmsg':'Wrong Form '})

    if allow != 'on':
        return render(request, 'register.html', {'errmsg' : 'Please check and Agree the User Policy'})


    #检查用户名是否重复

    #3. 如果数据没有问题，进行业务处理
        #使用Django内置的认证系统

    # user = User()
    # user.username = username
    # user.password = password
    # ...
    # user.save()
    # 用户名是否重复
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        # 用户名不存在
        user = None

    if user:
        return render(request, 'register.html', {'errmag' : 'Username alreaady exit'})

        #储存用户信息
    user = User.objects.create_user(username, email, password)
    user.is_active = 0
    user.save()

    # 返回应答, 跳转到首页

    return redirect(reverse('goods : index'))