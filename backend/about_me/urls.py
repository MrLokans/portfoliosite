from django.urls import path

from .api.views import ProjectListAPIView, TechnologyListAPIView

app_name = 'about_me'

urlpatterns = [
    path('projects/', ProjectListAPIView.as_view(), name='projects-list'),
    path('technologies/', TechnologyListAPIView.as_view(), name='technology-list'),
]
