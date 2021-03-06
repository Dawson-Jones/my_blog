from django import template
from comments.forms import CommentForm

register = template.Library()

# 评论表格
@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    if form is None:
        form = CommentForm()

    return {
        'form': form,
        'post': post,
    }

# 评论
@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    comment_list = post.comment_set.all().order_by('-created_time')
    comment_count = comment_list.count()

    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
    }









