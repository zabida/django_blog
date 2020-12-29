import re

import markdown
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

from blog.models import Post, Category, Tag
from utils.page_tools import page_return


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    data = page_return(request, post_list)
    data['post_list'] = data['data']
    del data['data']
    print(data)
    return render(request, 'blog/index.html', context=data)


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',    # 目录拓展
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m else ''
    return render(request, 'blog/detail.html', context={'post': post})


def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    # post_list = Post.objects.filter(category=cate).order_by('-created_time')
    post_list = cate.post_set.order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = tag.post_set.order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
