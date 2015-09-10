#from django.shortcuts import render
from . import models as M
from . import forms as F
# Create your views here.

from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from braces import views as BV

# ---- Mixin classes ----

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

# ----- View classes ----

class Home(TemplateView):
    template_name = "mods/index.html"
    
class Services(ListView):
    queryset = M.JsonService.objects.filter(active=True)
    template_name = "mods/list_services.html"
    
class Mods(ListView):
    queryset = M.Mod.objects.filter(active=True)
    template_name = "mods/list_mods.html"
    
class ModDisplay(DetailView):
    queryset = M.Mod.objects.filter(active=True)
    template_name = "mods/show_mod.html"

class ServiceDisplay(DetailView):
    queryset = M.JsonService.objects.filter(active=True)
    template_name = "mods/show_service.html"
    
class ModCreate(BV.LoginRequiredMixin, BV.UserPassesTestMixin, CreateView):
    model = M.Mod
    fields = ["name", "version", "category"]
    template_name = "mods/mod_create.html"
    
    def test_func(self, user):
        self.active_service = get_object_or_404(M.JsonService, pk=self.kwargs["pk"])
        return self.active_service.owner == user
    
    def get_success_url(self):
        return self.object.get_edit_url()
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.active = False
        form.instance.service = self.active_service
        
        return super(ModCreate, self).form_valid(form)

class ModEdit(BV.LoginRequiredMixin, BV.UserPassesTestMixin, UpdateView):
    model = M.Mod
    fields = ["name", "version", "category", "description", "homepage", "author", "archive", "active", "changelog", "long_description"]
    template_name = "mods/mod_edit.html"
    
    def test_func(self, user):
        obj = get_object_or_404(M.Mod, pk=self.kwargs["pk"])
        return obj.created_by == user
    
    def get_success_url(self):
        return self.object.get_edit_url()

class ModRelationMeta(BV.LoginRequiredMixin, BV.UserPassesTestMixin):
    model = M.ModDependency
    form_class = F.ModRelationForm
    
    def test_func(self, user):
        return self.get_mod().created_by == user
    
class ModCreateRelation(ModRelationMeta, CreateView):
    template_name = "mods/relation/mod_relation_create.html"

    def get_mod(self):
        return get_object_or_404(M.Mod, pk=self.kwargs["pk"])

    def form_valid(self, form):        
        form.instance.mod = self.get_mod()      
        return super(ModCreateRelation, self).form_valid(form)
    
class ModEditRelation(ModRelationMeta, UpdateView):
    template_name = "mods/relation/mod_relation_edit.html"

    def get_mod(self):
        return get_object_or_404(M.ModDependency, pk=self.kwargs["pk"]).mod

    def get_success_url(self):
        return self.object.mod.get_edit_url()
    
class ModRemoveRelation(ModRelationMeta, DeleteView):
    success_url = "/"
    template_name = "mods/relation/mod_relation_delete.html"
    
    def get_mod(self):
        return get_object_or_404(M.ModDependency, pk=self.kwargs["pk"]).mod