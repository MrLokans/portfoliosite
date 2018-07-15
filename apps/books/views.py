from django.views.generic.list import ListView

from .models import Book


class BookListView(ListView):

    model = Book
    context_object_name = 'book_data'
    template_name = 'books/book_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = Book.objects.non_empty()
        return qs
