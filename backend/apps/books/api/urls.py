from django.urls import path
from rest_framework.routers import SimpleRouter

from ..api.views import BookListAPIView, BookDetailAPIView, FavoritesViewSet

app_name = "books"

router = SimpleRouter()
router.register(r"favorites", FavoritesViewSet, basename="favorite")

urlpatterns = [
    path("<int:pk>/", BookDetailAPIView.as_view(), name="book-details"),
    path("", BookListAPIView.as_view(), name="book-list"),
]

urlpatterns += router.urls
