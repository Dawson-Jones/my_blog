from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import strip_tags
from django.urls import reverse
import markdown

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name  # 复数形式

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name  # 复数形式

    def __str__(self):
        return self.name


class Post(models.Model):
    # 文章标题
    title = models.CharField(verbose_name='标题', max_length=70)
    # 正文
    body = models.TextField('正文')
    # 创建时间和修改时间
    created_time = models.DateField('创建时间', default=timezone.now)
    modified_time = models.DateField('修改时间')
    # 摘要
    excerpt = models.CharField('摘要', max_length=200, blank=True)  # blank=True允许为空值
    # 阅读量
    views = models.PositiveIntegerField(default=0)

    # 外键, 分类一对多, 标签多对多
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    # 重写save方法, 让每次保存的时候默认保存修改时间
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 54 个字符赋给 excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:54]

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '文章'  # 后台显示的名称
        verbose_name_plural = verbose_name  # 复数形式
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])  # 只更新views域, 以提高效率
















