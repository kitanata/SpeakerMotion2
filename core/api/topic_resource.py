from tastypie.resources import ModelResource
from core.models import Topic

class TopicResource(ModelResource):
    class Meta:
        queryset = Topic.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
