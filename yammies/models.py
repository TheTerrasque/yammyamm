from django.db import models
import create_filedata
from django.conf import settings
# Create your models here.
import os.path

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

import json_interface

from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile

try:
    from makeTorrent import makeTorrent as mT
except ImportError:
    mT = None

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
    
    json_name = models.SlugField(unique=True)
    verbose_json = models.BooleanField(default=True)
    
    json_file = models.FileField(upload_to="service", storage=OverwriteStorage(), blank=True, null=True)
    
    active = models.BooleanField(default=True)
    
    torrent_enable = models.BooleanField(default=False)
    torrent_announce = models.CharField(max_length=200, blank=True, null=True)
    
    def __unicode__(self):
        return self.name

    def export(self):
        if self.active:
            json_interface.export_json(self)

    def save_json(self, data):
        self.json_file.save(self.json_name + ".json", ContentFile(data))

    def get_yamm_link(self):
        if self.json_file:
            return "yamm:service:" + settings.HOSTNAME + self.json_file.url
        return ""


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
    
    filesize = models.IntegerField(default=0)
    filehash = models.CharField(blank=True, null=True, max_length=90)
    homepage = models.CharField(null=True, blank=True, max_length=200)
    author = models.CharField(null=True, blank=True, max_length=60)
    
    active = models.BooleanField(default=True)
    
    torrent_file = models.FileField(upload_to="torrents", blank=True, null=True, storage=OverwriteStorage())
    torrent_magnet = models.TextField(blank=True)
    
    class Meta:
        ordering = ["name"]
    
    def __unicode__(self):
        return self.name
    
    def get_yamm_link(self):
        return "yamm:mod:" + self.name
    
    def create_torrent(self):
        if mT and self.service.torrent_enable and self.service.torrent_announce and self.archive:
            torrent = mT(announce=str(self.service.torrent_announce))
            torrent.single_file(str(self.get_archive_path()))
            content = ContentFile(torrent.getBencoded())
            self.torrent_file.save(self.name + "_" + self.version + ".torrent", content, save=False)
            self.torrent_magnet = torrent.info_hash()
            
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
    
    def save(self, *args, **kwargs):
        super(Mod, self).save(*args, **kwargs)
        self.update_file_data()
        super(Mod, self).save(*args, **kwargs)
    
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
    mod.service.export()

@receiver(post_save, sender=ModCategory)
def save_json4(sender, **kwargs):
    pass
    #mod = kwargs["instance"]
    #mod.service.export()