from django.db import models
from instantgram import settings

class Tag(models.Model):
    name = models.CharField(max_length = 200, unique=True)
    weigth = models.IntegerField(default=1)
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if Tag.objects.filter(name = self.name).exists():
            t = Tag.objects.filter(name = self.name)
            t.update(weigth = self.weigth + 1)
        else:
            super(Tag, self).save(*args, **kwargs)

class Image(models.Model):
    title = models.CharField(max_length=100)
    md5hash = models.CharField(max_length=32, unique=True)
    url = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now=True)
    geolocation = models.CharField(max_length=200)
    
    tags = models.ManyToManyField(Tag);

    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        url = settings.MEDIA_ROOT + self.title
        #if not (Image.objects.filter(md5hash = self.md5hash).exists()):
            #super(Image, self).save(*args, **kwargs)
        
