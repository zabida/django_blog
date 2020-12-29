from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from blog.models import Post
from comments.forms import CommentForm


@require_POST
def comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')
        # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
        # 然后重定向到 get_absolute_url 方法返回的 URL。
        return redirect(post)

    context = {
        'post': post,
        'form': form
    }
    messages.add_message(request, messages.ERROR, '评论发表失败！请修改表单中的错误重新提交', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)