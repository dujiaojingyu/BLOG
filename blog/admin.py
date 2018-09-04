from django.contrib import admin
from .models import BlogType,Blog
# from .models import ReadNum

# Register your models here.


@admin.register(BlogType)  #推荐用装饰器来注册模型
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')
    ordering = ('id',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title','blog_type','author','get_read_num','created_time','last_updated_time')
    ordering = ('id',)

"""
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num','blog')
"""