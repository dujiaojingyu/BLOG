from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.models import User
from mysite.forms import LoginForm
from mysite.forms import RegisterForm
# Create your views here.
def login(request):
    """登录"""
    """
    username = request.POST.get('username',None)
    password = request.POST.get('password',None)
    user = auth.authenticate(request, username=username, password=password)
    referer = request.META.get('HTTP_REFERER',reverse('home'))
    print(user)
    if user is not None:
        auth.login(request, user)
        # Redirect to a success page.
        return redirect(referer)
    else:
        # Return an 'invalid login' error message.
        context = {}
        context['message'] = '用户名或密码错误'
        return render(request,'error.html',context)
    """
    if request.method == "POST":
        login_form = LoginForm(request.POST)  #从forms表单获取数据
        if login_form.is_valid():              #检查数据是否正确
            user = login_form.cleaned_data['user']  #获取用户
            auth.login(request, user)               #登录
            # Redirect to a success page.
            print(request.GET.get("from",reverse('home')))
            return redirect(request.GET.get("from",reverse('home'))) #跳转回原页面,最先获取from数据，没有则用reverse('home')代替
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'account/login.html', context)

def logout(request):
    auth.logout(request)
    return  redirect('home')

def register(request):
    """注册"""
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid(): #执行is_valid()会执行在form.py的 clean等系列的函数
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = User.objects.create_user(username,email,password)#创建注册用户并设置密码
            user.save()
            # Redirect to a success page.
            user = auth.authenticate(username=username, password=password)
            auth.login(request,user)
            return redirect(request.GET.get("from",reverse('home')))
    else:
        register_form = RegisterForm()
    context = {}
    context['register_form'] = register_form
    return render(request, 'account/register.html', context)

