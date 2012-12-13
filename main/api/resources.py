# main/api/resources.py
from tastypie.resources import ModelResource, Resource, fields
from main.models import Image, Tag
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from instantgram import settings
import md5

class TagResource(ModelResource):
    
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        
        authorization = Authorization()

class ImageResource(ModelResource):
    img = fields.CharField(attribute='img', default='')
    tags = fields.ManyToManyField(TagResource, 'tags')
    
    class Meta:
        queryset = Image.objects.all()
        resource_name = 'image'
        filtering = {
            "tag": ALL,
        }
        authorization = Authorization()
        
    def hydrate_img(self, bundle):
        base64string = bundle.data['img']
        name = bundle.data['title']
        fh = open(settings.MEDIA_ROOT + "images/" + name, "wb")
        fh.write(base64string.decode('base64'))
        fh.close()
        
        bundle.data['md5hash'] = md5.new(base64string).hexdigest()
        bundle.data['url'] = settings.MEDIA_ROOT + name
            
        return ;