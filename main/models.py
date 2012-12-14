from django.db import models
from instantgram import settings
from django.utils import timezone
import geo
import datetime

class TagManager(models.Manager):
    
    def calcNearTags(self, latitude, longitude):
        myPos = geo.xyz(float(latitude), float(longitude))
        imgs = Image.objects.all()
        tags = []#
        excludes = []
        
        for img in imgs:
            if img.lat and img.lon:
                imgPos = geo.xyz(float(img.lat), float(img.lon))
                distance = geo.distance(myPos, imgPos)
                if (distance <= settings.NEAR_DISTANCE):
                    for t in img.tags.all():
                        if t not in tags:
                            tags.append(t)
        
        return tags
    
    def newTags(self, deltaTime):
        local = timezone.now()
        local = local.replace(hour = local.hour - deltaTime)
        
        return Tags.objects.filter(last_update__gt=local)
        
class Tag(models.Model):
    name = models.CharField(max_length = 200, unique=True)
    weigth = models.IntegerField(default=1)
    last_update = models.DateTimeField(auto_now=True)
    objects = TagManager()
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if Tag.objects.filter(name = self.name).exists():
            t = Tag.objects.filter(name = self.name)
            t.update(weigth = self.weigth + 1, last_update = timezone.now())
        else:
            super(Tag, self).save(*args, **kwargs)

class Image(models.Model):
    title = models.CharField(max_length=100)
    md5hash = models.CharField(max_length=32, unique=True)
    url = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now=True)
    lat = models.FloatField(default=0, null=True)
    lon = models.FloatField(default=0, null=True)
    
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.url = settings.MEDIA_URL + self.title 
        if (Image.objects.filter(md5hash = self.md5hash).exists()):
            self.full_clean()
        super(Image, self).save(*args, **kwargs)
        
