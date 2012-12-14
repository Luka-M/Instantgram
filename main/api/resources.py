# main/api/resources.py
from tastypie.resources import ModelResource, Resource, fields
from main.models import Image, Tag
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from instantgram import settings
from django.utils import timezone
import base64
import md5
import os

class TagResource(ModelResource):
    
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        filtering = {"weigth": ALL, "name": ALL, "last_update": ALL}
        ordering = ["weigth"]
        authorization = Authorization()
        
    def apply_filters(self, request, applicable_filters):
        latitude = request.GET.get('lat')
        longitude = request.GET.get('lon')
        last = request.GET.get('last')
        if latitude and longitude:
            queryset = Tag.objects.calcNearTags(latitude, longitude)
        elif last:
            queryset = Tag.objects.newTags(last)
        else:
            queryset = self.get_object_list(request)
        return queryset
        

class ImageResource(ModelResource):
    img = fields.CharField(attribute='img', default='')
    ext = fields.CharField(attribute='ext', default='')
    tags = fields.ManyToManyField(TagResource, 'tags')
    
    class Meta:
        queryset = Image.objects.all()
        resource_name = 'image'
        filtering = {
            "tags": ALL,
        }
        authorization = Authorization()
        
    def hydrate_img(self, bundle):
        bundle.data['url'] = ''
        base64string = bundle.data['img']
        ext = bundle.data['ext']
        name = bundle.data['title'] + timezone.now().strftime("%Y_%m_%d_%H_%M_%S_%f") +  base64.urlsafe_b64encode(os.urandom(settings.SALT_LENGHT)) + "." + ext
        bundle.data['title'] = name
        fh = open(settings.MEDIA_ROOT + "images/" + name, "wb")
        fh.write(base64string.decode('base64'))
        fh.close()
        
        bundle.data['md5hash'] = md5.new(base64string).hexdigest()
            
        return bundle;