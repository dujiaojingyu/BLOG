from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import reverse
from .models import Comment
from .forms import CommentForm
# Create your views here.

def update_comment(request):
    # context = {}
    # referer = request.META.get('HTTP_REFERER',reverse('home'))
    # #数据检查
    # user = request.user
    # if not user.is_authenticated:
    #     context['message'] = '用户未登录'
    #     context['referer_to'] = referer
    #     return render(request,'error.html',context)
    #
    # text = request.POST.get('text',None).strip()
    # if not text:
    #     context['message'] = '评论不能为空'
    #     context['referer_to'] = referer
    #     return render(request, 'error.html', context)
    # try:
    #     content_type = request.POST.get('content_type',None)
    #     object_id = int(request.POST.get('object_id',None))
    #     model_calss = ContentType.objects.get(model=content_type).model_class() #动态获取模型
    #     model_obj = model_calss.objects.get(id=object_id)    #获取具体博客
    # except Exception as e:
    #     context['message'] = '评论对象不存在'
    #     context['referer_to'] = referer
    #     return render(request, 'error.html', context)
    #
    # #保存数据
    # comment = Comment()
    # comment.user = user
    # comment.text = text
    # comment.content_object = model_obj
    # comment.save()
    #
    # return redirect(referer)

    if request.method == "POST":
        comment_form = CommentForm(request.POST,user=request.user) #将参数user=request.user传入CommentForm
        referer = request.META.get('HTTP_REFERER',reverse('home'))  #获取当前页的url
        # 验证数据是否正确
        if comment_form.is_valid():
            comment = Comment()
            comment.user = comment_form.cleaned_data['user']
            comment.text = comment_form.cleaned_data['text']
            comment.content_object = comment_form.cleaned_data['content_object']
            comment.save()

            #返回成功数据
            data = {}
            data['status'] = "SUCCESS"
            data['username'] = comment.user.username
            data['comment_time'] = comment.comment_time.strftime("%Y-%m-%d %H:%M:%S")
            data['text'] = comment.text
        else:
            #返回失败数据
            data = {}
            data['status'] = "ERROR"
            data['message'] = list(comment_form.errors.values())[0]
        return JsonResponse(data)

