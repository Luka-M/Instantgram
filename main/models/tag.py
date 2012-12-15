from django.db import models
from django.utils import timezone
from instantgram import settings
from datetime import datetime, timedelta
from main import geo

import main

class TagManager(models.Manager):
    """Manager class for Tag model."""
    
    def calcNearTags(self, latitude, longitude):
        """
        Queries db for all tags that are in certain radius of given GPS latitude and longitude.
        Radius is given by settings entry NEAR_DISTANCE.   
        """
        myPos = geo.xyz(float(latitude), float(longitude))
        imgs = main.models.image.Image.objects.all()
        tags = []
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
    
    def newTags(self, last):
        """
        Returns tags added in last `last` hours.
        """
        local = timezone.now()
        delta = timedelta(hours = last)
        local = local - delta
        
        return Tag.objects.filter(last_update__gt=local)


class Tag(models.Model):
    """Tag is annotation object for images. Image can have multiple tags.
    
    Attributes:
        name - Name of the tag.
        weight      - Number of pictures containig this tag.
        last_update - Date and time of last uploaded picture with this tag.
        objects     - Overriden django manager class which contains logic for advanced 
                      filtering of tags from db.
    """
    name = models.CharField(max_length = 200, unique=True)
    weigth = models.IntegerField(default=1)
    last_update = models.DateTimeField(auto_now=True)
    objects = TagManager()
    
    class Meta:
        app_label = "main"    
    
    def __unicode__(self):
        """ Overriden method for unicode representation of object."""
        return self.name
    
    def save(self, *args, **kwargs):
        """Overriden method for saving tag object.
           If tag allready exists, increases its weight and last_update, else saves new Tag object.
        """
        if Tag.objects.filter(name = self.name).exists():
            t = Tag.objects.filter(name = self.name)
            t.update(weigth = self.weigth + 1, last_update = timezone.now())
        else:
            super(Tag, self).save(*args, **kwargs)

