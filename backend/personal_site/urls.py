from django.conf import settings
from django.conf.urls import include
from django.urls import path

from django.contrib import admin

from blog.feed import LatestPostsFeed


urlpatterns = [
    path('', include('about_me.urls', namespace='about_me')),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('_internal-portal_/', admin.site.urls),
    path('api/apartments/', include('apartments_analyzer.urls')),
    path('api/books/', include('books.api.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/health/', include('health_check.urls')),
    path('api/statistics/', include('statistics.urls')),
    path('api/', include('about_me.api.urls')),
    path('feed/latest', LatestPostsFeed()),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # ... the rest of your URLconf goes here ...

    urlpatterns += staticfiles_urlpatterns()
