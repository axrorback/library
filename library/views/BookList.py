from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from library.models import Book, Category
from django.contrib.auth.mixins import LoginRequiredMixin

class BookByCategoryListView(LoginRequiredMixin,ListView):
    model = Book
    template_name = "library/book_list.html"
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        queryset = Book.objects.filter(categories=self.category).order_by('-id')

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context