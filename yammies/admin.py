from django.contrib import admin
from .models import Mod, ModCategory, ModDependency, HostMirror, JsonService, JsonServiceSuggestion, ModVersion

from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdminTabularInline

class ModDependencyInline(AjaxSelectAdminTabularInline):
    model = ModDependency
    form = make_ajax_form(ModDependency, {'dependency': 'mod'})
    extra = 5

class ModVersionAdmin(admin.ModelAdmin):
    list_display = ['mod', 'version', "archive", "releasetype", "filesize"]
    search_fields = ['mod__name']
    fieldsets = [
        (None,            {'fields': ["archive", "version", "changelog", "releasetype"]}),
        ('Torrent data',  {'fields': ["torrent_file", "torrent_magnet"]})
    ]
    list_filter = ['releasetype']

class ModAdmin(admin.ModelAdmin):
    list_display = ['name', "category"]
    search_fields = ['name', "description", "author", "homepage"]
    fieldsets = [
        (None,            {'fields': ['name', "category", "service", "created_by"]}),
        ('Optional data', {'fields': ['description', "homepage", "author"]}),
    ]
    inlines = [ModDependencyInline]
    list_filter = ['category', "added", "service"]

class JsonServiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,            {'fields': ['name', "description", "active"]}),
        ('Access',        {'fields': ["owner", "editors", "open_for_all"]}),
        ('JSON data',     {'fields': ["json_name", "verbose_json", "json_file"]}),
        ('Torrent creation',  {'fields': ["torrent_enable", "torrent_announce", "torrent_path", "torrent_minimum_bytes", "torrent_webseeds"]})
    ]  
    
admin.site.register(Mod, ModAdmin)
admin.site.register(ModVersion, ModVersionAdmin)
admin.site.register(ModCategory)
admin.site.register(HostMirror)
admin.site.register(JsonServiceSuggestion)
admin.site.register(JsonService, JsonServiceAdmin)
