from django.conf.urls import url

from favorites.api.views import FavoritesAPIView

urlpatterns = [
    # url(r'^(?P<favorite_id>[0-9]+)/$', FavoritesAPIView.as_view(),
    #     name="favorites-detail"),
    url(r'^$', FavoritesAPIView.as_view(), name="favorites-list"),
]
