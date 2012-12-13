from tastypie.api import Api
from resources import ImageResource, TagResource

v1_api = Api(api_name='v1')
v1_api.register(ImageResource())
v1_api.register(TagResource())