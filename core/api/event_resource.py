from tastypie.resources import ModelResource
from core.models import Event

class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
