from django.db import models
import create_filedata
from django.conf import settings
# Create your models here.
import os.path
import json
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile

from django.core.urlresolvers import reverse

from django.core.files import File

from django.contrib.auth.models import User

try:
    from makeTorrent import makeTorrent as mT
except ImportError:
    mT = None

class IgnorePostSave:
    def __init__(self, function, sender):
        self.function = function
        self.sender = sender
    
    def __enter__(self):
        post_save.disconnect(self.function, sender=self.sender)

    def __exit__(self, type, value, traceback):
        post_save.connect(self.function, sender=self.sender)
    
class OverwriteStorage(FileSystemStorage):
    '''
    Delete old file before saving new
    '''
    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class ModCategory(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class JsonService(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
        
    json_name = models.SlugField(unique=True, help_text="Base name for json file")
    verbose_json = models.BooleanField(default=True, help_text="Make the generated JSON file more readable. Turn off to save space")
    json_file = models.FileField(upload_to="service", storage=OverwriteStorage(), blank=True, null=True)
    
    torrent_enable = models.BooleanField(default=False, help_text="Enable torrent gereration for mods connected to this service")
    torrent_announce = models.CharField(max_length=200, default="udp://open.demonii.com:1337", blank=True, null=True)

    torrent_path = models.CharField(max_length=200, blank=True, null=True)
    torrent_minimum_bytes = models.PositiveIntegerField(default=5*1024*1024, help_text="Minimum size to generate a torrent for the mod")
    torrent_webseeds = models.BooleanField(default=False, help_text="Add http link to the file in torrent. Largely unsupported, and requires at least one Host Mirror entry")
    
    owner = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.name

    def user_can_add_mod(self, user):
        return user == self.owner

    def get_mirrors(self):
        mirrors = self.hostmirror_set.filter(active=True)
        if mirrors:
            return [x.url for x in mirrors]
        return [settings.MEDIA_URL + "mods/"]

    def get_torrent_path(self):
        if not self.torrent_path:
            return settings.MEDIA_URL + "torrents/"
        return self.torrent_path
    
    def get_absolute_url(self):
        return reverse('mod:servicedetail', args=[str(self.id)])
    
    def get_mods(self):
        return self.mod_set.filter(active=True)
    
    def get_announce(self):
        return str(self.torrent_announce)
    
    def export(self):
        if self.active:
            service = {
                "name": self.name,
                "filelocations": self.get_mirrors(),
            }
           
            if self.torrent_enable:
                service["torrents"] = self.get_torrent_path()
            
            if self.get_suggestions():
                service["recommend"] = self.get_suggestions()

            mods = []
            for mod in self.get_mods():  
                mods.append(mod.create_json_entry())

            d = {
                "mods": mods,
                "service": service
            }
                
            if self.verbose_json:
                j = json.dumps(d, indent=4)
            else:
                j = json.dumps(d)
            self.save_json(j)

    def save_json(self, data):
        with IgnorePostSave(save_json5, JsonService):
            self.json_file.save(self.json_name + ".json", ContentFile(data))

    def get_suggestions(self):
        return [x.url for x in self.jsonservicesuggestion_set.all()]
    
    def get_json_url(self):
        return self.json_file and settings.HOSTNAME + self.json_file.url
    
    def get_yamm_link(self):
        if self.json_file:
            return "yamm:service:" + self.get_json_url()
        return ""

class JsonServiceSuggestion(models.Model):
    service = models.ForeignKey(JsonService)
    url = models.URLField()

    def __unicode__(self):
        return u"Service suggestion for %s" % self.service
    

class HostMirror(models.Model):
    service = models.ForeignKey(JsonService)
    url = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.url

class Mod(models.Model):
    service = models.ForeignKey(JsonService)
    
    name = models.CharField(db_index=True, max_length=30)
    version = models.CharField(max_length=30)
    category = models.ForeignKey(ModCategory)
    
    archive = models.FileField(upload_to="mods", blank=True, null=True, storage=OverwriteStorage())
    
    updated = models.DateTimeField(auto_now=True)
    added = models.DateTimeField(auto_now_add=True)
    
    description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    changelog = models.TextField(blank=True)
    
    filesize = models.IntegerField(default=0)
    filehash = models.CharField(blank=True, null=True, max_length=90)
    homepage = models.CharField(null=True, blank=True, max_length=200)
    author = models.CharField(null=True, blank=True, max_length=60)
    
    active = models.BooleanField(default=True)
    
    torrent_file = models.FileField(upload_to="torrents", blank=True, null=True, storage=OverwriteStorage())
    torrent_magnet = models.TextField(blank=True)
    
    created_by = models.ForeignKey(User)
    
    class Meta:
        ordering = ["name"]
    
    def __unicode__(self):
        return self.name
    
    @property
    def torrent_filename(self):
        return self.torrent_file and self.torrent_file.name[len("torrents/"):]
    
    def get_yamm_link(self):
        link = "yamm:"
        
        service = self.service.get_json_url()
        if service:
            link = link + "service:%s|" % service
            
        link = link + "mod:%s" % self.name
        return link
    
    def create_json_entry(self):
        m = {
            "name": self.name,
            "version": self.version,
        }
        if self.archive:
            m["filename"] = self.get_filename()
            
        extra = []
        
        if self.service.torrent_enable:
            extra = [(self.torrent_filename, "torrent")]
            #else:
            #    extra = [("torrent_magnet", "magnet")]
            
        for key in ["category", "description", "filehash", "filesize", "homepage", "author"] + extra:
            if isinstance(key, basestring):
                k = key
                v = unicode(getattr(self, key))
            else:
                k, v = key
            if k:
                m[v] = k
                
        for depnr, deptype in enumerate(["depends", "provides", "conflicts", "recommends"]):
            entries = [x.dependency for x in self.get_dependencies().filter(relation=depnr).exclude(dependency=self.name)]
            #entries = [x.dependency for x in ModDependency.objects.filter(mod=self, relation=depnr) if x.dependency != self.name]
            if entries:
                m[deptype] = entries
        return m
    
    def get_dependencies(self):
        return self.moddependency_set.all()
    
    def create_torrent(self):
        if mT and self.service.torrent_enable and self.service.torrent_announce \
                and self.archive and self.service.torrent_minimum_bytes < self.filesize:
            
            S = None
            if self.service.torrent_webseeds:
                S = [str(x) + self.get_filename().encode("utf8") for x in self.service.get_mirrors()]
            
            torrent = mT(announce=str(self.service.get_announce()), httpseeds=S)
            torrent.single_file(str(self.get_archive_path()))
            
            content = ContentFile(torrent.getBencoded())
            self.torrent_file.save(self.name + "_" + self.version + ".torrent", content, save=False)
            
            self.torrent_magnet = torrent.info_hash()

    def import_file(self, filepath, filename=None):
        of = File(open(filepath, "rb"))
        if not filename:
            filename = os.path.basename(filepath)
        self.archive.save(filename, of, save=False)
    
    def get_filename(self):
        return self.archive.name[len("mods/"):]
            
    def get_archive_path(self):
        root = settings.MEDIA_ROOT or settings.BASE_DIR
        return os.path.join(root, self.archive.name)
    
    def update_file_data(self):
        if self.archive:
            data = create_filedata.filedata(self.get_archive_path())
            self.filehash = data["filehash"]
            self.filesize = data["filesize"]
        else:
            self.filehash = None
            self.filesize = 0
    
    def get_edit_url(self):
        return reverse('mod:mod_edit', args=[str(self.id)])
    
    def get_absolute_url(self):
        return reverse('mod:moddetail', args=[str(self.id)])
    
    def get_dependencies_detailed(self):
        D = []
        for k, v in DEPENDENCY:
            deps = self.moddependency_set.filter(relation=k)
            if deps:
                d = {
                    "name": v,
                    "mods": deps
                }
                D.append(d)
        return D
            
    
DEPENDENCY = [
    (0, "Requires"),
    (1, "Provides"),
    (2, "Conflicts"),
    (3, "Recommends"),
]

class ModDependency(models.Model):
    mod = models.ForeignKey(Mod)
    dependency = models.CharField(db_index=True, max_length=30)
    relation = models.IntegerField(choices = DEPENDENCY, default=0)
    
    def __unicode__(self):
        return "<%s> %s %s" % (self.mod, self.get_relation_display(), self.dependency)

    def get_modentry(self):
        r = Mod.objects.filter(name=self.dependency)
        if r:
            return r[0]

    def get_absolute_url(self):
        return reverse('mod:moddetail', args=[str(self.mod.id)])


@receiver(post_save, sender=JsonService)
def save_json5(sender, **kwargs):
    service = kwargs["instance"]
    service.export()
 
@receiver(post_save, sender=HostMirror)
def save_json3(sender, **kwargs):
    mirror = kwargs["instance"]
    mirror.service.export()

@receiver(post_save, sender=ModDependency)
def save_json2(sender, **kwargs):
    mod = kwargs["instance"].mod
    mod.service.export()

@receiver(pre_save, sender=Mod)
def update_dependency_names(sender, instance, **kwargs):
    if instance.id: # without an instance id, this is a create action                                                                                                                                            
        old = sender.objects.get(pk=instance.id)
        if old.name != instance.name:
            ModDependency.objects.filter(dependency=old.name).update(dependency=instance.name)
    
@receiver(post_save, sender=Mod)
def save_json(sender, **kwargs):
    mod = kwargs["instance"]
    with IgnorePostSave(save_json, Mod):
        mod.update_file_data()
        mod.create_torrent()
        mod.save()
    mod.service.export()
