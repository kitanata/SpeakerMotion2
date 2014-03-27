from tastypie.resources import ModelResource
from core.models import Review

class ReviewResource(ModelResource):
    class Meta:
        queryset = Review.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
