from django.db import models
import create_filedata
from django.conf import settings
# Create your models here.
import os.path

from django.db.models.signals import post_save
from django.dispatch import receiver

import json_interface

class ModCategory(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class HostMirror(models.Model):
    url = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.url

class Mod(models.Model):
    name = models.CharField(db_index=True, max_length=30)
    version = models.CharField(max_length=30)
    category = models.ForeignKey(ModCategory)
    archive = models.FileField(upload_to="files")
    
    updated = models.DateTimeField(auto_now=True)
    added = models.DateTimeField(auto_now_add=True)
    
    description = models.TextField(blank=True)
    
    filesize = models.IntegerField(default=0)
    filehash = models.CharField(blank=True, null=True, max_length=90)
    homepage = models.CharField(null=True, blank=True, max_length=200)
    author = models.CharField(null=True, blank=True, max_length=60)
    
    active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name
    
    def update_file_data(self):
        root = settings.MEDIA_ROOT or settings.BASE_DIR
        
        data = create_filedata.filedata(os.path.join(root, self.archive.name))
        self.filehash = data["filehash"]
        self.filesize = data["filesize"]
    
    def save(self, *args, **kwargs):
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
    
    
@receiver(post_save, sender=Mod)
def save_json(sender, **kwargs):
    if settings.YAMM_EXPORT_PATH:
        json_interface.export_json(settings.YAMM_EXPORT_PATH)