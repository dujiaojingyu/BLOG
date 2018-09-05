# from django.shortcuts import get_object_or_404
from django.shortcuts import reverse
from django.shortcuts import redirect
from django.contrib import auth
from django.shortcuts import render
from django.core.cache import cache
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_date
from read_statistics.utils import get_today_hot_date
from read_statistics.utils import get_yesterday_hot_date
from read_statistics.utils import get_seven_days_hot_blog
from blog.models import Blog
from mysite.forms import LoginForm
from mysite.forms import RegisterForm
# Create your views here.

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)      #通过contenttype的获取相关模型的类或模型的实例，例如Blog
    dates,read_nums = get_seven_days_read_date(blog_content_type)    #传入blog模型返回数据
    today_hot_date = get_today_hot_date(blog_content_type)           #传入blog模型返回数据
    yesterday_hot_date = get_yesterday_hot_date(blog_content_type)

    #获取7天热门的缓存数据
    seven_days_hot_blog = cache.get('seven_days_hot_blog')            #cache.get('缓存名称')，获取缓存数据
    #若无缓存从数据库中获取数据，设置再缓存。
    if seven_days_hot_blog is None:
        seven_days_hot_blog = get_seven_days_hot_blog()
        cache.set('seven_days_hot_blog',seven_days_hot_blog,3600)      #设置缓存，cache.set('缓存名称',缓存的数据,缓存时间)

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_date'] = today_hot_date
    context['yesterday_hot_date'] = yesterday_hot_date
    context['seven_days_hot_blog'] = seven_days_hot_blog
    return render(request,'home.html',context)


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
            print(reverse('home'))
            return redirect(request.GET.get("from",reverse('home'))) #跳转回原页面,最先获取from数据，没有则用reverse('home')代替
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request,'login.html',context)


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
    return render(request,'register.html',context)

