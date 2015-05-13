import json
from django.core.files import File
import models as M# Mod, ModCategory, ModDependency, HostMirror
from django.conf import settings

#>>> from yammies import json_interface as ym; ym.import_json("/home/terra/old/public/yamm/mods.json", "/home/terra/old/public/yamm/files/")

def import_json(jsonfile, basefiledir):
    data = json.load(open(jsonfile))
    for mod in data["mods"]:
        print "Importing %s" % mod["name"]
        modentry = M.Mod(name=mod["name"])
        modentry.version = mod["version"]
        modentry.description = mod.get("description", "")
        modentry.homepage = mod.get("homepage", "")
        modentry.author = mod.get("author", "")
        cat, created = M.ModCategory.objects.get_or_create(name=mod.get("category", "none"))
        modentry.category = cat
        mf = basefiledir + mod["filename"]
        of = File(open(mf))
        modentry.archive.save(mod["filename"], of, save=False)
        modentry.save()
        
        #modentry.update_file_data()
        #modentry.save()
        
        #print modentry.archive.name
        
        for dep in mod.get("depends", []):
            M.ModDependency.objects.create(mod=modentry, relation=0, dependency=dep)
        for dep in mod.get("provides", []):
            M.ModDependency.objects.create(mod=modentry, relation=1, dependency=dep)
        for dep in mod.get("conflicts", []):
            M.ModDependency.objects.create(mod=modentry, relation=2, dependency=dep)
        for dep in mod.get("recommends", []):
            M.ModDependency.objects.create(mod=modentry, relation=3, dependency=dep)


# from yammies import json_interface as j; j.export_json("/home/terra/old/public/yamm/export.json")        
def export_json(target):
    d = {
        "mods": [],
        "service": settings.YAMM_SERVICE.copy()
    }
    
    d["service"]["filelocations"] = [x.url for x in M.HostMirror.objects.filter(active=True)]
    
    for mod in M.Mod.objects.filter(active=True):
        m = {
            "name": mod.name,
            "version": mod.version,
            "filename": mod.archive.name[len("files/"):],
        }
        for key in ["category", "description", "filehash", "filesize", "homepage", "author"]:
            if getattr(mod, key):
                m[key] = unicode(getattr(mod, key))
                
        for depnr, deptype in enumerate(["depends", "provides", "conflicts", "recommends"]):
            entries = [x.dependency for x in M.ModDependency.objects.filter(mod=mod, relation=depnr) if x.dependency != mod.name]
            if entries:
                m[deptype] = entries
                
        d["mods"].append(m)
        
    outfile = open(target, "w")
    
    if settings.YAMM_VERBOSE_JSON:
        json.dump(d, outfile, indent=4)
    else:
        json.dump(d, outfile)
    