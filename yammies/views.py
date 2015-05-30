#from django.shortcuts import render
from . import models as M
# Create your views here.

from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView

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