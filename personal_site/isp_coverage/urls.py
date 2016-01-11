from django.conf.urls import patterns, url
urlpatterns = patterns(
    '',
    url(r'^providers$', 'isp_coverage.views.providers_map', name='providers'),
)
