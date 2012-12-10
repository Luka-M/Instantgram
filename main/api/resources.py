# main/api/resources.py
from tastypie.resources import ModelResource, Resource, fields
from main.models import Image
from tastypie.constants import ALL, ALL_WITH_RELATIONS
import random

class ImageResource(ModelResource):
    class Meta:
        queryset = Image.objects.all()
        resource_name = 'image'
        filtering = {
            "tag": ALL,
        }
class TagObject(object):
    def __init__(self, initial=None):
        self.__dict__['_data'] = {}

        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def to_dict(self):
        return self._data

class TagResource(Resource):
    uuid = fields.CharField(attribute='uuid')
    text = fields.CharField(attribute='text')
    weight = fields.IntegerField(attribute='weight')

    class Meta:
        resource_name = 'tag'
        object_class = TagObject

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.uuid
        else:
            kwargs['pk'] = bundle_or_obj.uuid

        return kwargs
		
    def get_object_list(self, request):
        tmp = Image.objects.all()
        tmp = [p.tag for p in tmp]
        seen = set()
        seen_add = seen.add
        queryset = [ x for x in tmp if x not in seen and not seen_add(x)]
        rez = []
		
        for p in queryset:
            new_obj = TagObject()
            new_obj.text = p
            new_obj.uuid = queryset.index(p)
            new_obj.weight = random.randint(1, 10)
            rez.append(new_obj)
        return rez

    def obj_get_list(self, request=None, **kwargs):
        # Filtering disabled for brevity...
        return self.get_object_list(request)

