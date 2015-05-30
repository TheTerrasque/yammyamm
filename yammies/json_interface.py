import json
from django.core.files import File
import models as M# Mod, ModCategory, ModDependency, HostMirror

#>>> from yammies import json_interface as ym; ym.import_json("/home/terra/old/public/yamm/mods.json", "/home/terra/old/public/yamm/files/")

def import_json(jsonfile, basefiledir, service):
    data = json.load(open(jsonfile))
    for mod in data["mods"]:
        print "Importing %s" % mod["name"]
        modentry = M.Mod(name=mod["name"], service=service)
        modentry.version = mod["version"]
        modentry.description = mod.get("description", "")
        modentry.homepage = mod.get("homepage", "")
        modentry.author = mod.get("author", "")
        cat, created = M.ModCategory.objects.get_or_create(name=mod.get("category", "none"))
        modentry.category = cat
        if "filename" in mod:
          mf = basefiledir + mod["filename"]
          of = File(open(mf))
        
          modentry.archive.save(mod["filename"], of, save=False)
        modentry.save()
        
        for dep in mod.get("depends", []):
            M.ModDependency.objects.create(mod=modentry, relation=0, dependency=dep)
        for dep in mod.get("provides", []):
            M.ModDependency.objects.create(mod=modentry, relation=1, dependency=dep)
        for dep in mod.get("conflicts", []):
            M.ModDependency.objects.create(mod=modentry, relation=2, dependency=dep)
        for dep in mod.get("recommends", []):
            M.ModDependency.objects.create(mod=modentry, relation=3, dependency=dep)


    
