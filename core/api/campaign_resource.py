import uuid

from django.db.models import Q

from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

from core.models import Campaign

class CampaignObjectsAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list.filter(
            Q(manager=bundle.request.user) | 
            Q(reviewers=bundle.request.user) |
            Q(speakers=bundle.request.user),
            deleted=False)

    def read_detail(self, object_list, bundle):
        return ((bundle.obj.manager == bundle.request.user) or
            (bundle.request.user in bundle.obj.reviewers) or
            (bundle.request.user in bundle.obj.speakers) and
            bundle.obj.deleted == False)

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        bundle.obj.manager = bundle.request.user
        return object_list

    def create_detail(self, object_list, bundle):
        return (bundle.obj.manager == bundle.request.user)

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.manager == bundle.request.user and obj.deleted == False:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return ((bundle.obj.manager == bundle.request.user) 
            and bundle.obj.deleted == False)

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        if bundle.obj.manager == bundle.request.user:
            bundle.obj.deleted = True
        else:
            raise Unauthorized("Sorry, no deletes.")


class CampaignResource(ModelResource):
    manager = fields.ToOneField('core.api.UserResource', 'manager')

    class Meta:
        queryset = Campaign.objects.filter()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        authorization = CampaignObjectsAuthorization()
        always_return_data = True

    def hydrate(self, bundle):
        if not bundle.obj.pk:
            bundle.obj.code = str(uuid.uuid4())

        return bundle