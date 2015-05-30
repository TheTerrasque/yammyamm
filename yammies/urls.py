from django.conf.urls import url

from .views import Home, Mods, Services, ModDisplay

urlpatterns = [
    url(r'^$', Home.as_view(), name='index'),
    url(r'^services/$', Services.as_view(), name='servicelist'),
    url(r'^mods/$', Mods.as_view(), name='modlist'),
    url(r'^mods/(?P<pk>[0-9]+)/$', ModDisplay.as_view(), name="mod"),
]