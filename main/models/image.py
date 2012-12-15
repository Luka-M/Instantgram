from django.db import models
from django.utils import timezone
from instantgram import settings
from tag import Tag
import datetime

class ImageManager(models.Manager):
    """Manager class for Image model."""
    
    def filterByTags(self, tag):
        """Filters images by given tag."""
        images = []
        for img in Image.objects.all():
            for t in img.tags.all():
                if t.name == tag:
                    images.append(img)
        return images

class Image(models.Model):
    """Model class representing image.
       
       Attributes:
           title    - Image title.
           md5hash  - Md5 hash digest of image base64 string representation,
                      which is used to check possible duplicate uploads.
           url      - Relative location of the image on disk.
           pub_date - Publication date of image. Date and time of upload.
           lat      - GPS geographical latitude of image. 
                      Can be NULL if data is not available during image capture.
           lon      - GPS geographical longiture of image. 
                      Can be NULL if data is not available during image capture.
           tags     - List of tags associated with image. Image can have multiple tags.
    """
    title = models.CharField(max_length=100)
    md5hash = models.CharField(max_length=32, unique=True)
    url = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now=True)
    lat = models.FloatField(default=0, null=True)
    lon = models.FloatField(default=0, null=True)
    
    tags = models.ManyToManyField(Tag)
    
    objects = ImageManager()
    
    class Meta:
        app_label = "main"

    def __unicode__(self):
        """Overriden method for unicode representation of object."""
        return self.url
    
    def save(self, *args, **kwargs):
        """Overriden method for saving image object to disk, ann related data to db.
           If md5hash digest of image exists in db, it does not save it because it is a duplicate.
        """
        self.url = settings.MEDIA_URL + "images/" + self.title 
        if (Image.objects.filter(md5hash = self.md5hash).exists()):
            self.full_clean()
        super(Image, self).save(*args, **kwargs)