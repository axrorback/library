from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from library.models import Book, Category, BookPurchase

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = "library/book_detail.html"
    context_object_name = 'book'
    slug_url_kwarg = 'book_slug'

    def get_queryset(self):
        return Book.objects.filter(
            is_active=True, 
            categories__slug=self.kwargs['category_slug']
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        user = self.request.user

        has_access = book.is_free
        if not has_access and user.is_authenticated:
            has_access = BookPurchase.objects.filter(
                user=user, 
                book=book, 
                status=BookPurchase.Status.PAID
            ).exists()

        context['category'] = book.categories.filter(slug=self.kwargs['category_slug']).first()
        context['has_access'] = has_access
        return context