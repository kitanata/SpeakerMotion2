from tastypie.resources import ModelResource
from core.models import SpeakerBiography

class SpeakerBiographyResource(ModelResource):
    class Meta:
        queryset = SpeakerBiography.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
