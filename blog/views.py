from django.shortcuts import render,get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Count
from read_statistics.utils import read_statistics_once_read
from .models import Blog,BlogType
# from .models import ReadNum
from mysite import settings
from comment.models import Comment
from comment.forms import CommentForm
# Create your views here.

# each_page_blogs_number = 2

def get_list_common_date(request,blog_all_list):
    """获取相同数据"""
    blog_dates = Blog.objects.dates('created_time','month',order='DESC')
    paginator = Paginator(blog_all_list,settings.EACH_PAGE_BLOGS_NUMBER)   #每10页进行分页
    page_num = request.GET.get('page',1)          #get获取页码参数
    # paginator.page(int(page_num))
    page_of_blogs = paginator.get_page(page_num)  #自动识别page_num的类型

    blogs = page_of_blogs.object_list             #获取所有博客
    # blog_types = BlogType.objects.all()           #获取所有分类

    curr_page_num = page_of_blogs.number           #当前页码
    total_page_num = paginator.num_pages           #总页码

    #页码列表
    page_range_number = list(range(max(curr_page_num-2,1),curr_page_num)) \
                        + list(range(curr_page_num,min(curr_page_num+2,total_page_num+1)))
    # print(page_range_number)

    #给页码添加首页码尾页码和...
    #添加...
    if page_range_number[0] - 1 >= 2:
        page_range_number.insert(0,'...')
    if total_page_num - page_range_number[-1] >= 2:
        page_range_number.append('...')
    #添加首页码和尾页码#
    if page_range_number[0] != 1:
        page_range_number.insert(0,1)
    if page_range_number[-1] != total_page_num:
        page_range_number.append(total_page_num)

    #获取日期分类数量
    blog_datas_dict = {}
    for blog_data in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_data.year,
                            created_time__month=blog_data.month).count()
        # print(blog_count)
        blog_datas_dict[blog_data] = blog_count
        # print(blog_count)
        # print(blog_datas_dict)

    #获取博客分类数量
    #方法一  用annotate
    blog_types = BlogType.objects.annotate(blog_count=Count('blog'))

    """
    #方法二
    blog_types_list = []
    #获取每一个分类加上blog_count属性
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()  #计算分类为blog_type的博客数量
        blog_types_list.append(blog_type)         #添加到列表blog_types_list以便后续页面可以循环取出数据
    """
    #最好用这种方式提交字典
    context = {}
    # context['blog_dates'] = blog_dates
    context['blog_dates'] = blog_datas_dict
    context['page_range_number'] = page_range_number
    context['blogs'] = blogs
    # context['blog_types'] = blog_types
    # context['blog_types'] = blog_types_list
    context['blog_types'] = blog_types
    context['page_of_blogs'] = page_of_blogs
    return context

def blog_list(request):
    """博客列表"""
    blog_all_list = Blog.objects.all()                 #获取全部列表
    context = get_list_common_date(request,blog_all_list)
    return render(request,"blog/blog_list.html",context)

def blog_detail(request,blog_id):
    """博文详细"""
    blog = get_object_or_404(Blog, id=blog_id)         #获取具体某篇博客

    """
    #自定义一 简单的计数
    if not request.COOKIES.get('blog_%s_read'%blog_id):
        blog.read_num += 1
        blog.save()
    """
    """
    #自定义二 计数功能优化
    if not request.COOKIES.get('blog_%s_read'%blog_id):
        if ReadNum.objects.filter(blog=blog).count():
            #存在记录
            readnum = ReadNum.objects.get(blog=blog)
        else:
            #不存在对应记录
            readnum = ReadNum(blog=blog)
        readnum.read_num += 1
        readnum.save()
    """

    #运用了封装的思想
    read_cookie_key = read_statistics_once_read(request,blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    commnets = Comment.objects.filter(content_type=blog_content_type,object_id=blog.id)

    previous_blog = Blog.objects.filter(created_time__gt=blog.created_time).last()
    next_blog = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context = {}
    context['comment_Form'] = CommentForm(initial={'content_type':blog_content_type,'object_id':blog.id})
    context['commnets'] = commnets
    context['previous_blog'] = previous_blog
    context['next_blog'] = next_blog
    context['blog'] = blog

    response = render(request,'blog/blog_detail.html',context)  #取返回数据
    response.set_cookie(read_cookie_key,'true')                 #阅读cookie的标记
    return response

def blogs_wilth_type(request,blog_type_id):
    """博文分类"""
    # blog_type = get_object_or_404(BlogType,id=blog_type_id)  #获取id为blog_type_id的博客分类
    # blogs = Blog.objects.filter(blog_type=blog_type)         #筛选出博客分类为blog_type的博客
    # blog_types = BlogType.objects.all()                      #获取全部博客分类
    # print('...',blog_type)
    # print(blog_types)
    # context = {}
    # context['blogs'] = blogs

    blog_type = get_object_or_404(BlogType,id=blog_type_id)         #获取id为blog_type_id的博客分类
    blog_all_list = Blog.objects.filter(blog_type=blog_type)        #获取全部分类文章列表


    #最好用这种方式提交字典
    context = get_list_common_date(request, blog_all_list)
    context['blog_type'] = blog_type
    return render(request,'blog/blogs_wilth_type.html',context)

def blogs_wilth_date(request,year,month):
    """日期分类"""
    blog_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)        #获取全部分类文章列表
    context = get_list_common_date(request, blog_all_list)
    context['blogs_with_dats'] = '%s年%s月'%(year,month)
    return render(request,'blog/blogs_wilth_date.html',context)
