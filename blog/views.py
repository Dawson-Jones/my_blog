from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Post, Category, Tag
import re
import markdown
from markdown.extensions.toc import TocExtension


# Create your views here.
class IndexView(ListView):
    # ListView 就是从数据库中获取某个模型列表数据的
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 4

def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


class CategoryView(IndexView):
    # 直接继承 IndexView 就不用写下面的三个属性了
    # model = Post
    # template_name = 'blog/index.html'
    # context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

def category(request, pk):
    # cate = get_object_or_404(Category, pk=pk)
    # post_list = Post.objects.filter(category=cate).order_by('-created_time')
    post_list = Post.objects.filter(category=pk).order_by('-created_time')
    return  render(request, 'blog/index.html', context={'post_list': post_list})


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=tag)

def tag(request, pk):
    # t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags__id=pk).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    # 获取对象
    # post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    # 阅读量+1
    post.increase_views()

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 'markdown.extensions.toc',
        TocExtension(slugify=slugify)  # slugify 参数可以接受一个函数, 将被用于处理标题的锚点值
    ])
    post.body = md.convert(post.body)
    # 获取目录中<ul>中的东西<li>
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m else ''

    return render(request, 'blog/detail.html', context={'post': post})


def search(request):
    q = request.GET.get('q')
    errmsg = ''

    if not q:
        errmsg = '请输入关键词'
        return render(request, 'blog/index.html', {'errmsg': errmsg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', context={'errmsg': errmsg, 'post_list': post_list})





def blog(request):
    return render(request, 'blog/full-width.html')


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')

























