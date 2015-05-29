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


# from yammies import json_interface as j; j.export_json("/home/terra/old/public/yamm/export.json")        
def export_json(service):
    d = {
        "mods": [],
        "service": {
            "name": service.name,
        }
    }
    
    d["service"]["filelocations"] = [x.url for x in service.hostmirror_set.filter(active=True)]
    
    for mod in service.mod_set.filter(active=True):
        m = {
            "name": mod.name,
            "version": mod.version,
        }
        if mod.archive:
            m["filename"] = mod.archive.name[len("files/"):]
            
        for key in ["category", "description", "filehash", "filesize", "homepage", "author", ("torrent_file", "torrent"), ("torrent_magnet", "magnet")]:
            if isinstance(key, basestring):
                k = v = key
            else:
                k, v = key
            if getattr(mod, k):
                m[v] = unicode(getattr(mod, k))
                
        for depnr, deptype in enumerate(["depends", "provides", "conflicts", "recommends"]):
            entries = [x.dependency for x in M.ModDependency.objects.filter(mod=mod, relation=depnr) if x.dependency != mod.name]
            if entries:
                m[deptype] = entries
                
        d["mods"].append(m)
        

    if service.verbose_json:
        j = json.dumps(d, indent=4)
    else:
        j = json.dumps(d)
    service.save_json(j)
    
