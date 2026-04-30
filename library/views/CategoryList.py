from django.views.generic import ListView
from django.db.models import Count, Q
from library.models import Category
from django.contrib.auth.mixins import LoginRequiredMixin


class CategoryListView(LoginRequiredMixin,ListView):
    model = Category
    template_name = "library/category_list.html"
    context_object_name = 'categories'
    paginate_by = 10

    def get_queryset(self):
        queryset = Category.objects.annotate(book_count=Count('books')).order_by('-id')

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
            )

        return queryset