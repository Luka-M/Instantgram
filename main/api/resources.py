from tastypie.resources import ModelResource, Resource, fields
from main.models.image import Image, ImageManager
from main.models.tag import Tag, TagManager
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from instantgram import settings
from django.utils import timezone
import base64
import md5
import os

"""Module for defining API REST resources."""

class TagResource(ModelResource):
    """API resource for Tag object model."""
    
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        filtering = {"weigth": ALL, "name": ALL, "last_update": ALL}
        ordering = ["weigth"]
        authorization = Authorization()
        
    def apply_filters(self, request, applicable_filters):
        """Overriden Tastypie method for applying resource filter depending on type of incoming request."""
        
        latitude = request.GET.get('lat')
        longitude = request.GET.get('lon')
        last = request.GET.get('last')
        if latitude and longitude:
            queryset = Tag.objects.calcNearTags(latitude, longitude)
        elif last:
            queryset = Tag.objects.newTags(int(last))
        else:
            queryset = self.get_object_list(request).filter(**applicable_filters)
        return queryset
        

class ImageResource(ModelResource):
    """API resource for Image model."""
    
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
    
    def apply_filters(self, request, applicable_filters):
        """Overriden Tastypie method for applying resource filter depending on type of incoming request."""        
        tag = request.GET.get('tag')
        if tag:
            queryset = Image.objects.filterByTags(tag)
        else:
            queryset = self.get_object_list(request)
        return queryset
    
    def hydrate_img(self, bundle):
        """Overriden Tastypie method for parsing JSON data from incoming request."""
        
        bundle.data['url'] = ''
        """Image data is encoded as base64 ASCII string"""
        base64string = bundle.data['img']
        
        """Md5hash is created from image data, which is checked for duplicate image upload."""
        bundle.data['md5hash'] = md5.new(base64string).hexdigest()         
        
        if not (Image.objects.filter(md5hash = bundle.data['md5hash']).exists()):
            ext = bundle.data['ext']
            """Create unique image name."""
            name = bundle.data['title'] + timezone.now().strftime("%Y_%m_%d_%H_%M_%S_%f") +  base64.urlsafe_b64encode(os.urandom(settings.SALT_LENGHT)) + "." + ext
            bundle.data['title'] = name
            fh = open(settings.MEDIA_ROOT + "images/" + name, "wb")
            fh.write(base64string.decode('base64'))
            fh.close()
            
        return bundle;