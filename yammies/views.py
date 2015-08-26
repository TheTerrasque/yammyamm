#from django.shortcuts import render
from . import models as M
# Create your views here.

from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.shortcuts import get_object_or_404

from braces import views as BV

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
        service = get_object_or_404(M.JsonService, pk=self.kwargs["pk"])
        return service.owner == user
    
    def get_success_url(self):
        return self.object.get_edit_url()
    
    def form_valid(self, form):
        service = get_object_or_404(M.JsonService, pk=self.kwargs["pk"])
        
        form.instance.created_by = self.request.user
        form.instance.active = False
        form.instance.service = service
        
        return super(ModCreate, self).form_valid(form)

class ModEdit(BV.LoginRequiredMixin, UpdateView):
    model = M.Mod
    fields = ["name", "version", "category", "description", "homepage", "author", "archive", "active", "changelog", "long_description"]
    template_name = "mods/mod_edit.html"
    
    def test_func(self, user):
        return self.object.created_by == user
    
    def get_success_url(self):
        return self.object.get_edit_url()