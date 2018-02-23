from django.urls import path
from .api.views import PostListAPIView, PostDetailsAPIView

app_name = 'blog'

urlpatterns = [
    path('<int:pk>/', PostDetailsAPIView.as_view(), name='detail'),
    path('/', PostListAPIView.as_view(), name="list"),
]
