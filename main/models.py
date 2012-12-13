from django.db import models
from instantgram import settings
from django.utils import timezone
import geo

class TagManager(models.Manager):
    
    def calcNearTags(self, latitude, longitude):
        myPos = geo.xyz(float(latitude), float(longitude))
        imgs = Image.objects.all()
        tags = []#
        excludes = []
        for img in imgs:
            imgPos = geo.xyz(float(img.lat), float(img.lon))
            distance = geo.distance(myPos, imgPos)
            if (distance <= settings.NEAR_DISTANCE):
                for t in img.tags.all():
                    if t not in tags:
                        tags.append(t)
        
        return tags
    
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
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        url = settings.MEDIA_ROOT + self.title
        if (Image.objects.filter(md5hash = self.md5hash).exists()):
            self.full_clean()
        super(Image, self).save(*args, **kwargs)
        
