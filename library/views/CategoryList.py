from django.db.models import Count
from django.shortcuts import render
from library.models import Category


def category_list(request):
    categories = Category.objects.annotate(book_count=Count('books'))
    context = {
        'categories': categories
    }
    return render(request, "library/category_list.html",context)