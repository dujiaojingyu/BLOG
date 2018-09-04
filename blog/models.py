from django.db import models
from django.contrib.auth.models import User
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from read_statistics.models import ReadNumExpandMethod,ReadDetail


# Create your models here.



class BlogType(models.Model):
    """博客分类"""
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model,ReadNumExpandMethod):
    """博客文章"""
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    # content = RichTextField()                    #使用ckeditor编辑器(不带图片上传)
    content = RichTextUploadingField()             #使用ckeditor编辑器(带图片上传)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    # 暂时先创建一个字段read_num
    # read_num = models.IntegerField(default=0)  #自定义一简单的计数

    """
    def get_read_num(self):
        '''获取模型ReadNum的属性read_num'''
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0
    """

    def __str__(self):
        return "<blog:%s>" % self.title

    #按创建时间的逆顺序排序，有分页功能时要加上，不然会出错
    class Meta:
        ordering = ['-created_time']

"""
#自定义二 计数功能优化
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog,on_delete=models.DO_NOTHING)
"""