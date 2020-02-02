from django.urls import path

from apps.spiders import views

urlpatterns = [
    path("", views.SpiderListView.as_view(), name="spiders-list"),
    path(
        "<spider_name>/config", views.SpiderConfigView.as_view(), name="spider-config"
    ),
]
