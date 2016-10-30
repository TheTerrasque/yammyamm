from django.conf.urls import url

from .views import ServiceDisplay, Services, ModDisplay, ModCreate, ModEdit, \
                    ModCreateRelation, ModEditRelation, ModRemoveRelation, UserMods, \
                    ModVersionCreate, ModVersionEdit

urlpatterns = [
    url(r'^$', Services.as_view(), name='servicelist'),
    url(r'^service/(?P<pk>[0-9]+)/$', ServiceDisplay.as_view(), name='servicedetail'),
    url(r'^mods/(?P<pk>[0-9]+)/$', ModDisplay.as_view(), name="moddetail"),
    url(r'^mods/(?P<pk>[0-9]+)/edit/$', ModEdit.as_view(), name="mod_edit"),
    url(r'^mods/(?P<modid>[0-9]+)/version/$', ModVersionCreate.as_view(), name="mod_create_version"),
    url(r'^mods/version/(?P<pk>[0-9]+)/$', ModVersionEdit.as_view(), name="mod_edit_version"),
    url(r'^mods/version/(?P<pk>[0-9]+)/remove/$', ModVersionEdit.as_view(), name="mod_remove_version"),
    url(r'^mods/(?P<pk>[0-9]+)/new_relation/$', ModCreateRelation.as_view(), name="mod_create_relation"),
    url(r'^mods/relation/(?P<pk>[0-9]+)/edit/$', ModEditRelation.as_view(), name="mod_edit_relation"),
    url(r'^mods/relation/(?P<pk>[0-9]+)/remove/$', ModRemoveRelation.as_view(), name="mod_remove_relation"),
    url(r'^service/(?P<pk>[0-9]+)/addmod/$', ModCreate.as_view(), name="mod_create"),
    url(r'^mymods/$', UserMods.as_view(), name="user_mods"),
]