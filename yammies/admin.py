from django.contrib import admin
from .models import Mod, ModCategory, ModDependency, HostMirror, JsonService, JsonServiceSuggestion

from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdminTabularInline

class ModDependencyInline(AjaxSelectAdminTabularInline):
    model = ModDependency
    form = make_ajax_form(ModDependency, {'dependency': 'mod'})
    extra = 5

class ModAdmin(admin.ModelAdmin):
    list_display = ['name', 'version', "category"]
    search_fields = ['name', "description", "author", "homepage"]
    fieldsets = [
        (None,            {'fields': ['name', "archive", "version", "category", "service"]}),
        ('Optional data', {'fields': ['description', "homepage", "author"]}),
        ('Torrent data',  {'fields': ["torrent_file", "torrent_magnet"]})
    ]
    inlines = [ModDependencyInline]
    list_filter = ['category', "added", "service"]

class JsonServiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,            {'fields': ['name', "description", "active"]}),
        ('JSON data',     {'fields': ["json_name", "verbose_json", "json_file"]}),
        ('Torrent creation',  {'fields': ["torrent_enable", "torrent_announce", "torrent_link", "torrent_minimum_bytes", "torrent_webseeds"]})
    ]  
    
admin.site.register(Mod, ModAdmin)
admin.site.register(ModCategory)
admin.site.register(HostMirror)
admin.site.register(JsonServiceSuggestion)
admin.site.register(JsonService, JsonServiceAdmin)
