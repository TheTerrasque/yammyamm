from django.conf.urls import url

from .views import Home, Mods, Services

urlpatterns = [
    url(r'^$', Home.as_view(), name='index'),
    url(r'^services/$', Services.as_view(), name='servicelist'),
    url(r'^mods/$', Mods.as_view(), name='modlist'),
]