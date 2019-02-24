from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls

from apps.blog.feed import LatestPostsFeed


wagtail_patterns = [
    re_path(r'^cms/', include(wagtailadmin_urls)),
    re_path(r'^pages/', include(wagtail_urls)),
]
urlpatterns = [
    path('', include('apps.about_me.urls', namespace='about_me')),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('_internal-portal_/', admin.site.urls),
    path('api/apartments/', include('apps.apartments_analyzer.urls')),
    path('api/books/', include('apps.books.api.urls')),
    path('api/blog/', include('apps.blog.urls')),
    path('api/health/', include('health_check.urls')),
    path('api/', include('apps.about_me.api.urls')),
    path('feed/latest', LatestPostsFeed()),
]

urlpatterns += wagtail_patterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # ... the rest of your URLconf goes here ...

    urlpatterns += staticfiles_urlpatterns()
