from django.conf.urls import url

from .views import Home, ServiceDisplay, Services, ModDisplay

urlpatterns = [
    url(r'^$', Services.as_view(), name='servicelist'),
    url(r'^service/(?P<pk>[0-9]+)/$', ServiceDisplay.as_view(), name='servicedetail'),
    url(r'^mods/(?P<pk>[0-9]+)/$', ModDisplay.as_view(), name="moddetail"),
]