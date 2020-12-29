import math

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def page_return(r, q, size=10):
    page_nu = int(r.GET.get('page_nu', 1))
    if not page_nu:
        page_nu = 1
    page_size = int(r.GET.get('page_size', size))
    total = q.count()
    previous_page_nu = 0
    next_page_nu = None
    paginator = Paginator(q, page_size)
    try:
        q = paginator.page(page_nu)
        previous_page_nu = page_nu - 1 if page_nu > 1 else 0
        next_page_nu = page_nu + 1
    except PageNotAnInteger:
        q = paginator.page(1)
        next_page_nu = 2 if paginator.num_pages > 1 else 1
    except EmptyPage:
        q = paginator.page(paginator.num_pages)
        previous_page_nu = paginator.num_pages - 1

    page_dict = {
        'previous_page': previous_page_nu,
        'next_page': next_page_nu,
        'page_nu': page_nu,
        'page_size': page_size,
        'total': total,
        'total_page': paginator.num_pages
    }
    data = {
        'page': page_dict,
        'data': q
    }
    return data
