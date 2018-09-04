import datetime
from django.utils import timezone
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum,ReadDetail
from blog.models import Blog

"""
def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)          #通过ContentType获取对应的models
    key = '%s_%s_read'%(ct.model,obj.id)
    if not request.COOKIES.get(key):
        if ReadNum.objects.filter(content_type=ct, object_id=obj.id).count():
            # 存在记录
            readnum = ReadNum.objects.get(content_type=ct, object_id=obj.id)
        else:
            # 不存在对应记录
            readnum = ReadNum(content_type=ct, object_id=obj.id)
        readnum.read_num += 1
        readnum.save()
    date = timezone.now().date()
    if ReadDetail.objects.filter(content_type=ct, object_id=obj.id,date=date).count():
        readdetail = ReadDetail.objects.get(content_type=ct, object_id=obj.id,date=date)
    else:
        readdetail = ReadDetail(content_type=ct, object_id=obj.id,date=date)
    readdetail.read_num += 1
    readdetail.save()
    return key
"""

def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)        # obj为具体某一篇博客，通过ContentType获取对应的models
    key = '%s_%s_read' % (ct.model, obj.id)
    if not request.COOKIES.get(key):
        #get_or_create获取有关信息，若无则创建，有则获取相关数据，返回一个元组
        #阅读数量+1
        readnum,created= ReadNum.objects.get_or_create(content_type=ct, object_id=obj.id)  #object_id储存博客的主键值
        readnum.read_num += 1
        readnum.save()
        #本日阅读数量+1
        date = timezone.now().date()
        readdetail,created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.id, date=date)
        readdetail.read_num += 1
        readdetail.save()

    return key

def get_seven_days_read_date(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(6,-1,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type,date=date)
        result = read_details.aggregate(read_num_sun=Sum('read_num'))
        read_nums.append(result['read_num_sun'] or 0)
    return dates,read_nums

def get_today_hot_date(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num') #获取模型Blog，日期为today的文章，按照read_num逆排序
    return read_details[:7]

def get_yesterday_hot_date(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=date).order_by('-read_num') #获取模型Blog，日期为today的文章，按照read_num逆排序
    return read_details[:7]

def get_seven_days_hot_blog():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects\
                    .filter(read_details__date__lt=today, read_details__date__gt=date)\
                    .values('id','title')\
                    .annotate(read_num_sum=Sum('read_details__read_num'))\
                    .order_by('-read_num_sum')
    return blogs[:7]