from django.urls import path

from .views import ProjectListAPIView, TechnologyListAPIView

urlpatterns = [
    path('projects/', ProjectListAPIView.as_view(), name='projects-list'),
    path('technologies/', TechnologyListAPIView.as_view(), name='technology-list'),
]