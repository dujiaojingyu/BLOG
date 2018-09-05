# from django.shortcuts import get_object_or_404

from django.shortcuts import render
from django.core.cache import cache

from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_date
from read_statistics.utils import get_today_hot_date
from read_statistics.utils import get_yesterday_hot_date
from read_statistics.utils import get_seven_days_hot_blog
from blog.models import Blog

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


