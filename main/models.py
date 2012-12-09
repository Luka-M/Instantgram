from django.db import models

class Image(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    geolocation = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title