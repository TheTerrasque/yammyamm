from django.contrib import admin
from .models import Mod, ModCategory, ModDependency, HostMirror

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
        (None,            {'fields': ['name', "version", "category", "archive"]}),
        ('Optional data', {'fields': ['description', "homepage", "author"]}),
    ]
    inlines = [ModDependencyInline]
    list_filter = ['category', "added"]

admin.site.register(Mod, ModAdmin)
admin.site.register(ModCategory)
admin.site.register(HostMirror)