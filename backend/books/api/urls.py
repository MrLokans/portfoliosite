from books.api.views import BookListAPIView, BookDetailAPIView
from django.urls import path

app_name = 'books'

urlpatterns = [
    path('<int:pk>/', BookDetailAPIView.as_view(), name='book-list'),
    path('', BookListAPIView.as_view(), name='book-details'),
]
