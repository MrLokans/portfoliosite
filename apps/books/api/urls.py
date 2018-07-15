from django.urls import path

from ..api.views import BookListAPIView, BookDetailAPIView

app_name = 'books'

urlpatterns = [
    path('<int:pk>/', BookDetailAPIView.as_view(), name='book-details'),
    path('', BookListAPIView.as_view(), name='book-list'),
]
