from tastypie.resources import ModelResource
from core.models import Proposal

class ProposalResource(ModelResource):
    class Meta:
        queryset = Proposal.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
