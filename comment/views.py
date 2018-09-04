from django.shortcuts import render,redirect
from .models import Comment
from django.shortcuts import reverse
from django.contrib.contenttypes.models import ContentType
# Create your views here.

def update_comment(request):
    context = {}
    referer = request.META.get('HTTP_REFERER',reverse('home'))
    #数据检查
    user = request.user
    if not user.is_authenticated:
        context['message'] = '用户未登录'
        context['referer_to'] = referer
        return render(request,'error.html',context)
    text = request.POST.get('text',None).strip()
    if not text:
        context['message'] = '评论不能为空'
        context['referer_to'] = referer
        return render(request, 'error.html', context)
    try:
        content_type = request.POST.get('content_type',None)
        object_id = int(request.POST.get('object_id',None))
        model_calss = ContentType.objects.get(model=content_type).model_class() #动态获取模型
        model_obj = model_calss.objects.get(id=object_id)    #获取具体博客
    except Exception as e:
        context['message'] = '评论对象不存在'
        context['referer_to'] = referer
        return render(request, 'error.html', context)

    #保存数据
    comment = Comment()
    comment.user = user
    comment.text = text
    comment.content_object = model_obj
    comment.save()

    print(referer)
    return redirect(referer)